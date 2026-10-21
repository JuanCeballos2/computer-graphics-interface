import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import librerias as lib

img_original = None  # Variable global que almacenará el arreglo de NumPy
img_segunda = None   # Segunda imagen (arreglo NumPy) para la suma ponderada
img_actual = None    # Última imagen mostrada en el visor (se usa para el histograma)
_bloqueo = False     # Evita que los .set() programáticos de los sliders disparen sus callbacks

ANCHO_VISOR = 750
ALTO_VISOR = 700


def mostrar_imagen(img_input, ampliar=False):
    """Muestra una imagen en el visor.
    ampliar=True la escala (vecino más cercano) hasta ocupar el visor, útil para
    ver los píxeles de imágenes pequeñas como las de reducir resolución."""
    global img_actual

    if isinstance(img_input, np.ndarray):
        img_actual = img_input
        img_pil = Image.fromarray(img_input)
    else:
        img_actual = np.array(img_input)
        img_pil = img_input

    if ampliar:
        ancho, alto = img_pil.size
        escala = min(ANCHO_VISOR / ancho, ALTO_VISOR / alto)
        img_pil = img_pil.resize(
            (max(1, int(ancho * escala)), max(1, int(alto * escala))),
            Image.NEAREST,
        )
    else:
        img_pil.thumbnail((ANCHO_VISOR, ALTO_VISOR))

    img_tk = ImageTk.PhotoImage(img_pil)

    etiqueta_imagen.config(image=img_tk)
    etiqueta_imagen.image = img_tk


def reiniciar_ajustes(mantener=None):
    """Deja en su valor inicial los controles de ajuste, excepto el grupo indicado
    ('canal', 'gris', 'brillo' o 'brillo_canal')."""
    global _bloqueo
    _bloqueo = True
    try:
        if mantener != "canal":
            combo_canales.current(0)
        if mantener != "gris":
            combo_grises.current(0)
        if mantener != "brillo":
            slider_brillo.set(0)
        if mantener != "brillo_canal":
            slider_brillo_canal.set(0)
        lbl_info_reduccion.config(text="")
    finally:
        _bloqueo = False


def poner_texto(entrada, texto):
    entrada.delete(0, "end")
    entrada.insert(0, str(texto))


