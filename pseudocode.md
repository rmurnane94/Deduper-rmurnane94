##Overview
PCR duplicates in a SAM file are identical reads created during the amplfication step in library preparation. 
By looking at defining characteristics in a SAM file, they can be idenfitied and removed.
Here multiple elements in the data lines of SAM files will be compared to do this.

###<u>duplicates have</u>:
same alignment position as noted by chromosome, 5' start of read, strand
same UMI

###<u>Where elements are located</u>:
chromosome number is found in the 3rd column
5' start of read combines position from column 5

Known UMIs will be taken from the STL96.txt file, and unknown ones will be thrown out.
