# **PCR Duplicate Removal Tool (UMI‑Aware, Single‑End)**
### **Author:** Ryan Murnane
### **Script:** `murnane_deduper.py`
### **Python Version:** **3.12**

---

## **Overview**
This repository contains a Python-based tool for **reference-based PCR duplicate removal** for **single-end sequencing reads** containing **known UMIs** in the read name (QNAME). The tool operates on **coordinate‑sorted SAM files of uniquely mapped reads**, identifies duplicate reads using genomic position, strand, and UMI, and outputs a **properly formatted deduplicated SAM file**.

The workflow is fully **streamed**, meaning the script never loads the entire SAM file into memory. This enables efficient handling of **millions of reads**.

---

## **What This Tool Does**
- Performs **PCR duplicate removal using UMIs**
- Computes **5′ genomic position** accurately using:
  - Strand (+ / –)
  - All CIGAR operations
  - Proper handling of **soft clipping**
- Uses **known UMIs** provided via a whitelist file
- Supports **single-end reads** (paired-end optional in a challenge branch)
- Keeps the **first read encountered** when duplicates are found
- Streams input for **low memory usage**
- Outputs a valid, fully formatted **SAM file**

---

## **How Duplicate Reads Are Identified**
Two reads are considered duplicates if they share:

1. **Chromosome (RNAME)**
2. **Strand** (FLAG bit 0x10)
3. **5′ Genomic Position**
   - `+` strand: `POS`
   - `–` strand: `POS + reference_consuming_length - 1`
4. **UMI** extracted from QNAME

Reads with UMIs not in the whitelist are **discarded** unless error correction is implemented in an optional branch.

---

## **Input Requirements**
- **Sorted SAM file**
  ```bash
  samtools sort -o input.sorted.sam input.sam
  ```
- **UMI whitelist** (96 known UMIs)
- **Single-end uniquely mapped reads**

Reads marked unmapped (0x4), secondary (0x100), or supplementary (0x800) are ignored.

---

## **Output**
- A **valid SAM file**
- Header lines copied exactly
- Only **non-duplicate** alignments written
- **First read preserved** when duplicates exist

---

## **Command Line Usage**
```
-f, --file        Path to sorted SAM file
-o, --outfile     Path for deduplicated SAM output
-u, --umi         Path to known UMI whitelist
-h, --help        Displays help message
```

### **Example command:**
```bash
./<your_last_name>_deduper.py -u STL96.txt -f input.sorted.sam -o output.deduped.sam
```

---

## **UMI Extraction Format**
Example QNAME:
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT
```
Extracted UMI:
```
GAACAGGT
```

---

## **Algorithm Summary**
1. Load UMI whitelist
2. Stream SAM file line‑by‑line
3. Write all header lines to output
4. Skip unmapped, secondary, or supplementary reads
5. Extract UMI and validate
6. Determine read strand using FLAG
7. Compute 5′ genomic position using CIGAR
8. Build deduplication key:
   ```
   (RNAME, five_prime_position, strand, UMI)
   ```
9. If key not seen → **write read**, store key
10. If key seen → **discard duplicate**
11. When chromosome changes, clear stored keys

---

## **File Structure**
```
Deduper-<github-user-name>/
│
├── <your_last_name>_deduper.py
├── README.md
├── data/
│   ├── umi_whitelist.txt
│   ├── example_input.sorted.sam
│   └── example_output.sam
└── tests/
    └── unit_tests.md
```

---

## **Challenge Branch (Optional Enhancements)**
- Paired-end deduplication
- Randomer UMI support
- UMI error correction
- Duplicate retention policy options

---

## **Limitations**
- Only **single-end** reads supported in the main version
- Requires **pre-sorted SAM**
- UMIs must be known unless optional mode is used

---

## **Summary**
This tool provides an efficient and accurate approach for removing PCR duplicates based on UMIs in single-end sequencing data. It is:
- **Memory efficient**
- **Deterministic (first-read kept)**
- **CIGAR-aware**
- **UMI-aware**
- Fully compatible with **Python 3.12** and **argparse**

Ideal for integration into sequencing analysis workflows.






# Deduper

## Part 1
Use this repo template to create your own Deduper repo - you should do all your work in your own repository. Please name it `Deduper-<github-user-name>`.

Write up a strategy for writing a Reference Based PCR Duplicate Removal tool. That is, given a sorted sam file of uniquely mapped reads, remove all PCR duplicates (retain only a single copy of each read). Develop a strategy that avoids loading everything into memory. You should not write any code for this portion of the assignment. Be sure to:
- Define the problem
- Write examples:
    - Include a properly formated sorted input sam file
    - Include a properly formated expected output sam file
- Develop your algorithm using pseudocode
- Determine high level functions
    - Description
    - Function headers
    - Test examples (for individual functions)
    - Return statement
    
For this portion of the assignment, you should design your algorithm for single-end data, with 96 UMIs. UMI information will be in the QNAME, like so: ```NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT```. Discard any UMIs with errors (or think about how you might error correct, if you're feeling ambitious).

## Part 2
An important part of writing code is reviewing code - both your own and other's. In this portion of the assignment, you will be assigned 3 students' pseudocode algorithms to review. Be sure to evaluate the following points:
- Does the proposed algorithm make sense to you? Can you follow the logic?
- Does the algorithm do everything it's supposed to do? (see part 1)
- Are proposed functions reasonable? Are they "standalone" pieces of code?

You can find your assigned reviewees on Canvas. You can find your fellow students' repositories at 
```
github.com/<user>/Deduper-<github-user-name>
```
Be sure to leave comments on their repositories by creating issues or by commenting on the pull request.

## Part 3
Write your deduper function!

Given a SAM file of uniquely mapped reads, and a text file containing the known UMIs, remove all PCR duplicates (retain only a single copy of each read). Remember:
- Your Python code can assume a sorted sam file (you *might* need to use `samtools sort` outside of your Python script)
- Account for: 
    - all possible CIGAR strings (including adjusting for soft clipping, etc.)
    - Strand
    - Single-end reads
    - Known UMIs
- Considerations:
    - Millions of reads – avoid loading everything into memory!
    - Be sure to utilize functions appropriately
    - Appropriately comment code and include doc strings
- **CHALLENGE**: In a **separate branch**, implement options for
    - Single-end vs paired-end
    - Known UMIs vs randomers
    - Error correction of known UMIs
    - Choice of duplicate written to file
    
You MUST:
- Write Python 3.12 compatible code
- Include the following argparse options
    - ```-f```, ```--file```: designates absolute file path to sorted sam file
    - ```-o```, ```--outfile```: designates absolute file path to deduplicated sam file
    - ```-u```, ```--umi```: designates file containing the list of UMIs
    - ```-h```, ```--help```: prints a USEFUL help message (see argparse docs)
        - That is, your code must be able to run (in a single step) if given a command in the format:
          ```
          ./<your_last_name>_deduper.py -u STL96.txt -f <in.sam> -o <out.sam>
          ```
- Output the first read encountered if duplicates are found
- Output a properly formatted SAM file
- Name your python script ```<your_last_name>_deduper.py``` and place it in the top level of your repo (that is, not inside a folder)

