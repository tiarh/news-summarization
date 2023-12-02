import pandas as pd
from nltk.tokenize import sent_tokenize
import re
import string
import nltk

nltk.download('punkt')

# Fungsi untuk melakukan tokenisasi kalimat, konversi ke huruf kecil, dan menghapus tanda baca dan angka
def extract_and_preprocess_sentences(text):
    sentences = sent_tokenize(text)
    preprocessed_sentences = []

    for sentence in sentences:
        # Konversi ke huruf kecil
        sentence = sentence.lower()

        # Hapus tanda baca dan angka menggunakan regular expression
        sentence = re.sub(f"[{string.punctuation}0-9]", " ", sentence)

        # Hapus karakter '\n'
        sentence = sentence.replace('\n', ' ')

        # Hapus spasi berlebih
        sentence = ' '.join(sentence.split())

        preprocessed_sentences.append(sentence)

    return preprocessed_sentences

class KalimatExtractor:
    def __init__(self, dataframe):
        self.df = dataframe
        self.kalimat_df = pd.DataFrame(columns=['berita_id', 'kalimat'])  # Pastikan ada kolom 'kalimat'

    def extract_sentences(self):
        for i in range(len(self.df)):
            berita_id = i
            # In KalimatExtractor class, update where you access the content
            isi_berita = self.df.loc[i, 'isi']  # Use "isi" instead of "content"
            kalimat_berita = sent_tokenize(isi_berita)

            for idx, kalimat in enumerate(kalimat_berita):
                preprocessed_sentences = extract_and_preprocess_sentences(kalimat)
                for preprocessed_sentence in preprocessed_sentences:
                    self.kalimat_df = pd.concat([self.kalimat_df, pd.DataFrame({'berita_id': [berita_id], 'kalimat': [preprocessed_sentence]})],
                                                ignore_index=True)

    def get_extracted_sentences(self):
        return self.kalimat_df
