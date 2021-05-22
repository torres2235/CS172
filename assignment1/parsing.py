import re
import os
import zipfile
from io import open # needed to add to get "encoding='ISO-8859-1'" to work

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

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

#--------------------- Creating some Globals -----------------------------------#
words = [] # holds the words in our doc without stopwords
#tokens = [] # holds our tuples

termindex = 1
docindex = 1
TermIds = dict() # holds our terms and TermIds
DocIds = dict() # holds our docnos and DocIds
posting_dictionary = dict() # comnbines our TermIds and DocIds and uses our terms as keys
#-------------------------------------------------------------------------------#

#--------------------------------.txt prep -------------------------------------#
docids_file = open("docids.txt", "w")
docids_file.write("") # reset our file
docids_file.close()
docids_file = open("docids.txt", "a") # put our file into append mode

termids_file = open("termids.txt", "w")
termids_file.write("") # reset our file
termids_file.close()
termids_file = open("termids.txt", "a") # put our file into append mode
#-------------------------------------------------------------------------------#
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

 #-------------------------- step 1 - lower-case words, remove punctuation, remove stop-words, etc. --------------------------#
            pattern = re.compile('[\.?\w\'-]+') # use our regex (updated to handle ' and -)

            lwr_case = text.lower() # lower-case our words

            words = pattern.findall(str(lwr_case)) # tokenize words and put into list
            #print(words)

            for line in stopwords_list: #remove stopwords from our tokens
                while line in words: words.remove(line)
            #print(words)

#-------------------------- step 2 - create tokens --------------------------#
            
            if docno not in DocIds:
                DocIds[docno] = str(docindex)
                docids_file.write(str(docindex) + "\t" + docno + "\n") # add docid and docno into our .txt
            #docids_file.close()
            #print(DocIds)

            for index, word in enumerate(words):
                if word not in TermIds:
                    TermIds[word] = termindex # add word into terms if it is unique
                    termids_file.write(str(termindex) + "\t" + word + "\n") # add termid and term into our .txt
                    posting_dictionary[word] = [] # make a new space in our posting_dictionary so we can append to it
                    termindex += 1

                tmp = (TermIds[word], DocIds[docno], index + 1)
                if TermIds[word] not in posting_dictionary:   
                    posting_dictionary[word].append(tmp) # create the tuple

            docindex += 1
            #print(DocIds[docno])
print(posting_dictionary)
#-------------------------- step 3 - build index --------------------------#
