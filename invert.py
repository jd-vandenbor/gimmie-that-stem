import re, string, timeit, StringIO
import cPickle as pickle
from DocumentStruct import *
from TermInfo import *

#strip the text of punctuation
#stext = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', rawText)

# ---------- Set up -------------
print("test")
f= open("cacm.all","r")
rText = f.read()
#rText = "I w!ent. to the, do\"ct#o$+rs %t|&o\da()y. to:d;ay/<~@>=, to^da'y!kjbn"

title=""
abstract=""
#noStopWords=""
documents=[]

# -------------   Stop words  ------------------
wantStopwords = raw_input("Would you like to omit stopwords? If yes, type Y. Otherwise, type N: ")
wantStemming = raw_input("Would you like to have stemming functionality? If yes, type Y. Otherwise, type N: ")
if wantStopwords == "y" or "Y":
    f2 = open("stopwords.txt", "r")
    for stopWord in f2:
        rText.replace(stopWord, "")
    f2.close()

#-------------- Take out punctuation / lowercase ----------
reservedWords=[".I", ".T", ".W", ".A", ".K", ".C", ".N", ".X", ".B"]
# temp=""
# for word in rText:
#     if word not in reservedWords:
#         word = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|-|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', word).lower()
#     temp += word
# rText = temp

# 1.1
#-------------------- create list of document objects -----------------------

#split file into documents by delimeter '.I'
docs = rText.split('.I ')


for doc in docs:
    #---init variables-- 
    allText = doc
    docFrequency={}
    terms={}

    #---- Get ID ----
    try:
        ID = re.search("^[0-9]+", doc.lstrip()).group(0)
    except AttributeError:
        ID = 'ERROR no ID found' 

    #---- Get Title ----
    title =""
    textIO = StringIO.StringIO(allText)
    for line in textIO:
        if line.startswith(".T"):
            run = True
            title=""
            while(run):
                try:
                    nextLine = next(textIO)
                except:
                    run = False
                if not re.match("\.I|\.T|\.W|\.A|\.K|\.C|\.N|\.X|\.B" , nextLine):
                    title += nextLine
                else:
                    run = False
            #print("TITLE: " + title)
    title = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', title).lower()
    title = re.sub('-', ' ', title).lower()
    if wantStopwords == "y" or "Y":
        f2 = open("stopwords.txt", "r")
        for stopWord in f2:
            title.replace(stopWord, "")
        f2.close()

    #---- Get ABSTRACT ----
    abstract =""
    textIO = StringIO.StringIO(allText)
    for line in textIO:
        if line.startswith(".A"):
            run = True
            abstract=""
            while(run):
                try:
                    nextLine = next(textIO)
                except:
                    run = False
                if not re.match("\.I|\.T|\.W|\.A|\.K|\.C|\.N|\.X|\.B" , nextLine):
                    abstract += nextLine
                else:
                    run = False
            #print("ABSTRACT: " + abstract)
    abstract = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', abstract).lower()
    abstract = re.sub('-', ' ', abstract).lower()
    if wantStopwords == "y" or "Y":
        f2 = open("stopwords.txt", "r")
        for stopWord in f2:
            abstract.replace(stopWord, "")
        f2.close()

    titleAbstract = title + abstract
        

    #create document dictionary initialized with all zero frequency
    for word in titleAbstract.split():
        docFrequency[word.strip()] = 0
        term = TermInfo(word.strip(), 0)
        terms[word.strip()] = term
    

    #document with text and initialized (all zero) dictionary of words
    document = DocumentStruct(allText, terms, docFrequency, ID, title, abstract, titleAbstract)
    documents.append(document)

# ---------------------------------------------------------------------

# 1.2
#------ for each document get the frequency of all the words in the document----
ATAA = ""
f3 = open("docc.txt", "w+")
for doc in documents:
    f3.write(doc.ID + "\r\n")
    ATAA += doc.titleAbstract
    for idx, word in enumerate (doc.titleAbstract.split()):
        if word not in reservedWords:
            doc.docFrequency[word.strip()] += 1
            doc.terms[word.strip()].frequency += 1
            doc.terms[word.strip()].positions.append(idx)
f3.close()


#----------------------- Postings list ------------------------
#init postingsList
postingsList={}
for word in ATAA.split():
    postingsList[word.strip(string.punctuation)] = []

# Create posting list
print("CREATING POSTING LIST ...")
for posting in postingsList:
    docList=[]
    for doc in documents:
        #if the doc has the word append it to the list
        if posting in doc.titleAbstract:
            docList.append(doc.ID)
    postingsList[posting] = docList

# Print postings list file
print("PRINTING POSTING LIST ...")
postingsFile = open("postingsLists.txt", "w+")
for post in postingsList:
    if (post != ""):
        postingsFile.write(post+ ": " + str(postingsList[post]) + "\r\n")
    
# -------------------------------------------------------------------




#----------------------- CREATE DICTIONARY -------------------------------------
# 2.1
#init dictionary 
print("Creating dictionary ...")
wordcount={}
for word in ATAA.split():
    if word not in reservedWords:
        wordcount[word.strip()] =0

for word in ATAA.split():
    if word not in reservedWords:
        wordcount[word.strip()] +=1


# 2.2
# write to dictionaty file. 
dicFile = open("dictionary.txt","w+")
for key in sorted(wordcount.keys()) :
    dicFile.write(key + " :: %d\r\n" % (wordcount[key]))
    #print(key , " :: " , wordcount[key])
dicFile.close
# -----------------------------------------------------------

