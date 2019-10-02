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
    userInput = raw_input("Please type in a sign term to test: ")
    userInput = userInput.strip()
    print(" ")
    #--- stem input if desired ---
    if invert.wantStemming == "y" and userInput != "ZZEND":
        p = PorterStemmer()
        userInput = p.stem(userInput, 0,len(userInput)-1)
        print("User Input stemmed is: " + userInput)
        print(" ")

    #---------- print correlating 
    if userInput in postingsList.keys():
        start = timeit.default_timer()
        for doc in postingsList[userInput]:
            print("Document ID: " + doc.ID) 
            print("Title: " + doc.title) # make original title in DocumentStruct
            print("Frequency: " + str(doc.docFrequency[userInput]))
            print("Positions: " + str(doc.positions[userInput]))
            
            
            lastFive=[]
            result=""
            counter=5
            found = False
            
            #print the 10 words surrounding the first match
            for word in doc.titleAbstract.split():
                if not found:
                    lastFive.append(word)
                    if len(lastFive) == 6:
                        del lastFive[0]
                    if word == userInput:
                        for e in lastFive:
                            result += e + " "
                        found = True
                        counter = (10 - len(lastFive))
                elif counter != 0:
                    result += word + " "
                    counter -= 1
            print("Summary: " + result)
            end = timeit.default_timer()
            time = end - start
            print("Time: " + str(time))
            print(" ")
            times.append(time)

    # report to user to enter new term if the search matched nothing
    elif userInput != "ZZEND":
        print("Sorry that term is not found in our postings list.")       

# print avverage time
totalTime = sum(times) / len(times)
print(" ")
print("Average Time for search: " + str(totalTime))
