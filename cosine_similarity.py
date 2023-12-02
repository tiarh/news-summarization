# cosine_similarity.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CosineSimilarity:
    def __init__(self, tfidf_matrix):
        self.tfidf_matrix = tfidf_matrix
        self.cosine_similarity_matrix = None

    def calculate_cosine_similarity(self):
        # Hitung kemiripan kosinus antara dokumen-dokumen
        self.cosine_similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_cosine_similarity_matrix(self):
        return self.cosine_similarity_matrix

# Example usage:
# cosine_calculator = CosineSimilarityCalculator(tfidf_matrix)
# cosine_calculator.calculate_cosine_similarity()
# cosine_similarity_matrix = cosine_calculator.get_cosine_similarity_matrix()
# # Now you can use cosine_similarity_matrix in the subsequent steps of your program.
