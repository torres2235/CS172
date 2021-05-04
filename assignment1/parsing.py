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

#-----------------------Generating my stopwords here--------------------------#

stopwords_list = []
with open('stopwords.txt', 'r') as stopwords:
    for line in stopwords:
        line = re.sub('\n',"", line)
        #print(line)
        stopwords_list.append(str(line))
#print stopwords_list

words = [] # holds the words in our doc without stopwords
tokens = [] # holds our tuples
terms = [] # holds our terms and the index for them is our TermId(?)
doc_num = [] # holds our docnos, the index for them is our DocId(?)
#--------------------------------------------------------------------#

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
            if docno not in doc_num:
                doc_num.append(docno)
            #print doc_num.index(docno)
            
            for word in words:
                if word not in terms:
                    terms.append(word) # add word into terms if it is unique
                tmp = (terms.index(word) + 1, "DocID: " + str(doc_num.index(docno) + 1), words.index(word) + 1)
                if tmp not in tokens:
                    tokens.append(tmp) # create the tuple
            #print(tokens)
            #print terms
#-------------------------- step 3 - build index --------------------------#
TermId = []
DocId = []

for word in terms:
    tmp = (terms.index(word) + "  " + word)
    TermId.append(tmp)
    
for doc in doc_num:
    tmp = (doc_num.index(doc) + "  " + doc)
    DocId.append(tmp)
    
print TermId
print DocId
