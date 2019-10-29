import invert, DocumentStruct, timeit, math
from PorterStemmer import *

# helper function to remove duplicate documents
def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

#--------- set up ----------
postingsList = invert.postingsList
postingListFile = open("postingsLists.txt", "r")
userInput = ""
start = 0
times=[]
numberOfDocuments = invert.numberOfDocuments
#-------- user input loop -----------
while userInput != "ZZEND":
    print(" ")

    #get user input
    userInput = raw_input("Please type in a term to test: ")
    userInput = userInput.strip()
    print(" ")

    inputWords = userInput.split()

    #--- stem input if desired ---
    if invert.wantStemming == "y" and userInput != "ZZEND":
            for idx, word in enumerate(inputWords):
                p = PorterStemmer()
                stemmed = p.stem(inputWords[idx], 0,len(inputWords[idx])-1)
                inputWords[idx] = stemmed

    idfs={}
    #---------------- MAIN LOOP ----------------
    docs=[]
    fs=[]
    tfs=[]
    ws={}
    for x, word in enumerate(inputWords):
        # print("N: " + str(numberOfDocuments))
        # print("Di: " + str(len(postingsList[word])))
        idf = math.log10(numberOfDocuments / len(postingsList[word]))
        idfs[word]=idf
        for doc in postingsList[word]:
            docs.append(doc)
    docs = unique(docs)
    # for doc in docs:
    #     print(doc.ID)

    docseen=[]
    for doc in docs:

        docseen.append(doc)
    
        f=[]
        tf=[]
        w=[]
        for word in inputWords:
            try:
                f.append(doc.docFrequency[word])
                tf.append(1 + math.log10(doc.docFrequency[word]))
                w.append(idfs[word] * (1 + math.log10(doc.docFrequency[word])))
            except:
                f.append(0)
                tf.append(0)
                w.append(0)
        
        fs.append(f)
        tfs.append(tf)
        ws[doc.ID] = w

    # for _f in fs:
    #     print(_f)
    
    # print("T's")
    # for _tf in tfs:
    #     print(_tf)

    for x, _w in enumerate(ws):
        # print(fs[x])
        # print(tfs[x])
        print(str(_w) + ": ")
        print(ws[_w])

    
    
    for idf in idfs:
        print(idfs[idf])

