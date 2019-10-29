import search as CustomSearch

sortedDocs = CustomSearch.search("computer system program")
for x in sortedDocs:
    print(x[1])