def restablecer_entradas():
    """Valores por defecto de las entradas numéricas (los de recorte se calculan según la imagen)."""
    poner_texto(entrada_umbral, 128)
    poner_texto(entrada_factor_red, 4)
    poner_texto(entrada_zoom_factor, 5)
    poner_texto(entrada_angulo, 45)

    if img_original is not None:
        alto, ancho = img_original.shape[:2]
        lbl_tam_img.config(text=f"Imagen cargada: {ancho} x {alto} px (ancho x alto)")
        poner_texto(entrada_x_ini, ancho // 4)
        poner_texto(entrada_x_fin, (3 * ancho) // 4)
        poner_texto(entrada_y_ini, alto // 4)
        poner_texto(entrada_y_fin, (3 * alto) // 4)
        poner_texto(entrada_zoom_region, min(500, alto, ancho))
    else:
        lbl_tam_img.config(text="Imagen cargada: ninguna")


def leer_entero(entrada, nombre):
    try:
        return int(entrada.get())
    except ValueError:
        raise ValueError(f"{nombre} debe ser un número entero.")


def abrir_imagen():
    global img_original
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")],
    )
    if ruta:
        pil_img = Image.open(ruta).convert("RGB")
        img_original = np.array(pil_img)

        reiniciar_ajustes()
        restablecer_entradas()
        reiniciar_suma()
        mostrar_imagen(pil_img)


def cambiar_canal(event=None):
    global img_original
    if img_original is None:
        return

    opcion = combo_canales.get()

    if opcion == "Rojo":
        img_mod = lib.canal_rojo(img_original, mostrar=False)
    elif opcion == "Verde":
        img_mod = lib.canal_verde(img_original, mostrar=False)
    elif opcion == "Azul":
        img_mod = lib.canal_azul(img_original, mostrar=False)
    elif opcion == "Cyan":
        img_mod = lib.canal_cyan(img_original, mostrar=False)
    elif opcion == "Magenta":
        img_mod = lib.canal_magenta(img_original, mostrar=False)
    elif opcion == "Amarillo":
        img_mod = lib.canal_amarillo(img_original, mostrar=False)
    else:
        img_mod = img_original.copy()

    reiniciar_ajustes(mantener="canal")
    mostrar_imagen(img_mod)


def actualizar_brillo(valor_slider):
    global img_original
    if _bloqueo or img_original is None:
        return

    valor = int(float(valor_slider))
    img_modificada = lib.ajustar_brillo_general(img_original, valor=valor, mostrar=False)
    reiniciar_ajustes(mantener="brillo")
    mostrar_imagen(img_modificada)


def actualizar_brillo_canal(valor_slider=None):
    """Ajusta el brillo de un solo canal (R, G o B) con el slider."""
    global img_original
    if _bloqueo or img_original is None:
        return

    canal = {"Rojo": 0, "Verde": 1, "Azul": 2}[combo_canal_brillo.get()]
    valor = int(float(slider_brillo_canal.get()))

    img_modificada = lib.ajustar_brillo_canal(img_original, canal=canal, valor=valor, mostrar=False)
    reiniciar_ajustes(mantener="brillo_canal")
    mostrar_imagen(img_modificada)


def aplicar_binarizacion():
    global img_original
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return
    try:
        umbral = int(entrada_umbral.get())
        if not (0 <= umbral <= 255):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El umbral debe ser un número entero entre 0 y 255.")
        return

    img_modificada = lib.binarizar_imagen(img_original, umbral=umbral, mostrar=False)
    reiniciar_ajustes()
    mostrar_imagen(img_modificada)


def cambiar_escala_grises(event=None):
    global img_original
    if img_original is None:
        return

    opcion = combo_grises.get()

    if opcion == "Luminosidad":
        img_mod = lib.escala_grises_luminosidad(img_original, mostrar=False)
    elif opcion == "Tonalidad":
        img_mod = lib.escala_grises_tonalidad(img_original, mostrar=False)
    elif opcion == "Promedio":
        img_mod = lib.escala_grises_promedio(img_original, mostrar=False)
    else:
        img_mod = img_original.copy()

    reiniciar_ajustes(mantener="gris")
    mostrar_imagen(img_mod)


def reiniciar_suma():
    global img_segunda
    img_segunda = None
    lbl_imagen2.config(text="Imagen 2: ninguna cargada")

    combo_tipo_suma.current(0)
    slider_alpha.config(state="normal")
    slider_alpha.set(0.5)

    ocultar_mostrar_slider()


def ocultar_mostrar_slider(event=None):
    tipo = combo_tipo_suma.get()

    if tipo == "Suma de imágenes ponderada":
        lbl_alpha.grid()
        slider_alpha.grid()
    else:
        lbl_alpha.grid_remove()
        slider_alpha.grid_remove()

    ejecutar_suma()


def cargar_segunda_imagen():
    global img_original, img_segunda
    if img_original is None:
        messagebox.showwarning("Error", "Primero carga la imagen 1 con 'Cargar Imagen'.")
        return

    ruta = filedialog.askopenfilename(
        title="Seleccionar segunda imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")],
    )
    if ruta:
        img_segunda = np.array(Image.open(ruta).convert("RGB"))
        nombre = os.path.basename(ruta)
        lbl_imagen2.config(text=f"Imagen 2: {nombre[:25]}...")

        if combo_tipo_suma.get() == "Original":
            combo_tipo_suma.current(1)
            ocultar_mostrar_slider()
        else:
            ejecutar_suma()


def ejecutar_suma(valor_slider=None):
    global img_original, img_segunda
    if _bloqueo or img_original is None:
        return

    tipo = combo_tipo_suma.get()

    if tipo == "Original":
        img_mod = img_original.copy()
    else:
        if img_segunda is None:
            return

        if tipo == "Suma de imágenes ponderada":
            alfa = float(slider_alpha.get())
            img_mod = lib.suma_ponderada(img_original, img_segunda, alfa=alfa, mostrar=False)
        elif tipo == "Suma de imágenes":
            img_mod = lib.suma_imagenes(img_original, img_segunda, mostrar=False)

    reiniciar_ajustes()
    mostrar_imagen(img_mod)


def aplicar_inversion():
    global img_original
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return

    img_modificada = lib.invertir_imagen(img_original, mostrar=False)

    reiniciar_ajustes()
    mostrar_imagen(img_modificada)


# ---------------------------------------------------------------------------
# HISTOGRAMA
# ---------------------------------------------------------------------------
def mostrar_histograma():
    """Abre una ventana con el histograma de la imagen que se ve en el visor."""
    if img_actual is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return

    datos = lib.calcular_histograma(img_actual, mostrar=False)

    if "rojo" in datos:
        series = [("Canal Rojo", datos["rojo"], "red"),
                  ("Canal Verde", datos["verde"], "green"),
                  ("Canal Azul", datos["azul"], "blue")]
        alto_fig = 6
    else:
        series = [("Histograma en escala de grises", datos["gris"], "gray")]
        alto_fig = 4

    top = tk.Toplevel(ventana)
    top.title("Histograma de la imagen")

    fig = Figure(figsize=(8, alto_fig), dpi=100)
    for i, (titulo, valores, color) in enumerate(series, start=1):
        ax = fig.add_subplot(len(series), 1, i)
        ax.bar(np.arange(256), valores, width=1.0, color=color)
        ax.set_title(titulo, fontsize=10)
        ax.set_xlim(0, 255)
        ax.set_ylabel("Píxeles")
    fig.axes[-1].set_xlabel("Intensidad (0 - 255)")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# ---------------------------------------------------------------------------
# GEOMETRÍA: RECORTE, ZOOM, REDUCCIÓN Y ROTACIÓN
# ---------------------------------------------------------------------------
def aplicar_recorte():
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return
    try:
        x_ini = leer_entero(entrada_x_ini, "La columna inicial (X)")
        x_fin = leer_entero(entrada_x_fin, "La columna final (X)")
        y_ini = leer_entero(entrada_y_ini, "La fila inicial (Y)")
        y_fin = leer_entero(entrada_y_fin, "La fila final (Y)")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    alto, ancho = img_original.shape[:2]
    if not (0 <= x_ini < x_fin <= ancho and 0 <= y_ini < y_fin <= alto):
        messagebox.showerror(
            "Error",
            f"Coordenadas inválidas. Deben cumplir 0 ≤ inicial < final ≤ tamaño.\n"
            f"La imagen mide {ancho} x {alto} px (ancho x alto).",
        )
        return

    img_mod = lib.recortar_imagen(img_original, x_ini=x_ini, x_fin=x_fin, y_ini=y_ini, y_fin=y_fin, mostrar=False)
    reiniciar_ajustes()
    mostrar_imagen(img_mod)


def aplicar_zoom():
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return
    try:
        region = leer_entero(entrada_zoom_region, "El tamaño de la región")
        factor = leer_entero(entrada_zoom_factor, "El factor de zoom")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    if region < 2:
        messagebox.showerror("Error", "El tamaño de la región debe ser de al menos 2 px.")
        return
    if not (1 <= factor <= 10):
        messagebox.showerror("Error", "El factor de zoom debe estar entre 1 y 10.")
        return

    alto, ancho = img_original.shape[:2]
    if (min(region, ancho) * factor) * (min(region, alto) * factor) > 40_000_000:
        messagebox.showerror("Error", "El resultado sería demasiado grande. Reduce la región o el factor.")
        return

    img_mod = lib.ampliar_region(
        img_original,
        ancho_region=region,
        alto_region=region,
        zoom_factor=factor,
        mostrar=False,
    )
    reiniciar_ajustes()
    mostrar_imagen(img_mod)


def aplicar_reduccion():
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return
    try:
        factor = leer_entero(entrada_factor_red, "El factor de reducción")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    alto, ancho = img_original.shape[:2]
    if not (1 <= factor <= min(alto, ancho)):
        messagebox.showerror("Error", f"El factor debe estar entre 1 y {min(alto, ancho)}.")
        return

    img_mod = lib.reducir_resolucion(img_original, factor=factor, mostrar=False)
    reiniciar_ajustes()
    alto_r, ancho_r = img_mod.shape[:2]
    lbl_info_reduccion.config(text=f"{ancho} x {alto} px  →  {ancho_r} x {alto_r} px")
    # Se amplía solo la vista (vecino más cercano) para que se aprecien los píxeles
    mostrar_imagen(img_mod, ampliar=True)


def aplicar_rotacion():
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return
    try:
        angulo = float(entrada_angulo.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Error", "El ángulo debe ser un número (en grados, positivo = antihorario).")
        return

    img_mod = lib.rotar_imagen(img_original, angulo, mostrar=False)
    reiniciar_ajustes()
    mostrar_imagen(img_mod)


def restablecer_imagen():
    global img_original
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return

    # Reiniciar todos los controles
    reiniciar_ajustes()
    restablecer_entradas()
    reiniciar_suma()

    mostrar_imagen(img_original)


# INTERFAZ GRÁFICA (TKINTER)
BG = "#F0F0F0"
F_TITULO = ("Arial", 11, "bold")
F_TEXTO = ("Arial", 10)


def crear_titulo(padre, texto, fila, columna=0, columnspan=2, pady=(10, 0)):
    lbl = tk.Label(padre, text=texto, font=F_TITULO, bg=BG)
    lbl.grid(row=fila, column=columna, columnspan=columnspan, sticky="w", pady=pady)
    return lbl


def crear_entrada(padre, valor, ancho=6):
    entrada = tk.Entry(padre, font=F_TEXTO, width=ancho)
    entrada.insert(0, str(valor))
    return entrada


def crear_boton(padre, texto, comando, ancho=12):
    return tk.Button(padre, text=texto, font=("Arial", 10, "bold"), command=comando, width=ancho, bg="#E0E0E0")


ventana = tk.Tk()
ventana.title("Visor de Imágenes")
ventana.geometry("1350x850")
ventana.configure(bg=BG)
ventana.resizable(False, False)

# Título Superior
lbl_titulo = tk.Label(
    ventana,
    text="Visor de Imágenes",
    font=("Arial", 20, "bold"),
    fg="darkred",
    bg=BG
)
lbl_titulo.pack(pady=10)

# Contenedor Principal
frame_principal = tk.Frame(ventana, bg=BG)
frame_principal.pack(fill="both", expand=True, padx=20, pady=5)

# 1. ÁREA DE IMAGEN
frame_visor = tk.Frame(frame_principal, bg="white", width=780, height=720, relief="sunken", bd=1)
frame_visor.pack(side="left", fill="both", expand=True, padx=(0, 20))
frame_visor.pack_propagate(False)

etiqueta_imagen = tk.Label(frame_visor, bg="white")
etiqueta_imagen.pack(expand=True)

# 2. PANEL DE CONTROLES
frame_controles = tk.Frame(frame_principal, bg=BG)
frame_controles.pack(side="right", fill="both", expand=True)

# -- BOTONES CARGAR / RESTABLECER --
frame_botones = tk.Frame(frame_controles, bg=BG)
frame_botones.pack(anchor="w", pady=(0, 10))

btn_cargar = tk.Button(
    frame_botones,
    text="Cargar Imagen",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#0055B8",
    width=14,
    height=2,
    command=abrir_imagen)
btn_cargar.pack(side="left", padx=(0, 10))

btn_restablecer = tk.Button(
    frame_botones,
    text="Restablecer",
    font=("Arial", 11, "bold"),
    bg="#E0E0E0",
    width=12,
    height=2,
    command=restablecer_imagen)
btn_restablecer.pack(side="left")

# -- PESTAÑAS --
notebook = ttk.Notebook(frame_controles)
notebook.pack(fill="both", expand=True)

tab_color = tk.Frame(notebook, bg=BG, padx=10, pady=5)
tab_fusion = tk.Frame(notebook, bg=BG, padx=10, pady=5)
tab_geometria = tk.Frame(notebook, bg=BG, padx=10, pady=5)
notebook.add(tab_color, text="Color y brillo")
notebook.add(tab_fusion, text="Fusión")
notebook.add(tab_geometria, text="Geometría")

# ===========================================================================
# PESTAÑA 1: COLOR Y BRILLO
# ===========================================================================
# -- CANALES DE COLOR --
crear_titulo(tab_color, "Canales Color", 0, columnspan=1, pady=(5, 0))
combo_canales = ttk.Combobox(
    tab_color,
    values=["Original", "Rojo", "Verde", "Azul", "Cyan", "Magenta", "Amarillo"],
    state="readonly",
    width=18
)
combo_canales.grid(row=1, column=0, sticky="w", pady=(0, 10))
combo_canales.current(0)
combo_canales.bind("<<ComboboxSelected>>", cambiar_canal)

# -- ESCALA DE GRISES --
crear_titulo(tab_color, "Escala Grises", 0, columna=1, columnspan=1, pady=(5, 0))
combo_grises = ttk.Combobox(
    tab_color,
    values=["Original", "Luminosidad", "Tonalidad", "Promedio"],
    state="readonly",
    width=18
)
combo_grises.grid(row=1, column=1, sticky="w", pady=(0, 10))
combo_grises.current(0)
combo_grises.bind("<<ComboboxSelected>>", cambiar_escala_grises)

# -- BRILLO --
crear_titulo(tab_color, "Ajustar Brillo", 2, pady=(0, 0))
slider_brillo = tk.Scale(
    tab_color,
    from_=-100,
    to=100,
    orient="horizontal",
    bg=BG,
    length=300,
    command=actualizar_brillo)
slider_brillo.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 5))

