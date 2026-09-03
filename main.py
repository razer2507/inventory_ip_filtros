import flet as ft


def main(page: ft.Page):
    # --- Configuración Visual ---
    page.title = "Distribuidora de Filtros - Demo"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    # --- Lista Fija de Marcas (Evita errores de ortografía) ---
    MARCAS_DISPONIBLES = [
        "WIX", "CHAMPION", "MILLARD", "MANN", "BALDWIN", "DONALDSON", 
        "FRAM", "FLEETGUARD", "MAHLE", "K&N", "TECFIL", "GONHER", "CATERPILLAR", "ISUZU"
    ]
    
    # Colores únicos y vibrantes para cada marca
    MAPA_COLORES_MARCAS = {
        "WIX": {"bg": "#FFD700", "text": "#000000"},       # Oro
        "CHAMPION": {"bg": "#000000", "text": "#FFFFFF"},  # Negro
        "MILLARD": {"bg": "#0000FF", "text": "#FFFFFF"},   # Azul
        "MANN": {"bg": "#00FF00", "text": "#000000"},      # Verde
        "BALDWIN": {"bg": "#FF0000", "text": "#FFFFFF"},   # Rojo
        "DONALDSON": {"bg": "#800080", "text": "#FFFFFF"}, # Púrpura
        "FRAM": {"bg": "#FF8C00", "text": "#000000"},      # Naranja
        "FLEETGUARD": {"bg": "#FF1493", "text": "#FFFFFF"},# Rosa
        "MAHLE": {"bg": "#008B8B", "text": "#FFFFFF"},     # Cian Oscuro
        "K&N": {"bg": "#A52A2A", "text": "#FFFFFF"},       # Marrón
        "TECFIL": {"bg": "#FFFF00", "text": "#000000"},    # Amarillo Neón
        "GONHER": {"bg": "#FF69B4", "text": "#000000"},    # Rosa Chicle
        "CATERPILLAR": {"bg": "#FFD700", "text": "#000000"}, # Amarillo Industrial
        "ISUZU": {"bg": "#00FFFF", "text": "#000000"}      # Cian
    }

    # --- Data Inicial Ficticia ---
    base_datos_ficticia = [
        {
            "id": 1, 
            "nombre": "FILTRO AIRE COROLLA", 
            "rosca": "3/4-16", 
            "stock": 30, 
            "modelos": [
                {"marca": "WIX", "codigo": "33674"},
                {"marca": "CHAMPION", "codigo": "3614"},
                {"marca": "MILLARD", "codigo": "ML-3614"}
            ]
        },
        {
            "id": 2, 
            "nombre": "FILTRO ACEITE TOYOTA YARIS", 
            "rosca": "3/4-16", 
            "stock": 12, 
            "modelos": [
                {"marca": "FRAM", "codigo": "PH4967"},
                {"marca": "FLEETGUARD", "codigo": "LF16104"}
            ]
        },
        {
            "id": 3, 
            "nombre": "FILTRO COMBUSTIBLE FORD RANGER", 
            "rosca": "3/4-16", 
            "stock": 8, 
            "modelos": [
                {"marca": "MAHLE", "codigo": "KL583"},
                {"marca": "K&N", "codigo": "HP-1002"}
            ]
        },
        {
            "id": 4, 
            "nombre": "FILTRO ACEITE HILUX 2.4", 
            "rosca": "M20x1.5", 
            "stock": 2, 
            "modelos": [
                {"marca": "MANN", "codigo": "W940"},
                {"marca": "WIX", "codigo": "51515"}
            ]
        },
        {
            "id": 5, 
            "nombre": "FILTRO COMBUSTIBLE CAT 320", 
            "rosca": "1-14 UNS", 
            "stock": 1, 
            "modelos": [
                {"marca": "CATERPILLAR", "codigo": "1R-0716"},
                {"marca": "FLEETGUARD", "codigo": "FF5320"}
            ]
        }
    ]

    # --- Referencias a Contenedores ---
    lista_tarjetas = ft.Column(spacing=15)

    # --- Función para Renderizar las Tarjetas ---
    def renderizar_aplicaciones(filtro_texto=""):
        lista_tarjetas.controls.clear()
        
        texto_busqueda = filtro_texto.strip().upper()

        # Ordenamiento eliminado para mantener la posición estable de las tarjetas
        for app in base_datos_ficticia:
            coincide_nombre = texto_busqueda in app["nombre"].upper()
            coincide_rosca = texto_busqueda in app["rosca"].upper()
            coincide_codigo = any(texto_busqueda in mod["codigo"].upper() for mod in app["modelos"])

            if texto_busqueda == "" or coincide_nombre or coincide_rosca or coincide_codigo:
                # Stock crítico
                es_bajo_stock = app["stock"] <= 3
                
                # Crear Chips para los Códigos de Fabricantes (Modelos)
                chips_modelos = []
                for mod in app["modelos"]:
                    colores = MAPA_COLORES_MARCAS.get(mod['marca'], {"bg": ft.Colors.GREY_700, "text": ft.Colors.WHITE})
                    chips_modelos.append(
                        ft.Container(
                            content=ft.Text(f"{mod['marca']}: {mod['codigo']}", weight=ft.FontWeight.BOLD, size=13, color=colores["text"]),
                            bgcolor=colores["bg"],
                            border_radius=15,
                            padding=5
                        )
                    )

                # Construir la Tarjeta
                tarjeta = ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            controls=[
                                ft.Row([
                                    ft.Text(app["nombre"], weight=ft.FontWeight.BOLD, size=16, expand=True),
                                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, a=app: abrir_formulario_gestion(e, a), icon_size=20),
                                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, a=app: (base_datos_ficticia.remove(a), renderizar_aplicaciones()), icon_size=20, icon_color=ft.Colors.RED_400)
                                ]),
                                # Alerta de Stock
                                ft.Text("¡ALERTA: STOCK BAJO!" if es_bajo_stock else "", color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD),
                                
                                ft.Container(
                                    content=ft.Row([
                                        ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_color=ft.Colors.RED_400, on_click=lambda e, item=app: (item.update({"stock": max(0, item["stock"]-1)}), renderizar_aplicaciones(input_busqueda.value))),
                                        ft.Text(f"{app['stock']} UND", size=16, weight=ft.FontWeight.BOLD),
                                        ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_color=ft.Colors.GREEN_600, on_click=lambda e, item=app: (item.update({"stock": item["stock"]+1}), renderizar_aplicaciones(input_busqueda.value))),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    bgcolor=ft.Colors.GREY_800, border_radius=10, padding=5
                                ),
                                ft.Divider(),
                                ft.Text("Modelos / Equivalencias:", size=12, weight=ft.FontWeight.W_500),
                                ft.Row(controls=chips_modelos, wrap=True, spacing=8),
                                ft.Container(height=5),
                                ft.Text(f"TIPO ROSCA: {app['rosca']}", size=13, color=ft.Colors.YELLOW_200, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
                lista_tarjetas.controls.append(tarjeta)
        page.update()

    # --- Evento de Búsqueda ---
    def al_cambiar_busqueda(e):
        renderizar_aplicaciones(e.control.value)

    # --- Campo de Búsqueda Gigante Arriba ---
    input_busqueda = ft.TextField(
        hint_text="BUSCAR FILTRO O CÓDIGO...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=al_cambiar_busqueda,
        capitalization=ft.TextCapitalization.CHARACTERS,
        border_radius=12,
        autofocus=True,
        expand=True
    )


    # --- Intercambio de pantalla (Formulario Estético) ---
    def abrir_formulario_gestion(e, app_a_editar=None):
        if app_a_editar is None:
            app_a_editar = {"nombre": "", "rosca": "", "stock": 1, "modelos": []}
            es_edicion = False
        else:
            es_edicion = True
        
        contenido_anterior = page.controls[:]

        
        # Campos básicos
        txt_nombre = ft.TextField(label="Nombre Aplicación", value=app_a_editar["nombre"] if es_edicion else "", capitalization=ft.TextCapitalization.CHARACTERS)
        txt_rosca = ft.TextField(label="Rosca", value=app_a_editar["rosca"] if es_edicion else "", capitalization=ft.TextCapitalization.CHARACTERS)
        txt_stock = ft.TextField(label="Stock", value=str(app_a_editar["stock"]) if es_edicion else "1", keyboard_type=ft.KeyboardType.NUMBER)

        # Edición de modelos (códigos)
        lista_modelos_edicion = ft.Column()
        
        # --- NUEVOS CAMPOS DE AGREGADO IN-PLACE ---
        dd_marca_nuevo = ft.Dropdown(label="Marca", options=[ft.dropdown.Option(m) for m in MARCAS_DISPONIBLES], expand=True)
        txt_codigo_nuevo = ft.TextField(label="Código", expand=True)

        def actualizar_lista_modelos():
            lista_modelos_edicion.controls.clear()
            for i, mod in enumerate(app_a_editar["modelos"]):
                lista_modelos_edicion.controls.append(ft.Row([
                    ft.Text(f"{mod['marca']}:", weight=ft.FontWeight.BOLD, width=80),
                    ft.TextField(value=mod['codigo'], dense=True, expand=True, on_change=lambda e, idx=i: app_a_editar["modelos"].__getitem__(idx).__setitem__("codigo", e.control.value.upper())),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, idx=i: (app_a_editar["modelos"].pop(idx), actualizar_lista_modelos()))
                ]))
            page.update()

        def agregar_al_momento(e):
            if dd_marca_nuevo.value and txt_codigo_nuevo.value:
                app_a_editar["modelos"].append({"marca": dd_marca_nuevo.value, "codigo": txt_codigo_nuevo.value.upper()})
                txt_codigo_nuevo.value = "" # Limpiar
                actualizar_lista_modelos()
                page.update()

        if es_edicion:
            actualizar_lista_modelos()

        def volver(ev):
            page.controls.clear()
            page.controls.extend(contenido_anterior)
            page.update()

        def guardar_datos(ev):
            if txt_nombre.value:
                if es_edicion:
                    app_a_editar.update({
                        "nombre": txt_nombre.value.upper(),
                        "rosca": txt_rosca.value.upper(),
                        "stock": int(txt_stock.value) if txt_stock.value.isdigit() else 0
                    })
                else:
                    nueva_app = {
                        "id": len(base_datos_ficticia) + 1,
                        "nombre": txt_nombre.value.upper(),
                        "rosca": txt_rosca.value.upper(),
                        "stock": int(txt_stock.value) if txt_stock.value.isdigit() else 0,
                        "modelos": app_a_editar["modelos"] if "modelos" in app_a_editar else []
                    }
                    base_datos_ficticia.append(nueva_app)
                renderizar_aplicaciones()
                volver(None)

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Editar Filtro" if es_edicion else "Nuevo Filtro", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Divider(),
                    txt_nombre, txt_rosca, txt_stock,
                    ft.Text("Códigos de Fabricante:", weight=ft.FontWeight.BOLD),
                    ft.Row([
                        dd_marca_nuevo, 
                        txt_codigo_nuevo, 
                        ft.ElevatedButton("Agregar Código", icon=ft.Icons.ADD_CIRCLE, on_click=agregar_al_momento)
                    ]),
                    ft.Text("Lista de Códigos:", weight=ft.FontWeight.W_500, size=12),
                    lista_modelos_edicion,
                    ft.Container(height=20),
                    ft.Row([
                        ft.OutlinedButton("Cancelar", on_click=volver),
                        ft.FilledButton("Guardar Cambios", on_click=guardar_datos)
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=20,
                bgcolor=ft.Colors.GREY_900,
                border_radius=15
            )
        )
        page.update()


    # --- Renderizar Vista Inicial ---
    renderizar_aplicaciones()

    # --- Estructura de la Pantalla ---
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                        controls=[
                        input_busqueda,
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            tooltip="Nuevo Filtro",
                            on_click=lambda e: abrir_formulario_gestion(e, None),
                            bgcolor=ft.Colors.BLUE_600
                        )
                    ],
                    spacing=10
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                lista_tarjetas
            ]
        )
    )

if __name__ == "__main__":
    ft.run(main)
