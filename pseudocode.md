## Overview
PCR duplicates in a SAM file are identical reads created during the amplfication step in library preparation.  
By comparing defining characteristics in a SAM file, they can be idenfitied and removed.

### duplicates have:
same alignment position as noted by chromosome, 5' start of read, strand  
same UMI

### where elements are located:
chromosome number - column 3  
5' start of read - combines position from column 5 along with CIGAR info from column 6  
strand - column 2 (FLAG)  
UMI - column 1

### what to do:
UMIs will be checked against those in the STL96.txt file, and reads with unknown UMIs will be thrown out.  
Check to find read duplicates based on the criteria above, if all criteria match, keep only one

## Examples located [HERE](example_files)
#### for examples (8 total):
original,
duplicate,
unknown UMI,
different but known UMI,
different chromosome,
different 5' start(pos and cigar),
different strand


## Pseudocode:
samtools sort the file to make it easier to navigate as potential duplicates will be sequential

make an empty variable to hold the information of the previous read so that reads can be compared

Open the SAM file to read. Open new output file to write to. 
go through lines in read file
  
if header "@" lines: add to the new file. these stay the same.

for data lines with read/alignment information:  
  strip and split on tabs as delimiter. save to a list to make it accessible.  
  -save UMI (last characters of column 1)  
  -get chromosome number (column 3) as variable  
  -calculate/get 5' start (use function with info from 5 and 6) as a variable    
  -detect strand (use function on column 2), can also save as variable  

  save these 4 pieces to a new list for this read

  check to see if the current read list matches the previous read list. only add to new file if it does NOT match AND the UMI is in the known file.

  update the previous read list to the new read list
  
## functions:

This function calculates the 5' start for reads using the POS and CIGAR:  
get_read_start(position (int), CIGAR (str)) -> int:  
return 5' start  
example get_read_start(10,5M) -> 10

This function determines strand using FLAG:  
get_strand(FLAG (int) ) -> str:  
return +/-  
example get_strand(0) -> +
  



  
      
  








