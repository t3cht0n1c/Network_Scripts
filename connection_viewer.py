#!/usr/bin/python
'''
Name: eSentire_Parser.py
Description: Script to find unique traffic destinations
By: TMaz
Info: The original excel/csv file must be converted into a csv prior to script execution
'''

import os
import sys
import argparse
import re
import csv
import pprint

def main():

        parser = argparse.ArgumentParser(
                prog='Connection Viewer',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='''\
This program takes user input to parse a CSV file and find unique traffic flows

Requirements:
-------------

1) CSV file for input
                ''',
                epilog="Edge Technology Group")

        parser.add_argument(
                "--ip",
                help="Specific IP to find Flow(s) for",
                type=str)
        parser.add_argument(
                "-i",
                "--input_file",
                help="Input File to parse",
                required=True)
        parser.add_argument(
                "-o",
                "--output_file",
                help="File to output traffic flows. Default = <inputfile>_results.csv")

        args = parser.parse_args()

        if args.ip != None and args.output_file == None:
                outFile = args.input_file + "_results-" + args.ip + ".csv"
        elif args.ip == None and args.output_file == None:
                outFile = args.input_file + "_results.csv"
        else:
                outFile = args.output_file

        inFile = args.input_file
        if not inFile.endswith('.csv'):
                print("*** ERROR *** " + inFile + " is not a .csv file!")
                sys.exit()

        inFile = open(args.input_file)
        inRead = csv.reader(inFile)
        #inData = list(inRead)

        connections = {}

        for row in inRead:
                if len(row) < 2:
                        continue
                dst_ip = row[0]
                port = row[1]
                count = 1

                if dst_ip in connections.keys():
                        dst_dict = connections[dst_ip]

                        if port in dst_dict.keys():
                                port_dict = dst_dict[port]
                                port_dict['count'] += count

                        else:
                                dst_dict[port] = port_dict
                                port_dict = {'count' : count}

                else:
                        connections[dst_ip] = {
                                port: {'count' : count
                                }
                        }

        inFile.close()

        #print(connections)

        row_list = []
        outputFile = open(outFile, 'w') # newline=''
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(['Destination', 'Port', 'Conn Count'])

        row_count = 0

        if args.ip != None:
                ip = args.ip
                regex = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
                if not re.match(regex, ip):
                        print("*** ERROR *** " + ip + " is not a Valid IP address!")
                        sys.exit()
                else:
                        for dst_ip in connections:
                                for port in connections[dst_ip]:
                                        if ip == dst_ip:
                                                row_list = [dst_ip]
                                                row_list.append(port)
                                                row_list.append(connections[dst_ip][port]['count'])
                                                outputWriter.writerow(row_list)
                                                row_count = row_count + 1

                #print(full_csv_list)
        else:
                for dst_ip in connections:
                        for port in connections[dst_ip]:
                                row_list = [dst_ip]
                                row_list.append(port)
                                row_list.append(connections[dst_ip][port]['count'])
                                outputWriter.writerow(row_list)
                                row_count = row_count + 1

        outputFile.close()

        print('Completed!!!' + '\n' + 'Your file has ' + str(row_count) + ' results!' + '\n' 'Your output is in: ' + outFile)


if __name__ == '__main__':
        main()
