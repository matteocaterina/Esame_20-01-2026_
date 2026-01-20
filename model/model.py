import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()

        self._artists_list = []
        self.lista_artisti_min = []
        self.lista_conn = []
        self.id_map = {}
        self._nodes = []
        self._edges = []
        self.load_all_artists()

        self.percorso_best = []
        self.peso_best = 0

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.lista_artisti_min = DAO.get_artisti_soglia(min_albums)
        return self.lista_artisti_min


    def build_graph(self, soglia):
        for artist in self.lista_artisti_min:
            self._nodes.append(artist)

        for artist in self.lista_artisti_min:
            self.id_map[artist.id] = artist
        self._graph.add_nodes_from(self._nodes)

        self.lista_conn = DAO.get_conn_art_track(soglia)

        for id1, id2, w in self.lista_conn:
            self._edges.append((id1, id2, w))
            self._graph.add_edge(id1, id2, weight=w)


    def get_vicini(self, artista):
        print(artista)
        result = []
        for v in self._graph.neighbors(artista):
            print(v)
            w = self._graph[artista][v]['weight']
            result.append((v,w))
        return sorted(result, key=lambda x: x[0])


    def cammino_massimo(self, n_max, d_min, artista):
        self.percorso_best = []
        self.peso_best = 0
        self._ricorsione([artista], n_max, d_min, 0)

        return self.percorso_best, self.peso_best

    def _ricorsione(self, parziale, num_max_art, durata_min, peso_corrente):
        ultimo_nodo = parziale[-1]
        vicini = self.get_neighb(ultimo_nodo,durata_min)

        if len(parziale) == num_max_art:
            if peso_corrente > self.peso_best:
                self.percorso_best = parziale.copy()
                self.peso_best = peso_corrente
            return

        for n,w in vicini:
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, num_max_art, durata_min, peso_corrente + w)
                parziale.pop()




    def get_neighb(self, ultimo_nodo, durata_min):
        result = []
        art = DAO.durate()
        for v in self._graph.neighbors(ultimo_nodo):
            durata = art[v.id]
            if durata >= durata_min:
                w = self._graph[ultimo_nodo][v]['weight']
                result.append((v,w))
        return result




