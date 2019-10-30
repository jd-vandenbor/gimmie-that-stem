import search as CustomSearch

sortedDocs = CustomSearch.search("I am interested in distributed algorithms - concurrent programs inwhich processes communicate and synchronize by using message passing.Areas of particular interest include fault-tolerance and techniquesfor understanding the correctness of these algorithms")
doubleword = False
seen=[]
for x in sortedDocs:
    if x[0] not in seen:
        seen.append(x[0])
    else:
        doubleword = True
        print(x[0])
print(doubleword)
