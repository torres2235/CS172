# CS172 - Assignment 2 (Retrival)

## Team member 1 - Joshua Torres

###### Provide a short explanation of your design
Design makes use of dictionaries to help us store our doc. names/ docIds, terms/TermIds, and our posting dictionary. Regex used is
 "r'\w+(?:\.?\w+)*'" to help parse out punctiation, and keep words with ' and - together. Tuples of (termId, docId, position) are stored
 within my "posting_dictionary". 

VSM.py uses similar methods as read_index.py to help read and compare the documents to the queries
Queries are tested using your choice of query
Queries are organized in to a dictionary w/ the leading number acting as the key for access
Cosine similarity is displayed to the user as output and equals 0 if there are no query terms in the document
Stopwords have been removed from the query as they will not be in the term corpus

###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 
Coded using Python 3

Run using "python parse.py" to create the .txts
Run read_index.py using this format: read_index.py --term <TERM> | read_index.py --doc <DOCNAME> | read_index.py --term <TERM> --doc <DOCNAME>
Run VSM.py using this format: python VSM.py <query-file> <query-id> <DOCNAME>
-- example: python .\VSM.py query_list.txt 85 AP890128-0031

Used binary term weights instead of TF-IDF
Did partial credit version of the assignment