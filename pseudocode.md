## Overview
PCR duplicates in a SAM file are identical reads created during the amplfication step in library preparation.  
By comparing defining characteristics in a SAM file, they can be idenfitied and removed.

### duplicates have:
same alignment position as noted by chromosome, 5' start of read, strand  
same UMI

### Where elements are located:
chromosome number - column 3  
5' start of read - combines position from column 5 along with CIGAR info from column 6  
strand - column 2 (FLAG)  
UMI - column 1

### what to do:
UMIs will be checked against those in the STL96.txt file, and reads with unknown UMIs will be thrown out.  
Check to find read duplicates based on the criteria above, if all criteria match, keep only one


## Pseudocode:

Open the SAM file to read. Open new output file to write to. 
go through lines in read file
  
for header "@" lines: add to new file. these stay the same.
      
for data lines with read/alignment information:  
  strip and split on tabs as delimiter  
  check UMI against file  
    if it is unknown, skip
  
      
  



