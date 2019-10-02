import invert, DocumentStruct, timeit

documents = invert.documents
postingsList = invert.postingsList
postingListFile = open("postingsLists.txt", "r")
userInput = ""
start = 0
times=[]
while userInput != "ZZEND":
    userInput = raw_input("Please type in a sign term to test: ")
    userInput = userInput.strip()
    if userInput in postingsList.keys():
        start = timeit.default_timer()
        for doc in postingsList[userInput]:
            print("Document ID: " + doc.ID) 
            print("Title: " + doc.title) # make original title in DocumentStruct
                            # possibly stem answer
            print("Frequency: " + str(doc.docFrequency[userInput]))
            print("Positions: " + str(doc.positions[userInput]))
            #re.search(r"%s" % userInput , doc.titleAbstract)
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
    else:
        print("Sorry that term is not found in our postings list. Perhaps it was stemmed?")       
    # for line in postingListFile:
    #     if line.startswith(userInput):
    #         print(line)
    postingListFile = open("postingsLists.txt", "r")

totalTime = sum(times) / len(times)
print("Average Time: " + str(totalTime))
