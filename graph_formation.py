# graph_formation.py
import networkx as nx

class GraphFormation:
    def __init__(self, cosine_similarity_matrix, threshold=0.07):
        self.cosine_similarity_matrix = cosine_similarity_matrix
        self.threshold = threshold
        self.graph = nx.Graph()

    def create_graph(self):
        # Tambahkan simpul (node) untuk setiap kalimat
        for i in range(len(self.cosine_similarity_matrix)):
            node_label = f"Kalimat #{i}"
            self.graph.add_node(node_label, label=node_label)

        # Tambahkan tepi (edge) antara kalimat berdasarkan skor kemiripan kosinus
        for i in range(len(self.cosine_similarity_matrix)):
            for j in range(i + 1, len(self.cosine_similarity_matrix)):
                similarity_score = self.cosine_similarity_matrix[i][j]
                if similarity_score > self.threshold:
                    node_i = f"Kalimat #{i}"
                    node_j = f"Kalimat #{j}"
                    self.graph.add_edge(node_i, node_j, weight=similarity_score)

    def get_graph(self):
        return self.graph

# Example usage:
# graph_formation = GraphFormation(cosine_similarity_matrix)
# graph_formation.create_graph()
# graph = graph_formation.get_graph()
# # Now you can use the graph in the subsequent steps of your program.
