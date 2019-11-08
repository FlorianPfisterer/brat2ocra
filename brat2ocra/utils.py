from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 

def lemmatize(word: str) -> str:
    return lemmatizer.lemmatize(word)