# -- BRILLO POR CANAL --
crear_titulo(tab_color, "Ajustar Brillo por Canal", 4, pady=(5, 0))
combo_canal_brillo = ttk.Combobox(
    tab_color,
    values=["Rojo", "Verde", "Azul"],
    state="readonly",
    width=18
)
combo_canal_brillo.grid(row=5, column=0, sticky="w", pady=(2, 0))
combo_canal_brillo.current(0)
combo_canal_brillo.bind("<<ComboboxSelected>>", actualizar_brillo_canal)

slider_brillo_canal = tk.Scale(
    tab_color,
    from_=-100,
    to=100,
    orient="horizontal",
    bg=BG,
    length=300,
    command=actualizar_brillo_canal)
slider_brillo_canal.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 5))

# -- BINARIZACIÓN --
crear_titulo(tab_color, "Binarización", 7, pady=(5, 0))
frame_umbral = tk.Frame(tab_color, bg=BG)
frame_umbral.grid(row=8, column=0, columnspan=2, sticky="w", pady=(5, 5))

tk.Label(frame_umbral, text="Umbral:", font=F_TEXTO, bg=BG).pack(side="left")
entrada_umbral = crear_entrada(frame_umbral, 128)
entrada_umbral.pack(side="left", padx=5)
crear_boton(frame_umbral, "Aplicar", aplicar_binarizacion, ancho=10).pack(side="left", padx=10)

