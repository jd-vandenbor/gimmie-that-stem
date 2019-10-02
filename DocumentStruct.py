class DocumentStruct:
    def __init__(self, allText, terms, docFrequency, ID, title, abstract, titleAbstract, positions={}):
        self.allText = allText
        self.terms = terms  # A dictionary containing all terms in the doc
        self.docFrequency = docFrequency
        self.ID = ID
        self.title = title
        self.abstract = abstract
        self.titleAbstract = titleAbstract
        self.positions = positions
        #self.noStopWords = noStopWords


