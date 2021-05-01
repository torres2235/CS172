import re
import os
import zipfile

import array

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
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

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 

            pattern = re.compile('\w+(\.?[\w\'-]+)*') # use our regex (updated to handle ' and -)

            lwr_case = text.lower() # lower-case our words

            #sample_string = "bob, Bob, BOB, 376, 98.6, 192.160.0.1, test's, another-test"
            #lwr_sample = sample_string.lower()

            matches = pattern.finditer(lwr_case)
            #matches = pattern.finditer(lwr_sample)

            new_array = []

            for match in matches:
                if (new_array.count(match) < 1):
                    new_array.append(match)
     
            print(new_array)

            
            # step 2 - create tokens 
            # step 3 - build index
            