# -- INVERSIÓN / NEGATIVO --
crear_titulo(tab_color, "Invertir colores de la imagen", 9, pady=(5, 0))
btn_invertir = crear_boton(tab_color, "Invertir", aplicar_inversion, ancho=18)
btn_invertir.grid(row=10, column=0, columnspan=2, sticky="w", pady=(5, 5))

# -- HISTOGRAMA --
crear_titulo(tab_color, "Histograma", 11, pady=(5, 0))
btn_histograma = crear_boton(tab_color, "Ver histograma", mostrar_histograma, ancho=18)
btn_histograma.grid(row=12, column=0, columnspan=2, sticky="w", pady=(5, 5))

# ===========================================================================
# PESTAÑA 2: FUSIÓN DE IMÁGENES (SIMPLE Y PONDERADA)
# ===========================================================================
frame_suma_titulo = tk.Frame(tab_fusion, bg=BG)
frame_suma_titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(5, 0))

tk.Label(frame_suma_titulo, text="Fusión de Imágenes", font=F_TITULO, bg=BG).pack(side="left")

tk.Button(
    frame_suma_titulo,
    text="+ Img 2",
    font=("Arial", 9, "bold"),
    fg="white",
    bg="#0055B8",
    command=cargar_segunda_imagen
).pack(side="left", padx=15)

