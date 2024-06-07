import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.anno=None
        self.country=None
        self.N=0

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        self._listCountry=self._model.getAllCountries()
        for el in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(el))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self.anno=self._view.ddyear.value
        self.country=self._view.ddcountry.value
        if self.anno is None or self.anno=="" or self.country is None or self.country=="":
            self._view.create_alert("Scegliere un anno e una nazione dai dropdown")
            return
        self._model.creaGrafo(self.anno,self.country)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato. Ha {len(self._model.g.nodes)} nodi e {len(self._model.g.edges)} archi"))




    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        if len(self._model.g.nodes)==0:
            self._view.create_alert("Creare prima il grafo!")
            return

        vertici = self._model.getVerticiOrdinati()
        for v in vertici:
            self._view.txtOut2.controls.append(
                ft.Text(f"{v[0].Retailer_name}: {v[1]}"))

        self._view.update_page()

        pass


    def handle_path(self, e):
        self._view.txtOut3.controls.clear()
        if len(self._model.g.nodes)==0:
            self._view.create_alert("Prima devi creare il grafo")
            return
        self.N=self._view.txtN.value
        if self.N==0 or self.N is None:
            self._view.create_alert("Inserire un valore in N")
            return
        try:
            self.N=int(self._view.txtN.value)
            if self.N<2:
                self._view.create_alert("Inserire un intero maggiore o uguale a 2")
                return
            self._model.getBP(self.N)
            elementi=self._model.BP
            peso=self._model.topPeso
            self._view.txtOut3.controls.append(
                ft.Text(f"Peso: {peso} , nodi: {len(elementi)} archi"))

            for el in elementi:
                self._view.txtOut3.controls.append(
                    ft.Text(f"{el.Retailer_name}"))





        except ValueError:
            self._view.create_alert("Inserire un intero")
            return








        self._view.update_page()


        pass
