class OcraToken:
    index: int
    text: str 
    lemma: str
    upos: str
    xpos: str
    governor_index: int
    dependency_relation: str

    def __init__(self, index: int, text: str, lemma: str, upos: str, xpos: str, governor_index: int, dependency_relation: str):
        self.index = index
        self.text = text
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.governor_index = governor_index
        self.dependency_relation = dependency_relation

    def to_dict(self):
        return {
            'index': self.index,
            'text': self.text,
            'lemma': self.lemma,
            'upos': self.upos,
            'xpos': self.xpos,
            'governor': self.governor_index,
            'dependency_relation': self.dependency_relation
        }
