# Introduction
A simple tool to add a clickable table of contents to a PDF document. The intended use case is to copy-paste the existing table of contents
into a text file, edit it to the correct format, and write it to the PDF.

# Requirements
Python 3.x. `pdftk` in your PATH.

# Usage
If you want to write a table of contents from `contents.txt` to `book.pdf` with offset 10:
```
python3 contents.py book.pdf contents.txt --offset 10
```
The updated book will be `final.pdf`.

# Table of contents file format
The textual table of contents (copied from a real book) might look like this:
```
0 Introduction                                                            1
    0.1 Automata, Computability, and Complexity . . . . . . . . . . . . . 1
        Complexity theory . . . . . . . . . . . . . . . . . . . . . . . . 2
        Computability theory  . . . . . . . . . . . . . . . . . . . . . . 3
        Automata theory . . . . . . . . . . . . . . . . . . . . . . . . . 3
    0.2 Mathematical Notions and Terminology  . . . . . . . . . . . . . . 3
        Sets  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
        Sequences and tuples  . . . . . . . . . . . . . . . . . . . . . . 6
        Functions and relations . . . . . . . . . . . . . . . . . . . . . 7
```

Your table of contents file should look like this:
```
0 Introduction 1
    0.1 Automata, Computability, and Complexity 1
        Complexity theory 2
        Computability theory 3
        Automata theory 3
    0.2 Mathematical Notions and Terminology 3
        Sets 3
        Sequences and tuples 6
        Functions and relations 7
```
Each line must finish with a positive integer. Numbers at the start of the line have no significance. Indents are done with four spaces
and determine the contents hierarchy.

Your book probably has an offset between page 1 on the internal page numbers and page 1 of the PDF. Scroll your book to page 1, note the PDF
page number, and pass this as the `--offset` argument.