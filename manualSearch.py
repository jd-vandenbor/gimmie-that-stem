import invert, DocumentStruct, timeit, math
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

    #---------------- MAIN LOOP ----------------
    idfs={}
    docs=[]
    fs=[]
    tfs=[]
    ws={}

    # create doc list that has a least one query word
    for x, word in enumerate(inputWords):
        for doc in postingsList[word]:
            docs.append(doc)
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
        # print("doc.titleAbstract")
        # print(doc.titleAbstract)
        # print("fv")
        # print(fv)
        # print("tfv")
        # print(tfv)
        # print("wv")
        # print(wv)
        fs.append(fv)
        tfs.append(tfv)
        ws[doc.ID] = wv
    #print("Document Weight Vectors:")
    # for x, _w in enumerate(ws):
        # print(fs[x])
        # print(tfs[x])
        # print(str(_w) + ": " + str(ws[_w]))

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
    for weightedVector in ws:
        dot = dotProduct(ws[weightedVector], qWeight)
        magTotal = magnitude(ws[weightedVector]) * magnitude(qWeight)
        cosineSimilarity = dot/magTotal
        print("cosineSimilarity of Document " + weightedVector + ":")
        print(cosineSimilarity)
        print("")