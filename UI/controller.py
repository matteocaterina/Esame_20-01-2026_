import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.artista = None

    def handle_create_graph(self, e):
        try:
            n_alb = int(self._view.txtNumAlbumMin.value)
            if n_alb <= 0:
                self._view.show_alert('Inserire un numero maggiore di 0')
            self.lista_nodi = self._model.load_artists_with_min_albums(n_alb)
            self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {len(self.lista_nodi)}'))
            self._model.build_graph(n_alb)
            lista_archi = self._model._edges
            self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {len(lista_archi)}'))

            for a in self.lista_nodi:
                self._view.ddArtist.options.append(ft.dropdown.Option(key=a.id, text=a))


        except ValueError:
            self._view.show_alert('Inserire un numero intero')

        self._view.update_page()

    def handle_connected_artists(self, e):
        id = int(self._view.ddArtist.value)
        self.artista = self._model.id_map[id]
        print(self.artista)
        self._view.txt_result.controls.append(ft.Text(f'ARTISTI DIRETTAMENTE COLLEGATI AD ARTISTA {self.artista}'))
        vicini = self._model.get_vicini(self.artista)
        for x in vicini:
            self._view.txt_result.controls.append(ft.Text(f' {x[0]} - {x[1]}\n'))

        self._view.update_page()

    def handle_cammino(self, e):
        try:
            d_min = float(self._view.txtMinDuration.value)
            n_max = int(self._view.txtMaxArtists.value)
            if d_min <= 0:
                self._view.show_alert('Inserire un numero maggiore di 0')
            if n_max < 1 or n_max > len(self.lista_nodi):
                self._view.show_alert('Inserire un numero valido')
            percorso,peso = self._model.cammino_massimo(n_max, d_min, self.artista)
            self._view.txt_result.clear()
            self._view.txt_result.controls.append(ft.Text(f'cammino di peso massimo di artista {self.artista}'))
            self._view.txt_result.controls.append(ft.Text(f'{len(percorso)}'))
            for n in percorso:
                self._view.txt_result.controls.append(ft.Text(f'{n}'))
            self._view.txt_result.controls.append(ft.Text(f'Peso massimo {peso}'))


        except ValueError:
            self._view.show_alert('Inserire un numero valido, intero o float a seconda della casella')


    def on_change(self,e):
        id = int(self._view.ddArtist.value)
        self.artista = self._model.id_map[id]