combo_tipo_suma = ttk.Combobox(
    tab_fusion,
    values=["Original", "Suma de imágenes", "Suma de imágenes ponderada"],
    state="readonly",
    width=28
)
combo_tipo_suma.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 5))
combo_tipo_suma.current(0)
combo_tipo_suma.bind("<<ComboboxSelected>>", ocultar_mostrar_slider)

lbl_imagen2 = tk.Label(tab_fusion, text="Imagen 2: ninguna", font=("Arial", 9), bg=BG)
lbl_imagen2.grid(row=2, column=0, columnspan=2, sticky="w")

lbl_alpha = tk.Label(tab_fusion, text="Alpha (peso Img 1):", font=("Arial", 9), bg=BG)
lbl_alpha.grid(row=3, column=0, columnspan=2, sticky="w")

slider_alpha = tk.Scale(
    tab_fusion,
    from_=0,
    to=1,
    resolution=0.05,
    orient="horizontal",
    bg=BG,
    length=300,
    command=ejecutar_suma
)
slider_alpha.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 10))

# ===========================================================================
# PESTAÑA 3: GEOMETRÍA
# ===========================================================================
lbl_tam_img = tk.Label(tab_geometria, text="Imagen cargada: ninguna", font=("Arial", 9), bg=BG)
lbl_tam_img.grid(row=0, column=0, sticky="w", pady=(5, 0))

