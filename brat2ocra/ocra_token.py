class OcraToken:
    index: int
    text: str 
    lemma: str
    governor_index: int
    dependency_relation: str

    def __init__(self, index: int, text: str, lemma: str, governor_index: int, dependency_relation: str):
        self.index = index
        self.text = text
        self.lemma = lemma
        self.governor_index = governor_index
        self.dependency_relation = dependency_relation

    def to_dict(self):
        return {
            'index': self.index,
            'text': self.text,
            'lemma': self.lemma,
            'governor': self.governor_index,
            'dependency_relation': self.dependency_relation
        }
