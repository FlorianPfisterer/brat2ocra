from bratreader.annotateddocument import AnnotatedDocument
from bratreader.annotation import Annotation
from bratreader.sentence import Sentence
from bratreader.word import Word
from typing import List, Dict
from brat2ocra.ocra_token import OcraToken
from brat2ocra.ocra_sentence import OcraSentence
import brat2ocra.utils as utils

class DocConverter:
    doc: AnnotatedDocument
    sentences: List[OcraSentence]

    def __init__(self, document: AnnotatedDocument):
        self.doc = document
        self.__read_tokens()

    def __read_tokens(self):
        # first, only read the words
        words = []
        for sentence in self.doc.sentences:
            for word in sentence.words:
                words.append(word)

        # now, bucket them by sentence
        words_in_sentence: Dict[int, List[Word]] = {}
        for word in words:
            if word.sentkey in words_in_sentence:
                words_in_sentence[word.sentkey].append(word)
            else:
                words_in_sentence[word.sentkey] = [word]

        # sort the words in each sentence-bucket by start index (this gives token indices in the sentence)
        num_sentences = len(words_in_sentence.keys())
        sentences_words: List[List[Word]] = [[]] * num_sentences
        token_idx_by_span_id: Dict[str, int] = {}
        for sentence_idx in words_in_sentence:
            words = words_in_sentence[sentence_idx]
            sorted_words = sorted(words, key=lambda w: w.start)
            sentences_words[sentence_idx] = sorted_words

            for idx, word in enumerate(sorted_words):
                # make the token index in the sentence retrievable by the span of the word
                span_id = DocConverter.__get_span_id(word)
                token_idx_by_span_id[span_id] = idx

        def create_ocra_token(word: Word) -> OcraToken:
            if len(word.annotations) != 1:
                    raise ValueError('Found word with zero or multiple annotations: {} (num annotations: {})'.format(word.form, len(word.annotations)))

            annotation = word.annotations[0]    
            labels: Dict[str, List[str]] = annotation.labels
            links: Dict[str, List[Annotation]] = annotation.links

            # determine POS-tag
            upos = list(labels.keys())[0]

            # determine head and relation to head
            token_idx = token_idx_by_span_id[DocConverter.__get_span_id(word)]
            relation = None
            governor_idx = None
            if len(links.keys()) == 0:
                relation = 'root'
                governor_idx = token_idx
            else:
                relation = list(links.keys())[0]
                governor_annotations: List[Annotation] = links[relation]
                governor_annotation = governor_annotations[0]
                
                if len(governor_annotations) != 1:
                    print('Found word with multiple governors: {} (relation = {}), governors: {}. Ignoring all but last.'.format(word.form, relation, governor_annotations))
                
                governor_word = governor_annotation.words[0]
                governor_span_id = DocConverter.__get_span_id(governor_word)
                governor_idx = token_idx_by_span_id[governor_span_id]

            lemma = utils.lemmatize(word.form)
            xpos = utils.get_xpos(upos, word.form)
            return OcraToken(index=token_idx, text=word.form, lemma=lemma, upos=upos, xpos=xpos, governor_index=governor_idx, dependency_relation=relation)

        def create_ocra_sentence(sentence_idx: int) -> OcraSentence:
            words = sentences_words[sentence_idx]
            tokens: List[OcraToken] = list(map(create_ocra_token, words))
            return OcraSentence(sentence_idx, tokens)

        # finally, we can check the annotations (dependency relations) and create tokens 
        self.sentences = list(map(create_ocra_sentence, range(num_sentences)))

    @staticmethod
    def __get_span_id(word: Word) -> str:
        return '{}:{}'.format(word.start, word.end)
