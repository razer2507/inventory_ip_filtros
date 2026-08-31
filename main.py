
import flet as ft

def main(page:ft.Page):
    page.add(ft.Text('Hola mundo desde ANDROIDDD',size=30))
    if 1 == 1:
        raise EresUnPendejoError

class EresUnPendejoError(Exception):
    def __init__(self, mensaje="Eres bien pendejo"*100):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

ft.run(main=main)