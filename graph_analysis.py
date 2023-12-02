import networkx as nx
import streamlit as st

class GraphAnalysis:
    def __init__(self, graph, kalimat_df):
        self.graph = graph
        self.kalimat_df = kalimat_df

    def calculate_closeness_centrality(self):
        closeness_centrality = nx.closeness_centrality(self.graph)
        sorted_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
        return sorted_closeness

    def get_top_closeness_nodes(self, top_k=3):
        sorted_closeness = self.calculate_closeness_centrality()
        top_nodes = sorted_closeness[:top_k]
        return top_nodes


    def display_top_closeness_sentences(self, top_k=3):
        sorted_closeness = self.get_top_closeness_nodes(top_k)
        
        st.write("Tiga Kalimat Teratas dari Nilai Tertinggi Closeness Centrality:")
        for node, _ in sorted_closeness:
            kalimat_index = int(node.split("#")[1])  # Mendapatkan indeks kalimat dari simpul
            kalimat = self.kalimat_df['kalimat'][kalimat_index]
            st.write(f"Kalimat #{kalimat_index}: {kalimat}")

    def remove_numbers_from_sentences(self, sentences):
        # Hapus angka dari kalimat
        return ["".join(filter(str.isalpha, sentence)) for sentence in sentences]
    



