import re, string, timeit, StringIO
import cPickle as pickle
from DocumentStruct import *
from PorterStemmer import *


# ---------- Set up -------------
print("test")
f= open("cacm_copy.all","r")
rText = f.read()
title=""
abstract=""
documents=[]
reservedWords=[".I", ".T", ".W", ".A", ".K", ".C", ".N", ".X", ".B"]

# -------------   Stop words  ------------------
wantStopwordsRemoved = raw_input("Would you like to omit stopwords? If yes, type y. Otherwise, type n: ")
wantStemming = raw_input("Would you like to have stemming functionality? If yes, type y. Otherwise, type n: ")
if wantStopwordsRemoved == "y":
    f2 = open("stopwords.txt", "r")
    for stopWord in f2:
        #rText = rText.replace(stopWord, "")
        rText = re.sub(r"\b%s\b" % stopWord , "", rText)

    f2.close()

# 1.1
#-------------------- create list of document objects -----------------------
#split file into documents by delimeter '.I'
docs = rText.split('.I ')
numberOfDocuments = len(docs)

for doc in docs:
    #---init variables-- 
    allText = doc
    docFrequency={}

    #---- Get ID ----
    try:
        ID = re.search("^[0-9]+", doc.lstrip()).group(0)
    except AttributeError:
        ID = 'ERROR no ID found' 

    #--------- Get Author ---------
    author =""
    textIO = StringIO.StringIO(allText)
    for line in textIO:
        if line.startswith(".A"):
            run = True
            while(run):
                try:
                    nextLine = next(textIO)
                except:
                    run = False
                if not re.match("\.I|\.T|\.W|\.A|\.K|\.C|\.N|\.X|\.B" , nextLine):
                    author += nextLine
                else:
                    run = False
    author = author.strip()


    #--------- Get Title ---------
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

    rawTitle = title        

    # take out punctuation
    title = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', title).lower()
    title = re.sub('-', ' ', title).lower()

    #take stopwords out of title
    if wantStopwordsRemoved == "y":
        f2 = open("stopwords.txt", "r")
        stopwordsArray=[]
        for word in f2:
            stopwordsArray.append(word.strip())
        temp = ""
        for word in title.split():
            if word not in stopwordsArray:
                temp += word + " "
        title = temp

    # stem title
    if wantStemming == "y":
        p = PorterStemmer()
        output=""
        for word in title.split():
            output += p.stem(word, 0,len(word)-1) + " "
            #print(output)
        title = output
    #--------- End of getting Title ---------
    

    #------------ Get ABSTRACT --------------
    abstract =""
    textIO = StringIO.StringIO(allText)
    for line in textIO:
        if line.startswith(".W"):
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

    # take out punctuation from abstract
    abstract = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', abstract).lower()
    abstract = re.sub('-', ' ', abstract).lower()

    # take out stopwords from abstract
    if wantStopwordsRemoved == "y":
        f2 = open("stopwords.txt", "r")
        stopwordsArray=[]
        for word in f2:
            stopwordsArray.append(word.strip())
        temp = ""
        for word in abstract.split():
            if word not in stopwordsArray:
                temp += word + " "
        abstract = temp
        f2.close()

    # stem abstract
    if wantStemming == "y":
        p = PorterStemmer()
        output=""
        for word in abstract.split():
            output += p.stem(word, 0,len(word)-1) + " "
            #print(output)
        abstract = output
    #------------ End of getting abstract --------------

    #combine title and abstract
    titleAbstract = title + abstract
        

    #----------------------- Create Document -------------------------

    #create doc frequency dictionary initialized with all zero frequency
    for word in titleAbstract.split():
        docFrequency[word.strip()] = 0
    
    #document with text and initialized (all zero) dictionary of words
    document = DocumentStruct(allText, docFrequency, ID, title, rawTitle, author, abstract, titleAbstract, {})
    documents.append(document)

# ---------------------------------------------------------------------

# 1.2
#---------------------- Populate the Documents -------------------
ATAA = ""

# init document positions
for doc in documents:
    for word in doc.titleAbstract.split():
        doc.positions[word] = []

# get positions
for doc in documents:
    for idx, word in enumerate(doc.titleAbstract.split()):
        doc.positions[word].append(idx)

# get term frequency
for doc in documents:
    ATAA += doc.titleAbstract
    for idx, word in enumerate (doc.titleAbstract.split()):
        #doc.positions["accelerating"].append(0)
        if word not in reservedWords:
            doc.docFrequency[word.strip()] += 1



# 2.0
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
        if posting in doc.docFrequency.keys():
            docList.append(doc)
    postingsList[posting] = docList

# Print postings list file
print("PRINTING POSTING LIST ...")
postingsFile = open("postingsLists.txt", "w+")


for post in sorted(postingsList.keys()):
    if (post != ""):
        postingsFile.write(post+ ": ")
        #postingsFile.write("\r\n")
        for d in postingsList[post]:
            postingsFile.write("[ ID:" + str(d.ID) + " | ")
            postingsFile.write("Freq:" + str(d.docFrequency[post]) + " | Pos: ")
            for pos in d.positions[post]:
                postingsFile.write(str(pos) + ", ")

            postingsFile.write("], ")
        postingsFile.write("\r\n")
        postingsFile.write("\r\n")


# -------------------------------------------------------------------



# 3.0
#----------------------- CREATE DICTIONARY -------------------------------------

#init dictionary 3.1
print("Creating dictionary ...")
wordcount={}
for word in ATAA.split():
    if word not in reservedWords:
        wordcount[word.strip()] =0

# fill dictionary
for word in ATAA.split():
    if word not in reservedWords:
        wordcount[word.strip()] +=1

# 3.2
# write to dictionaty file. 
dicFile = open("dictionary.txt","w+")
for key in sorted(wordcount.keys()) :
    dicFile.write(key + " :: %d\r\n" % (wordcount[key]))
    #print(key , " :: " , wordcount[key])
dicFile.close
# -----------------------------------------------------------
