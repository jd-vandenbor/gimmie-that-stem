import re, string, timeit
import cPickle as pickle
from DocumentStruct import *

print("test")
f= open("cacm.all","r")
rText = f.read()
#rText = "I w!ent. to the, do\"ct#o$+rs %t|&o\da()y. to:d;ay/<~@>=, to^da'y!kjbn"

#strip the text of punctuation
#stext = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', rawText)


#split file into documents by delimeter '.I'
docs = rText.split('.I')


# 1.1
#-------------------- create list of document objects -----------------------
documents=[]
for doc in docs:
    allText = doc
    #inter = allText.trim()
    try:
        ID = re.search("^[0-9]+", doc.lstrip()).group(0)
    except AttributeError:
        ID = 'ERROR no ID found' 

    #print("ID: " + str(ID) + "\r\n")
    docFrequency={}
    #create document dictionary initialized with all zero frequency
    for word in doc.split():
        docFrequency[word.strip(string.punctuation)] = 0

    #document with text and initialized (all zero) dictionary of words
    document = DocumentStruct(allText, docFrequency, ID)
    documents.append(document)
# ---------------------------------------------------------------------

# 1.2
#------ for each document get the frequency of all the words in the document----
for doc in documents:
    for word in doc.allText.split():
        doc.docFrequency[word.strip(string.punctuation)] += 1


# 1.3 - PRINT DOCUMENT
postingsFile = open("postingsLists.txt","w+")
for doc in documents:
    postingsFile.write(doc.ID + "\r\n")
    postingsFile.write("dictionary goes here" + "\r\n")
    
#------------------------------------------------------------------------------


# 2.1
#------- get the frequency of words in ALL documents --------
#------------------------ Output 2 --------------------------
wordcount={}
for word in rText.split():
        wordcount[word.strip(string.punctuation)] = 0
for word in rText.split():
    wordcount[word.strip(string.punctuation)] += 1

# 2.2
# write to dictionaty file. 
dicFile = open("dictionary.txt","w+")
for key in sorted(wordcount.keys()) :
    dicFile.write(key + " :: %d\r\n" % (wordcount[key]))
    #print(key , " :: " , wordcount[key])

# -----------------------------------------------------------


dicFile.close

