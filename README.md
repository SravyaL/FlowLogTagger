# Flow Log Tagger

A Python script for parsing log files(Version 2) and generating CSV reports with tag and port/protocol counts.

## Overview

This script processes log files to produce two CSV reports:
1. **Tag Counts**: Counts of each tag based on a lookup table.
2. **Port/Protocol Counts**: Counts of occurrences of port/protocol combinations.

## Features

- **Input Handling**: Reads log files and configuration files.
- **CSV Conversion**: Converts lookup and protocol tables into dictionaries.
- **CSV Output**: Writes the results to output CSV files.

## Requirements

- Python 3.x
- `csv` module (included in Python standard library)
- `argparse` module (included in Python standard library)

## Assumptions

- **Log File Format**: The log file must be in a specific format where:
  - The destination port is located at index 6.
  - The protocol is located at index 7.
  - Each line in the log file is space-separated.
- **Lookup Table Format**: The lookup CSV/txt file should have columns:
  - `dstport`: The destination port.
  - `protocol`: The protocol type.
  - `tag`: The associated tag.
- **Protocol File Format**: The protocol CSV file should have columns:
  - `Decimal`: The protocol number.
  - `Keyword`: The protocol name.
- Tag counts are based on matches with Lookup Table
- Port/Protocol counts are based on matches with input Log File 

## Installation

1. **Clone the repository:**

    ```bash
   git clone https://github.com/SravyaL/FlowLogTagger.git
    ```

2. **Navigate into the project directory:**

    ```bash
    cd FlowLogTagger
    ```
Alternatively, the code can be downloaded as .zip and run

## Usage

### Running the Script

To run the script, use the following command:

1. Run the file with default input files 

```bash
python log_parser.py
```
2. Run the file with custom input files - can take one or both - log file and look up file 
```bash
python log_parser.py --log_file <path_to_log_file> --lookup_file <path_to_lookup_file>
```

## Output
The script generates two CSV files in the current directory:

- op_tag_counts.csv: Contains tag counts.
- op_port_protocol_counts.csv: Contains port/protocol combination counts.
