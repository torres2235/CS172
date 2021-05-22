# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import sys
import re

if (sys.argv[1] == "--doc" and len(sys.argv) == 3):
    #print("this is a document")
    print("Listing for document: " + sys.argv[2])
elif (sys.argv[1] == "--term" and len(sys.argv) == 3):
    #print("this is a term")
    print("Listing for term: " + sys.argv[2])

    termids_file = "termids.txt"

    with open(termids_file) as f:
        content = f.read().splitlines()

    for line in content:
        new_line = re.sub(r'\d+''\t+','',line) #remove the termid and \t so we can compare it to the term we are trying to find
        #print(new_line)
        if new_line == sys.argv[2]:
            new_line = re.sub(r"[a-z]",'',line)
            #print(line)
            print("TERMID: " + new_line)
else:
    print("ERROR: must provide a term or document")
