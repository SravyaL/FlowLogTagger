import csv
import os
import argparse

def parse_file_arguments():
    """Handles custom input files"""
    parser = argparse.ArgumentParser(description="Process input files.")
    parser.add_argument('--log_file', default='data/input_logs.txt', help='Path to the input log file')
    parser.add_argument('--lookup_file', default='data/lookup_table.csv', help='Path to the lookup table CSV')
    return parser.parse_args()

def csv_to_list_dict(input, specific): 
    """Converts the lookup and protocol tables into dictionaries"""
    try:
        with open(input, 'r') as lookup:
            reader = csv.DictReader(lookup)
            if not specific:
                #this block handles the lookup table
                list_dict = {}
                for row in reader:
                    #if no proper keys found, adding Unnamed tag to handle different format
                    list_dict[(row.get('dstport','0'), row.get('protocol','0').lower())] = row.get('tag','Unnamed')
            else:
                #this block handles the protocol table
                list_dict = {}
                for row in reader:
                    list_dict[row.get('Decimal')] = row.get('Keyword')
        return list_dict
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
    

def write_to_csv(dictionary, output):
    """This function handles writing the supplied dictionary to the output file"""
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        if('tag' in output):
            #tag counts
            writer.writerow(['Tag', 'Count'])
            for tag, count in dictionary.items():
                writer.writerow([tag, count])
        else: 
            #port/protocol counts
            writer.writerow(["Port", "Protocol", "Count"])
            for (port, protocol), count in dictionary.items():
                writer.writerow([port, protocol, count])
    
def count_matches(ip_log_file, lookup, protocol, tag_counts, port_protocol_counts):
    """This function handles counting the matches and returns the dictionaries"""
    try:
        with open(ip_log_file, 'r') as logs:
            for line in logs:
                line = line.strip().split(" ")
                if len(line) != 14 and line != [''] :
                    #handling where the log isn't in expected format
                    print("Line skipped due to insufficient data:", line)
                    continue
                if(line != [''] and (line[6].isdigit() and line[7].isdigit())):
                    # dstport - index 6 and protocol - index 7
                    
                    #key for loopup dictionary 
                    key = (line[6],protocol.get(line[7],'0').lower())
                    
                    #Updating dictionary to reflect port/protocol counts
                    port_protocol_counts[key] = port_protocol_counts.get(key,0) +1
                    
                    #Below if-else condition is to reflect appropriate tag counts
                    if(key in lookup):                    
                        tag_counts[lookup[key]] = tag_counts.get(lookup[key],0) + 1               
                    else:
                        tag_counts['Untagged'] = tag_counts.get('Untagged',0) + 1
                        
                elif(line != ['']):
                    #Handling no data and skipped record
                    print("There is a 'no data and skipped record'!")
                    
    except Exception as e:
        print(f"Error occurred with input log file: {e}")
     
    return tag_counts, port_protocol_counts
            

def main():
    """This function handles parsing and counting the matches by calling appropriate functions"""
    args = parse_file_arguments()
    #input files
    ip_log_file = args.log_file
    ip_lookup_file = args.lookup_file
    
    #The protocol dictionary from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
    ip_protocol_file = 'data/protocol-numbers.csv'
    
    #output files
    op_tag_counts = 'op_tag_counts.csv'
    op_port_protocol_counts = 'op_port_protocol_counts.csv'    
        
    #output count dictionaries
    tag_counts = {}
    port_protocol_counts = {}
    
    #converting the csv files to dictionaries using a function
    lookup = csv_to_list_dict(ip_lookup_file, False)
    protocol = csv_to_list_dict(ip_protocol_file, True)
    
    #Counting the matches and updating the dictionaries
    tag_counts, port_protocol_counts = count_matches(ip_log_file, lookup, protocol, tag_counts, port_protocol_counts)
    
    #Writing output files using dictionaries
    write_to_csv(tag_counts,op_tag_counts)
    write_to_csv(port_protocol_counts,op_port_protocol_counts)
    print("Tag counts file created at:", os.path.abspath(op_tag_counts))
    print("Port/Protocol counts file created at:", os.path.abspath(op_port_protocol_counts))


if __name__ == "__main__":
    main()