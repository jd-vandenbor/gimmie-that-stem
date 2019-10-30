import invert, DocumentStruct, timeit, math, operator
from PorterStemmer import *

#---------------------- helper functions ---------------------

# remove duplicate documents
def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def dotProduct(d, q):
    if len(d) != len(q):
        return 0
    return sum(i[0] * i[1] for i in zip(d, q))

def magnitude(d):
    count = 0
    for num in d:
        count += num**2
    return math.sqrt(count)
#-------------------------------------------------------------

#--------- set up ----------
postingsList = invert.postingsList
postingListFile = open("postingsLists.txt", "r")
numberOfDocuments = invert.numberOfDocuments

#-------- SEARCH -----------
def search(input):
    userInput = input
    inputWords = userInput.split()

    #--- stem input if desired ---
    if invert.wantStemming == "y" and userInput != "ZZEND":
            for idx, word in enumerate(inputWords):
                p = PorterStemmer()
                stemmed = p.stem(inputWords[idx], 0,len(inputWords[idx])-1)
                inputWords[idx] = stemmed

    #---------------- MAIN LOOP ----------------
    idfs={}
    docs=[]
    fs=[]
    tfs=[]
    ws={}

    # create doc list that has a least one query word
    removelist=[]
    for x, word in enumerate(inputWords):
        try:
            print(word)
            for doc in postingsList[word]:
                docs.append(doc)
        except:
            print("ERROR ON LINE 51 of search.py: key did not match a word in posting list")
            removelist.append(word)
    for word in removelist:    
        inputWords.remove(str(word))
    docs = unique(docs)

    # create word bank
    wordCollection=[]
    for i in inputWords:
        if i not in wordCollection:
            wordCollection.append(i)
    for doc in docs:
        for word in doc.titleAbstract.split():
            if word not in wordCollection:
                wordCollection.append(word)

    #get idf values
    for x, word in enumerate(wordCollection):
        idf = math.log10(numberOfDocuments / len(postingsList[word]))
        idfs[word]=idf

    # get weighted document vectors 
    for doc in docs:
        fv=[]
        tfv=[]
        wv=[]
        for word in wordCollection:
            try:
                fv.append(doc.docFrequency[word])
                tfv.append(1 + math.log10(doc.docFrequency[word]))
                wv.append(idfs[word] * (1 + math.log10(doc.docFrequency[word])))

            except:
                fv.append(0)
                tfv.append(0)
                wv.append(0)
        fs.append(fv)
        tfs.append(tfv)
        ws[doc.ID] = wv

    # get query and query frequencies
    qWeight=[]
    query = ' '.join(inputWords)
    print("query:")
    print(query)
    print("")
    querywords={}
    for word in wordCollection:
        querywords[word] = 0
    for word in query.split():
        querywords[word] += 1

    # get weighted query vector qWeight 
    for word in wordCollection:
        fv=[]
        tfv=[]
        try:
            fv.append(querywords[word])
            tfv.append(1 + math.log10(querywords[word]))
            qWeight.append(idfs[word] * (1 + math.log10(querywords[word])))
        except:
            fv.append(0)
            tfv.append(0)
            qWeight.append(0)

    #------- get cosine similarity ---------    
    returnDic={}
    for weightedVector in ws:
        dot = dotProduct(ws[weightedVector], qWeight)
        magTotal = magnitude(ws[weightedVector]) * magnitude(qWeight)
        cosineSimilarity = dot/magTotal

        returnDic[weightedVector] = cosineSimilarity
        print("cosineSimilarity of Document " + weightedVector + ":")
        print(cosineSimilarity)
        print("")
    
    sortedDocs = sorted(returnDic.items(), key=operator.itemgetter(1))
    return sortedDocs
    


