# app.py
import streamlit as st
from crawling_detik import DetikCrawler
from ekstraksi_kalimat import KalimatExtractor
from tfidf_calculation import TFIDFCalculator
from cosine_similarity import CosineSimilarity
from graph_formation import GraphFormation
from graph_analysis import GraphAnalysis
import matplotlib.pyplot as plt
import networkx as nx

def main():
    st.title("Detik Summarization App")

    # Menu
    menu = ["Crawling", "Ekstraksi Kalimat", "TF-IDF", "Cosine Similarity", "Graph Formation", "Graph Analysis"]
    choice = st.sidebar.selectbox("Pilih Menu", menu)

# ...

    if choice == "Crawling":
        st.header("Crawling Berita Detik.com")
        topic = st.text_input("Masukkan topik berita yang ingin diambil:")
        if st.button("Crawl"):
            detik_crawler = DetikCrawler(topic)
            detik_crawler.extract_news()
            st.session_state.detik_crawler = detik_crawler  # Store detik_crawler in session state
            st.success("Crawling Selesai!")
            st.subheader("Hasil Crawling:")
            st.write(st.session_state.detik_crawler.df)

    elif choice == "Ekstraksi Kalimat":
        st.header("Ekstraksi Kalimat")
        if st.button("Ekstraksi Kalimat"):
            if "detik_crawler" not in st.session_state or st.session_state.detik_crawler is None:
                st.warning("Silakan lakukan crawling terlebih dahulu.")
            else:
                kalimat_extractor = KalimatExtractor(st.session_state.detik_crawler.df)
                kalimat_extractor.extract_sentences()

                # Store kalimat_extractor in session_state
                st.session_state.kalimat_extractor = kalimat_extractor

                # Display extracted sentences DataFrame
                st.subheader("DataFrame Hasil Ekstraksi Kalimat:")
                st.write(st.session_state.kalimat_extractor.df)

                # Display DataFrame with words
                st.write(st.session_state.kalimat_extractor.kalimat_df[['berita_id', 'kalimat']])





# Pada bagian TF-IDF Calculation
    elif choice == "TF-IDF":
        st.header("TF-IDF Calculation")
        if st.button("Hitung TF-IDF"):
            # Check if kalimat_extractor is in session_state and not None
            if "kalimat_extractor" not in st.session_state or st.session_state.kalimat_extractor is None:
                st.warning("Silakan lakukan ekstraksi kalimat terlebih dahulu.")
            else:
                # Use kalimat_df from session_state
                tfidf_calculator = TFIDFCalculator(st.session_state.kalimat_extractor.kalimat_df)
                tfidf_calculator.calculate_tfidf()

                # Store tfidf_calculator in session_state
                st.session_state.tfidf_calculator = tfidf_calculator

                st.success("Perhitungan TF-IDF Selesai!")
                st.subheader("Hasil Perhitungan TF-IDF:")
                st.write(st.session_state.tfidf_calculator.tfidf_matrix)
                



    elif choice == "Cosine Similarity":
        st.header("Cosine Similarity Calculation")

        # Check if tfidf_calculator is in session_state and not None
        if "tfidf_calculator" not in st.session_state or st.session_state.tfidf_calculator is None:
            st.warning("Silakan lakukan perhitungan TF-IDF terlebih dahulu.")
        else:
            if st.button("Hitung Similaritas Cosine"):
                # Use tfidf_calculator from session_state
                cosine_similarity = CosineSimilarity(st.session_state.tfidf_calculator.tfidf_matrix)
                cosine_similarity.calculate_cosine_similarity()

                # Store cosine_similarity in session_state
                st.session_state.cosine_similarity = cosine_similarity

                st.success("Perhitungan Similaritas Cosine Selesai!")
                # Tampilkan hasil Similaritas Cosine jika cosine_similarity telah diinisialisasi

                st.subheader("Hasil Perhitungan Similaritas Cosine:")
                st.write(st.session_state.cosine_similarity.tfidf_matrix)



    elif choice == "Graph Formation":
        st.header("Graph Formation")
        # Gunakan cosine_similarity dari session_state
        cosine_similarity = st.session_state.cosine_similarity
        
        # Pastikan cosine_similarity sudah ada di dalam session_state
        if "cosine_similarity" in st.session_state and cosine_similarity is not None:
            # Pastikan cosine_similarity_matrix sudah ada di dalam cosine_similarity
            if hasattr(cosine_similarity, 'cosine_similarity_matrix') and cosine_similarity.cosine_similarity_matrix is not None:
                # Gunakan cosine_similarity_matrix dari cosine_similarity
                cosine_similarity_matrix = cosine_similarity.cosine_similarity_matrix
                
                # Buat objek GraphFormation
                graph_formation = GraphFormation(cosine_similarity_matrix)
                graph_formation.create_graph()

                st.session_state.graph_formation = graph_formation

                # Dapatkan graf
                G = graph_formation.graph

                # Visualisasikan graf menggunakan networkx
                pos = nx.spring_layout(G)  # Sesuaikan layout sesuai kebutuhan

                # Gambar graf
                nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800)

                # Tampilkan graf di Streamlit
                st.pyplot(plt)

                st.success("Pembentukan Graf Selesai!")
            else:
                st.warning("Silakan lakukan perhitungan Similaritas Cosine terlebih dahulu.")
        else:
            st.warning("Silakan lakukan perhitungan Similaritas Cosine terlebih dahulu.")


    elif choice == "Graph Analysis":
        st.header("Graph Analysis")

        # Check if kalimat_extractor is in session_state and not None
        if "kalimat_extractor" not in st.session_state or st.session_state.kalimat_extractor is None:
            st.warning("Silakan lakukan pembentukan Graf terlebih dahulu.")
        else:
            # Use kalimat_extractor from session_state
            kalimat_extractor = st.session_state.kalimat_extractor

            # Check if kalimat_df is available in kalimat_extractor
            if hasattr(kalimat_extractor, 'kalimat_df') and kalimat_extractor.kalimat_df is not None:
                kalimat_df = kalimat_extractor.kalimat_df

                # Check if graph_formation is available in session_state
                if "graph_formation" in st.session_state and st.session_state.graph_formation is not None:
                    # Use graph_formation from session_state
                    graph_formation = st.session_state.graph_formation

                    # Create an instance of GraphAnalysis
                    graph_analysis = GraphAnalysis(graph_formation.graph, kalimat_df)

                    # Perform analysis or display data as needed
                    graph_analysis.display_top_closeness_sentences()
                else:
                    st.warning("Data graf tidak tersedia. Lakukan pembentukan graf terlebih dahulu.")
            else:
                st.warning("Data kalimat tidak tersedia. Lakukan pembentukan graf terlebih dahulu.")






if __name__ == "__main__":
    main()
