from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 

def lemmatize(word: str) -> str:
    return lemmatizer.lemmatize(word)

def get_xpos(upos: str, word: str) -> str:
    if upos == 'VERB' and word.endswith('ed'):
        return 'VBN'
    else:
        return ''