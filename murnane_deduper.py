#!/usr/bin/env python

import argparse
import re

#argparse
def get_args():
    parser = argparse.ArgumentParser(description="to deduplicate single-ended reads given a SAM file of uniquely mapped reads and a file with a list of UMIs")
    parser.add_argument("-f", "--input_file", help="designates file to sorted sam file", type=str, required=True)
    parser.add_argument("-o", "--output_file", help="designates file to deduplicated sam file", type=str, required=True)
    parser.add_argument("-u", "--umi_file", help="designates file containing the list of UMIs", type=str, required=True)
    return parser.parse_args()

args = get_args()

#bringing in files from the argparse
input_file = args.input_file
output_file = args.output_file
umi_file = args.umi_file

#make set of known umis by pulling from file
umi_set = set()
with open(umi_file, 'r') as open_umi:
    for line in open_umi:
        line=line.strip()
        umi_set.add(line)

#defining function for getting strand of the read from the FLAG
def get_strand(flag):
    if (int(flag) & 16) == 16:
        this_strand = '-'
    else:
        this_strand = '+'
    return this_strand

#make additional funtion to help sort through cigar strings for rev strands so I don't go crazy
def sort_rev_cigar(cigar):
    modifier = 0
    while len(cigar) > 0:
        chunk = re.search(r"^(\d+[A-Z])",cigar).group(0)
        chunk_len = len(chunk)
        cigar = cigar[chunk_len:]
        
        if "S" in chunk and len(cigar)>0:
            modifier+=0
            
        elif "I" in chunk:
            modifier+=0
            
        else:
            chunk_num = chunk[:-1]
            modifier += int(chunk_num)
    
    return modifier


#defining function for getting the 5' read start
def get_read_start(position, cigar, strand):
    position = int(position)
    if strand == '+':
        soft_clip = re.search(r"^(\d+)(S)",cigar)
        modifier = 0
        
        if soft_clip:
            modifier = int(soft_clip.group(1))

        new_start  = position - modifier
            
    
    else:
        modifier = sort_rev_cigar(cigar)
        new_start = position + modifier


    return new_start


#initialize set for seen read info for detecting duplicates
read_tracker = set()


#make last chromosome tracker to know when to empty values
last_chromosome = None


#making counters for things to track: header lines, unique reads, wrong umis, duplicates removed
header_lines = 0
unique_reads = 0
wrong_umis = 0
duplicates_removed = 0


with open(input_file, 'r') as open_input_file, open(output_file, 'w') as open_output_file: 
    for line in open_input_file: #reading through the input file
        line = line.strip()
        split_line = line.split("\t") #split each line on tabs

        #copy over header lines to new file
        if split_line[0][0] == '@':
            print(line, file = open_output_file)
            header_lines += 1
            continue
        
        #start grabbing the current umi and make sure it is known. if not, get rid of the read
        current_umi = split_line[0][-8:]


        if current_umi not in umi_set:
            #print(current_umi)
            wrong_umis += 1
            continue

        #in order to check duplicates, in addition to umi also need chromosome, strand, and 5' start 
        
        #get chromosome
        current_chromosome = split_line[2]

        #get strand
        current_flag = split_line[1]
        current_strand = get_strand(current_flag)

        #get 5' start
        current_position = split_line[3]
        current_cigar = split_line[5]
        current_start = get_read_start(current_position, current_cigar, current_strand)


        #make a tuple for the read values to keep track of duplicates
        read_values = (current_umi, current_strand, current_start)
        

        #clear the tracked values if we are now reading a new chromosome.
        if current_chromosome != last_chromosome:
            read_tracker.clear()
    

        #check to see if values are seen already
        if read_values in read_tracker:
            duplicates_removed += 1
            continue
        else:
            read_tracker.add(read_values)
            print(line, file = open_output_file)
            unique_reads += 1

        #reset the last chromosome to the current one
        last_chromosome = current_chromosome



#printing out summary stats
with open('deduper_stats.txt', 'w') as stats_file:

    print(f'header lines: {header_lines}', file = stats_file)
    print(f'unique reads: {unique_reads}', file = stats_file)
    print(f'wrong umis: {wrong_umis}', file = stats_file)
    print(f'duplicates removed: {duplicates_removed}', file = stats_file)




        #where do i want to add the periodical empytying of the read checker??
       

        #double check that line column numbers are correct for each piece of information
        #double check flag fxn
