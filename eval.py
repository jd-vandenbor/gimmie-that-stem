import search as CustomSearch

sortedDocs = CustomSearch.search("coter system program")
for x in sortedDocs:
    print(x[0])