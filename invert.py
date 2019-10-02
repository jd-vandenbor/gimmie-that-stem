import re, string, timeit, StringIO
import cPickle as pickle
from DocumentStruct import *
from TermInfo import *
from PorterStemmer import *


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
wantStopwordsRemoved = raw_input("Would you like to omit stopwords? If yes, type Y. Otherwise, type N: ")
wantStemming = raw_input("Would you like to have stemming functionality? If yes, type Y. Otherwise, type N: ")
if wantStopwordsRemoved == "y":
    f2 = open("stopwords.txt", "r")
    for stopWord in f2:
        #rText = rText.replace(stopWord, "")
        rText = re.sub(r"\b%s\b" % stopWord , "", rText)

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
    # take out punctuation
    title = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', title).lower()
    title = re.sub('-', ' ', title).lower()
    # take out stopwords
    # if wantStopwordsRemoved == "y":
    #     f2 = open("stopwords.txt", "r")
    #     for stopWord in f2:
    #         #title = title.replace(stopWord.strip(), "")
    #         title = re.sub(r"%s" % stopWord , "", title)
    #     f2.close()
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

    #stem it
    if wantStemming == "y":
        p = PorterStemmer()
        output=""
        for word in title.split():
            output += p.stem(word, 0,len(word)-1) + " "
            #print(output)
        title = output
    
    

    #---- Get ABSTRACT ----
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
            #print("ABSTRACT: " + abstract)
    # take out punctuation
    abstract = re.sub('!|"|#|\\$|%|&|\'|\\(|\\)|\\*|\\+|,|\\.|/|:|;|<|=|>|\\?|@|\\[|]|\\^|_|`|\\{|}|~|\\\\|\\|', '', abstract).lower()
    abstract = re.sub('-', ' ', abstract).lower()
    # take out stopwords
    # if wantStopwordsRemoved == "y":
    #     f2 = open("stopwords.txt", "r")
    #     for stopWord in f2:
    #         #abstract = abstract.replace(stopWord.strip(), "")
    #         abstract = re.sub(r"%s" % stopWord , "", abstract)
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

    
        


    #stem it DOG!
    if wantStemming == "y":
        p = PorterStemmer()
        output=""
        for word in abstract.split():
            output += p.stem(word, 0,len(word)-1) + " "
            #print(output)
        abstract = output




    #combine title and abstract
    titleAbstract = title + abstract
        

    #create document dictionary initialized with all zero frequency
    for word in titleAbstract.split():
        docFrequency[word.strip()] = 0
        term = TermInfo(word.strip(), 0)
        terms[word.strip()] = term
    

    #document with text and initialized (all zero) dictionary of words
    
    document = DocumentStruct(allText, terms, docFrequency, ID, title, abstract, titleAbstract, {})
    documents.append(document)

# ---------------------------------------------------------------------

# 1.2
#------ for each document get the frequency of all the words in the document----
ATAA = ""
f3 = open("docc.txt", "w+")

# init document positions
for doc in documents:
    for word in doc.titleAbstract.split():
        doc.positions[word] = []

# get positions
for doc in documents:
    for idx, word in enumerate(doc.titleAbstract.split()):
        doc.positions[word].append(idx)



for doc in documents:
    f3.write(doc.ID + "\r\n")
    ATAA += doc.titleAbstract
    for idx, word in enumerate (doc.titleAbstract.split()):
        #doc.positions["accelerating"].append(0)
        if word not in reservedWords:
            doc.docFrequency[word.strip()] += 1
            doc.terms[word.strip()].frequency += 1
f3.close()

#print(documents[20].positions)
#print(documents[20].ID)
#print(documents[20].titleAbstract)



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
        if posting in doc.terms.keys():
            docList.append(doc)
    postingsList[posting] = docList

# Print postings list file
print("PRINTING POSTING LIST ...")
postingsFile = open("postingsLists.txt", "w+")

print(str(documents[20].ID))
print(str(documents[20].positions["convergence"]))

for post in postingsList:
    if (post != ""):
        postingsFile.write(post+ ": ")
        postingsFile.write("\r\n")
        for d in postingsList[post]:
            postingsFile.write("[ ID:" + str(d.ID) + " | ")
            postingsFile.write("Freq:" + str(d.docFrequency[post]) + " | Pos: ")
            for pos in d.positions[post]:
                postingsFile.write(str(pos) + ", ")

            postingsFile.write("], ")
        postingsFile.write("\r\n")
        postingsFile.write("\r\n")


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
