import invert, DocumentStruct, timeit, math
from PorterStemmer import *
import search as CustomSearch


#--------- set up ----------
userInput = ""
numberOfDocuments = invert.numberOfDocuments
documents = invert.documents
docs={}
for doc in documents:
    docs[doc.ID]=doc
#-------- user input loop -----------
while userInput != "ZZEND":
    print(" ")

    #get user input
    userInput = raw_input("Please type in a term to test: ")
    userInput = userInput.strip()
    sortedDocs = CustomSearch.search(userInput)
    for idx, x in enumerate(sortedDocs):
        print(str(idx) + ": " + x[0] + "    Author: " + docs[x[0]].author.strip() + "\"" + "    Title: \"" + docs[x[0]].rawTitle.strip('\n') + "\"")


