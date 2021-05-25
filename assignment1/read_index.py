import sys
import linecache

if len(sys.argv) < 3:
    print("ERROR: Invalid term/document")
    sys.exit()

#---------------------------- Load our termids.txt, docids.txt, doclengths.txt, and termindex.txt --------------------------------#
term_ids = open('termids.txt', 'r')
term_ids_map = dict()

for line in term_ids:
    split_array = line.split()
    term_ids_map[split_array[1]] = split_array[0]
# print(term_ids_map)
term_ids.close()

doc_ids = open('docids.txt', 'r')
doc_ids_map = dict()

for line in doc_ids:
    split_array = line.split()
    doc_ids_map[split_array[1]] = split_array[0]
# print(doc_ids_map)
doc_ids.close()

doc_lengths = open('doclengths.txt', 'r')
doc_lengths_map = dict()

for line in doc_lengths:
    split_array = line.split()
    doc_lengths_map[split_array[0]] = split_array[1]

# print(doc_lengths_map)
doc_lengths.close()

term_index = open('term_index.txt', 'r')
#------------------------------------------------------------------------------#

# Process query
if len(sys.argv) < 4:
    if sys.argv[1] == '--doc':
        try:
            doc = doc_ids_map[sys.argv[2]]
        except:
            print("ERROR: Invlaid document")
            sys.exit()

        print("Listing for document: " + str(sys.argv[2]))
        print("DOCID: " + str(doc))
        print("Total terms: " + str(doc_lengths_map[doc]))
    elif sys.argv[1] == '--term':
        try:
            term = term_ids_map[sys.argv[2]]
        except:
            print("ERROR: Invlaid term")
            sys.exit()
            
        term_info = linecache.getline('term_info.txt', int(term))
        term_info = term_info.split()

        # print(split_posting)

        print("Listing for term: " + str(sys.argv[2]))
        print("TERMID: " + str(term))
        print("Number of documents containing term: " + str(term_info[3]))
        print("Term frequency in corpus: " + str(term_info[2]))
else:
    try:
        term = term_ids_map[sys.argv[2]]
        doc = doc_ids_map[sys.argv[4]]
    except:
        print("ERROR: Invalid arguements. Try format read_index.py --term <TERM> --doc <DOCNAME>")
        sys.exit()
  
    print("Inverted list for term: " + str(sys.argv[2]))
    print("In document: " + str(sys.argv[4]))

    # Grab stats from posting file
    term_info = linecache.getline('term_info.txt', int(term))
    term_info = term_info.split()
    #print(term_info)

    term_index.seek(int(term_info[1]))
    #print(term_index.tell())

    #print(term_index.readline())

    if int(term) != 1:
        term_index.readline() # i have to read the line twice for some reason unless its the first termid (???) i really wish i knew why  

    posting = term_index.readline()
    #print(posting)

    term_index.close()
    split_posting = posting.split()[1:]
    positions = []

    #print(split_posting)

    for posting in split_posting:
        #print(posting)

        posting_arr = posting.split(':')

        #print(posting_arr)
        #print(doc)

        if posting_arr[0] == str(doc):
            positions.append(posting_arr[1])

    print("TERMID: " + term)
    print("DOCID: " + doc)
    print("Term frequency in document: " + str(len(positions)))
    print("Positions: " + ", ".join(positions))