# -- RECORTE --
crear_titulo(tab_geometria, "Recortar imagen", 1, columnspan=1)
frame_recorte = tk.Frame(tab_geometria, bg=BG)
frame_recorte.grid(row=2, column=0, sticky="w", pady=(3, 5))

tk.Label(frame_recorte, text="Columnas (X):", font=F_TEXTO, bg=BG).grid(row=0, column=0, sticky="w")
entrada_x_ini = crear_entrada(frame_recorte, 50)
entrada_x_ini.grid(row=0, column=1, padx=5)
tk.Label(frame_recorte, text="a", font=F_TEXTO, bg=BG).grid(row=0, column=2)
entrada_x_fin = crear_entrada(frame_recorte, 600)
entrada_x_fin.grid(row=0, column=3, padx=5)

tk.Label(frame_recorte, text="Filas (Y):", font=F_TEXTO, bg=BG).grid(row=1, column=0, sticky="w", pady=(4, 0))
entrada_y_ini = crear_entrada(frame_recorte, 200)
entrada_y_ini.grid(row=1, column=1, padx=5, pady=(4, 0))
tk.Label(frame_recorte, text="a", font=F_TEXTO, bg=BG).grid(row=1, column=2, pady=(4, 0))
entrada_y_fin = crear_entrada(frame_recorte, 800)
entrada_y_fin.grid(row=1, column=3, padx=5, pady=(4, 0))

crear_boton(frame_recorte, "Recortar", aplicar_recorte, ancho=10).grid(row=0, column=4, rowspan=2, padx=10)

# -- ZOOM --
crear_titulo(tab_geometria, "Ampliar región (Zoom)", 3, columnspan=1)
frame_zoom = tk.Frame(tab_geometria, bg=BG)
frame_zoom.grid(row=4, column=0, sticky="w", pady=(3, 5))

tk.Label(frame_zoom, text="Región central (px):", font=F_TEXTO, bg=BG).grid(row=0, column=0, sticky="w")
entrada_zoom_region = crear_entrada(frame_zoom, 500)
entrada_zoom_region.grid(row=0, column=1, padx=5)

tk.Label(frame_zoom, text="Factor de zoom:", font=F_TEXTO, bg=BG).grid(row=1, column=0, sticky="w", pady=(4, 0))
entrada_zoom_factor = crear_entrada(frame_zoom, 5)
entrada_zoom_factor.grid(row=1, column=1, padx=5, pady=(4, 0))

crear_boton(frame_zoom, "Ampliar", aplicar_zoom, ancho=10).grid(row=0, column=2, rowspan=2, padx=10)

# -- REDUCCIÓN DE RESOLUCIÓN --
crear_titulo(tab_geometria, "Reducir resolución", 5, columnspan=1)
frame_reduccion = tk.Frame(tab_geometria, bg=BG)
frame_reduccion.grid(row=6, column=0, sticky="w", pady=(3, 0))

tk.Label(frame_reduccion, text="Factor f:", font=F_TEXTO, bg=BG).pack(side="left")
entrada_factor_red = crear_entrada(frame_reduccion, 4)
entrada_factor_red.pack(side="left", padx=5)
crear_boton(frame_reduccion, "Reducir", aplicar_reduccion, ancho=10).pack(side="left", padx=10)

lbl_info_reduccion = tk.Label(tab_geometria, text="", font=("Arial", 9), bg=BG)
lbl_info_reduccion.grid(row=7, column=0, sticky="w", pady=(0, 5))

# -- ROTACIÓN --
crear_titulo(tab_geometria, "Rotar imagen", 8, columnspan=1)
frame_rotar = tk.Frame(tab_geometria, bg=BG)
frame_rotar.grid(row=9, column=0, sticky="w", pady=(3, 5))

tk.Label(frame_rotar, text="Ángulo (°):", font=F_TEXTO, bg=BG).pack(side="left")
entrada_angulo = crear_entrada(frame_rotar, 45)
entrada_angulo.pack(side="left", padx=5)
crear_boton(frame_rotar, "Rotar", aplicar_rotacion, ancho=10).pack(side="left", padx=10)
tk.Label(tab_geometria, text="Positivo = antihorario", font=("Arial", 9), bg=BG).grid(row=10, column=0, sticky="w")

reiniciar_suma()

ventana.mainloop()