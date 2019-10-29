import invert, DocumentStruct, timeit
from PorterStemmer import *

#--------- set up ----------
documents = invert.documents
postingsList = invert.postingsList
postingListFile = open("postingsLists.txt", "r")
userInput = ""
start = 0
times=[]

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
    for word in inputWords:
        idfs[word]=len(postingsList[word])
    
    for idf in idfs:
        print(idfs[idf])

