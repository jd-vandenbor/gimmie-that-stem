class DocumentStruct:
    def __init__(self, allText, docFrequency, ID, title, rawTitle, author, abstract, titleAbstract, positions={}):
        self.allText = allText
        self.docFrequency = docFrequency
        self.ID = ID
        self.title = title
        self.abstract = abstract
        self.titleAbstract = titleAbstract
        self.positions = positions
        self.rawTitle = rawTitle
        self.author = author
        #self.noStopWords = noStopWords


