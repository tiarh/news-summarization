# tfidf_calculation.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class TFIDFCalculator:
    def __init__(self, kalimat_df):
        self.kalimat_df = kalimat_df
        self.tfidf_matrix = None
        self.feature_names = None

    def extract_and_preprocess_words(self, text):
        stop_words = set(stopwords.words('indonesian'))
        words = word_tokenize(text)
        preprocessed_words = [word.lower() for word in words if (word.isalnum() and word.lower() not in stop_words)]
        return preprocessed_words

    def calculate_tfidf(self):
        # Inisialisasi objek TfidfVectorizer untuk token kata
        tfidf_vectorizer = TfidfVectorizer(tokenizer=self.extract_and_preprocess_words, stop_words=stopwords.words('indonesian'))

        # Transforms kalimat menjadi matriks TF-IDF
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.kalimat_df['kalimat'])

        # Dapatkan daftar fitur (kata-kata) yang terkandung dalam TF-IDF
        self.feature_names = tfidf_vectorizer.get_feature_names_out()

    def get_tfidf_matrix(self):
        return self.tfidf_matrix

    def get_feature_names(self):
        return self.feature_names
