import re
import os
import zipfile
import string
import sys
import linecache
import math

if len(sys.argv) != 4:
    print("ERROR: Invalid query")
    print("Use format 'python VSM.py <query-file> <query-id> <DOCNAME>' ")
    sys.exit()

query_file = sys.argv[1]

if os.path.isfile(query_file) == True: # check if the entered query file exists
    query_list = open(query_file, 'r')
else:
    print("ERROR: Invalid query file")
    sys.exit()

#---------------------------- Load our termids.txt, docids.txt --------------------------------#
term_ids = open('termids.txt', 'r')
term_ids_map = dict()

for line in term_ids:
    split_array = line.split()
    term_ids_map[split_array[1]] = split_array[0]

term_ids.close()

# Load docids.txt
doc_ids = open('docids.txt', 'r')
doc_ids_map = dict()

for line in doc_ids:
    split_array = line.split()
    doc_ids_map[split_array[1]] = split_array[0]

doc_ids.close()
#------------------------------------------------------------------------------#

#----------------------- Generating my stopwords here --------------------------#

stopwords_list = []
with open('stopwords.txt', 'r') as stopwords:
    for line in stopwords:
        line = re.sub('\n',"", line)
        #print(line)
        stopwords_list.append(str(line))
stopwords.close()
#print stopwords_list
#-------------------------------------------------------------------------------#

#---------------------------- Load our query --------------------------------#
query_list_map = dict()

for line in query_list:

    lwr_case = line.lower().strip().rstrip('.').replace(',', '').replace('"', '') # make query lower case and remove ',', '"', and ending '.'

    split_array = lwr_case.split()
    QID = int(split_array[0].replace('.', '')) # make the leading number our key (and remove the '.')

    del split_array[0] # delete leading numbner
    # print(split_array)

    for line in stopwords_list: #remove stopwords from our query
        while line in split_array: split_array.remove(line)

    query_list_map[QID] = []

    for i in split_array:
        query_list_map[QID].append(i)

#print(query_list_map)

query_list.close()
#------------------------------------------------------------------------------#

#----------------------- Checking if args are valid ---------------------------#
QID = int(sys.argv[2]) # get the QID
docno = sys.argv[3] # get the document

if QID not in query_list_map: # check if QID is in our query map
    print("ERROR: QID invalid")
    print("QID must be: 85, 77, 87, 94, 100, 89, 95, 98, or 91")
    sys.exit()

try: # check if docno is in valid
    docno = doc_ids_map[sys.argv[3]]
except:
    print("ERROR: Invlaid document")
    sys.exit()

print("DOCNO: " + docno)

print("Query is: " + str(query_list_map[QID]))

q_binary_weights = len(query_list_map[QID]) # binary weight of query is the length of the query
#------------------------------------------------------------------------------#

doc_binary_weights = 0 # initalize binary weights for the document


#----------------------- Comparing the query terms to our document ---------------------------#
term_index = open('term_index.txt', 'r') # Open term_index.txt

for term in query_list_map[QID]:
    #print(term)
    term = term_ids_map.get(term)

    if term:
        term_info = linecache.getline('term_info.txt', int(term))
        term_info = term_info.split()
        term_index.seek(int(term_info[1]))

        if int(term) != 1:
            term_index.readline() # i have to read the line twice for some reason unless its the first termid (???) i really wish i knew why  

        posting = term_index.readline()
        split_posting = posting.split()[1:]

        flag = 0 # keeps track of if we have found the term at least once

        for posting in split_posting:
            posting_arr = posting.split(':')
            #print(posting_arr)

            if posting_arr[0] == str(docno):
                flag += 1 # find match and trip flag

        if flag > 0: # increment our weights if we find at least 1 match
            doc_binary_weights += 1

term_index.close()
#print(doc_binary_weights)
#------------------------------------------------------------------------------#

#-----------------------------Compute Cosine Similarity------------------------------#
## NOTE since we are using binary weights, the dot product of (q_binary_weights, doc_binary_weights) = doc_binary_weights
mag_q = math.sqrt(q_binary_weights) # magnitude of q
mag_doc = math.sqrt(doc_binary_weights) # magnitude of doc

magnitudes = (mag_q * mag_doc)

if magnitudes == 0:
    print("The cosine similarity of documment " + str(docno) + " and the query " + str(QID) + " is 0" ) # accounting for zero in the denominator of the cosine-sim function
else:
    cosine_similarity = doc_binary_weights / magnitudes
    print("The cosine similarity of documment " + str(docno) + " and the query " + str(QID) + " is " + str(cosine_similarity))
#------------------------------------------------------------------------------#