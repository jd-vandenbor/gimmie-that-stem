import re, string, timeit
import cPickle as pickle
from DocumentStruct import *
from TermInfo import *


print("test")
f= open("cacm.all","r")
rText = f.read()
#rText = "I w!ent. to the, do\"ct#o$+rs %t|&o\da()y. to:d;ay/<~@>=, to^da'y!kjbn"

#strip the text of punctuation
#stext = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', rawText)

wantStopwords = raw_input("Would you like to omit stopwords? If yes, type Y. Otherwise, type N: ")
wantStemming = raw_input("Would you like to have stemming functionality? If yes, type Y. Otherwise, type N: ")


#split file into documents by delimeter '.I'
docs = rText.split('.I')


# 1.1
#-------------------- create list of document objects -----------------------
title=""
abstract=""
noStopWords=""
documents=[]
for doc in docs:
    allText = doc
    noStopWords = allText
    f2 = open("stopwords.txt", "r")
    for line in f2:
        stopWord = line
        if (wantStopwords == "Y" or wantStopwords == "y"):
            for line2 in noStopWords:

                if (line2.startswith(".T")):
                    title = next(noStopWords, '').strip().lower()
                    title = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', title)
                if (line2.startswith(".W")):
                    abstract = next(noStopWords, '').strip().lower()
                    abstract = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', abstract)
                for word in line2:
                    if (word == stopWord):
                        noStopWords.replace(word, "")
        else:
            for line2 in noStopWords:
                if (line2.startswith(".T")):
                    title = next(noStopWords).lower()
                    title = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', title)
                if (line2.startswith(".W")):
                    abstract = next(noStopWords).lower()
                    abstract = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', abstract)


    #inter = allText.trim()
    try:
        ID = re.search("^[0-9]+", doc.lstrip()).group(0)
    except AttributeError:
        ID = 'ERROR no ID found' 

    #print("ID: " + str(ID) + "\r\n")
    docFrequency={}
    terms={}
    #create document dictionary initialized with all zero frequency
    for word in noStopWords.split():
        docFrequency[word.strip(string.punctuation)] = 0
        term = TermInfo(word.strip(string.punctuation), 0)
        terms[word.strip(string.punctuation)] = term
    

    #document with text and initialized (all zero) dictionary of words
    document = DocumentStruct(allText, terms, docFrequency, ID, title, abstract, noStopWords)
    documents.append(document)

temp=""
for doc in documents:
    temp += doc.noStopWords + "\r\n"
noStopWords = noStopWords.lower()
noStopWords = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', noStopWords)

# ---------------------------------------------------------------------

# 1.2
#------ for each document get the frequency of all the words in the document----
for doc in documents:
    #add boolean
    for idx, word in enumerate (doc.noStopWords.split()):
        doc.docFrequency[word.strip(string.punctuation)] += 1
        doc.terms[word.strip(string.punctuation)].frequency += 1
        doc.terms[word.strip(string.punctuation)].positions.append(idx)
        #temp = doc.terms[word.strip(string.punctuation)]
        #temp.frequency += 1
        #temp.positions.append(idx)
        #doc.terms[word.strip(string.punctuation)] = temp

postingsList={}
#init postingsList
for word in noStopWords.split():
    postingsList[word.strip(string.punctuation)] = []

for posting in postingsList:
    docList=[]
    for doc in documents:
        #if the doc has the word append it to the list
        if posting in doc.noStopWords:
            print(doc.ID)
            docList.append(doc.ID)
    postingsList[posting] = docList

postingsFile = open("postingsLists.txt", "w+")
for post in postingsList:
    postingsFile.write(post+ ": " + str(postingsList[post]) + "\r\n")
    






# for doc in documents:
#     postingsFile.write(doc.ID + "\r\n")
#     for term in doc.terms:
#         postingsFile.write(str(doc.terms[term].frequency))
    
#------------------------------------------------------------------------------


# 2.1
#------- get the frequency of words in ALL documents --------
#------------------------ Output 2 --------------------------
wordcount={}
for word in noStopWords.split():
        wordcount[word.strip(string.punctuation)] = 0
for word in noStopWords.split():
    wordcount[word.strip(string.punctuation)] += 1

# 2.2
# write to dictionaty file. 
dicFile = open("dictionary.txt","w+")
for key in sorted(wordcount.keys()) :
    dicFile.write(key + " :: %d\r\n" % (wordcount[key]))
    #print(key , " :: " , wordcount[key])

# -----------------------------------------------------------


dicFile.close

print(noStopWords)