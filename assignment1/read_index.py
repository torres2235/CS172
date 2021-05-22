# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import sys

if (sys.argv[1] == "--doc" and len(sys.argv) == 3):
    #print("this is a document")
    print("Listing for document: " + sys.argv[2])
elif (sys.argv[1] == "--term" and len(sys.argv) == 3):
    #print("this is a term")
    print("Listing for term: " + sys.argv[2])
else:
    print("ERROR: must provide a term or document")
