import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import librerias as lib

img_original = None  # Variable global que almacenará el arreglo de NumPy
img_segunda = None   # Segunda imagen (arreglo NumPy) para la suma ponderada

def mostrar_imagen(img_input):
    if isinstance(img_input, np.ndarray):
        img_pil = Image.fromarray(img_input)
    else:
        img_pil = img_input

    img_pil.thumbnail((750, 700))
    img_tk = ImageTk.PhotoImage(img_pil)
    
    etiqueta_imagen.config(image=img_tk)
    etiqueta_imagen.image = img_tk 

def abrir_imagen():
    global img_original
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")],
    )
    if ruta:
        pil_img = Image.open(ruta).convert("RGB")
        img_original = np.array(pil_img)

        slider_brillo.set(0)
        combo_canales.current(0)
        combo_grises.current(0)
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

    slider_brillo.set(0)
    combo_grises.current(0)
    mostrar_imagen(img_mod)

def actualizar_brillo(valor_slider):
    global img_original
    if img_original is None:
        return
    
    valor = int(float(valor_slider))
    img_modificada = lib.ajustar_brillo_general(img_original, valor=valor, mostrar=False)
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
    mostrar_imagen(img_modificada)

def cambiar_escala_grises(event=None):
    global img_original
    if img_original is None:
        return
    
    opcion = combo_grises.get()
    combo_canales.current(0)
    
    if opcion == "Luminosidad":
        img_mod = lib.escala_grises_luminosidad(img_original, mostrar=False)
    elif opcion == "Tonalidad":
        img_mod = lib.escala_grises_tonalidad(img_original, mostrar=False)
    elif opcion == "Promedio":
        img_mod = lib.escala_grises_promedio(img_original, mostrar=False)
    else:
        img_mod = img_original.copy()
        
    slider_brillo.set(0)
    combo_canales.current(0)
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
    if img_original is None:
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

    combo_canales.current(0)
    combo_grises.current(0)
    slider_brillo.set(0)
    mostrar_imagen(img_mod)


def aplicar_inversion():
    global img_original
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return

    img_modificada = lib.invertir_imagen(img_original, mostrar=False)

    combo_canales.current(0)
    combo_grises.current(0)
    slider_brillo.set(0)
    
    mostrar_imagen(img_modificada)

def restablecer_imagen():
    global img_original
    if img_original is None:
        messagebox.showwarning("Error", "No se ha cargado ninguna imagen.")
        return
 
    # Reiniciar todos los controles
    slider_brillo.set(0)
    combo_canales.current(0)
    combo_grises.current(0)
    entrada_umbral.delete(0, "end")
    entrada_umbral.insert(0, "128")
    reiniciar_suma()
 
    mostrar_imagen(img_original)

# INTERFAZ GRÁFICA (TKINTER)
ventana = tk.Tk()
ventana.title("Visor de Imágenes")
ventana.geometry("1350x850")
ventana.configure(bg="#F0F0F0")
ventana.resizable(False, False)

# Título Superior
lbl_titulo = tk.Label(
    ventana,
    text="Visor de Imágenes",
    font=("Arial", 20, "bold"),
    fg="darkred",
    bg="#F0F0F0"
)
lbl_titulo.pack(pady=10)

# Contenedor Principal 
frame_principal = tk.Frame(ventana, bg="#F0F0F0")
frame_principal.pack(fill="both", expand=True, padx=20, pady=5)

# 1. ÁREA DE IMAGEN
frame_visor = tk.Frame(frame_principal, bg="white", width=780, height=720, relief="sunken", bd=1)
frame_visor.pack(side="left", fill="both", expand=True, padx=(0, 20))
frame_visor.pack_propagate(False)

etiqueta_imagen = tk.Label(frame_visor, bg="white")
etiqueta_imagen.pack(expand=True)

# 2. PANEL DE CONTROLES 
frame_controles = tk.Frame(frame_principal, bg="#F0F0F0")
frame_controles.pack(side="right", fill="both", expand=True)

# -- BOTONES CARGAR / RESTABLECER --
frame_botones = tk.Frame(frame_controles, bg="#F0F0F0")
frame_botones.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")
 
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

# -- CANALES DE COLOR --
lbl_canales = tk.Label(
    frame_controles, 
    text="Canales Color", 
    font=("Arial", 11, "bold"), 
    bg="#F0F0F0"
)
lbl_canales.grid(row=1, column=0, sticky="w", pady=(5,0))
combo_canales = ttk.Combobox(
    frame_controles, 
    values=["Original", "Rojo", "Verde", "Azul", "Cyan", "Magenta", "Amarillo"], 
    state="readonly", 
    width=18
)
combo_canales.grid(row=2, column=0, sticky="w", pady=(0, 15))
combo_canales.current(0)
combo_canales.bind("<<ComboboxSelected>>", cambiar_canal)

# -- BRILLO --
lbl_brillo = tk.Label(
    frame_controles, 
    text="Ajustar Brillo", 
    font=("Arial", 11, "bold"), 
    bg="#F0F0F0")
lbl_brillo.grid(row=3, column=0, columnspan=2, sticky="w")
slider_brillo = tk.Scale(
    frame_controles, 
    from_=-100, 
    to=100, 
    orient="horizontal", 
    bg="#F0F0F0", 
    length=300, 
    command=actualizar_brillo)
slider_brillo.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 15))


# -- BINARIZACIÓN --
lbl_binarizar = tk.Label(
    frame_controles, 
    text="Binarización", 
    font=("Arial", 11, "bold"), 
    bg="#F0F0F0"
)
lbl_binarizar.grid(row=5, column=0, columnspan=2, sticky="w")

frame_umbral = tk.Frame(
    frame_controles, 
    bg="#F0F0F0"
)
frame_umbral.grid(
    row=6, 
    column=0, 
    columnspan=2, 
    sticky="w", 
    pady=(5, 15)
)

tk.Label(
    frame_umbral,  
    text="Umbral:", 
    font=("Arial", 10), 
    bg="#F0F0F0").pack(side="left")

entrada_umbral = tk.Entry(
    frame_umbral, 
    font=("Arial", 10), 
    width=6
)
entrada_umbral.pack(side="left", padx=5)
entrada_umbral.insert(0, "128")
tk.Button(
    frame_umbral, 
    text="Aplicar", 
    font=("Arial", 10, "bold"), 
    command=aplicar_binarizacion, 
    width=10, 
    bg="#E0E0E0"
).pack(side="left", padx=10)


# -- ESCALA DE GRISES --
lbl_grises = tk.Label(
    frame_controles, 
    text="Escala Grises", 
    font=("Arial", 11, "bold"), 
    bg="#F0F0F0"
)
lbl_grises.grid(row=1, column=1, sticky="w", pady=(5,0))

combo_grises = ttk.Combobox(
    frame_controles, 
    values=["Original", "Luminosidad", "Tonalidad", "Promedio"], 
    state="readonly", 
    width=18
)
combo_grises.grid(row=2, column=1, sticky="w", pady=(0, 15))
combo_grises.current(0)
combo_grises.bind("<<ComboboxSelected>>", cambiar_escala_grises)

# -- FUSIÓN DE IMÁGENES (SIMPLE Y PONDERADA) --
frame_suma_titulo = tk.Frame(frame_controles, bg="#F0F0F0")
frame_suma_titulo.grid(row=9, column=0, columnspan=2, sticky="w", pady=(5, 0))

tk.Label(
    frame_suma_titulo, 
    text="Fusión de Imágenes", 
    font=("Arial", 11, "bold"), 
    bg="#F0F0F0"
).pack(side="left")

tk.Button(
    frame_suma_titulo, 
    text="+ Img 2", 
    font=("Arial", 9, "bold"), 
    fg="white", 
    bg="#0055B8", 
    command=cargar_segunda_imagen
).pack(side="left", padx=15)

combo_tipo_suma = ttk.Combobox(
    frame_controles, 
    values=["Original", "Suma de imágenes", "Suma de imágenes ponderada"], 
    state="readonly", 
    width=28
)
combo_tipo_suma.grid(row=10, column=0, columnspan=2, sticky="w", pady=(5, 5))
combo_tipo_suma.current(0)
combo_tipo_suma.bind("<<ComboboxSelected>>", ocultar_mostrar_slider)

lbl_imagen2 = tk.Label(frame_controles, text="Imagen 2: ninguna", font=("Arial", 9), bg="#F0F0F0")
lbl_imagen2.grid(row=11, column=0, columnspan=2, sticky="w")

lbl_alpha = tk.Label(
    frame_controles, 
    text="Alpha (peso Img 1):", 
    font=("Arial", 9), 
    bg="#F0F0F0"
)
lbl_alpha.grid(row=12, column=0, columnspan=2, sticky="w")

slider_alpha = tk.Scale(
    frame_controles, 
    from_=0, 
    to=1, 
    resolution=0.05, 
    orient="horizontal", 
    bg="#F0F0F0", 
    length=300, 
    command=ejecutar_suma
)
slider_alpha.grid(row=13, column=0, columnspan=2, sticky="w", pady=(0, 10))

reiniciar_suma()

# -- INVERSIÓN / NEGATIVO --
lbl_invertir = tk.Label(
    frame_controles, 
    text="Invertir colores de la imagen", 
    font=("Arial", 11, "bold"), 
    bg="#F0F0F0"
)
lbl_invertir.grid(row=16, column=0, columnspan=2, sticky="w", pady=(10, 0))

btn_invertir = tk.Button(
    frame_controles, 
    text="Invertir", 
    font=("Arial", 10, "bold"), 
    command=aplicar_inversion, 
    bg="#E0E0E0", 
    width=18
)
btn_invertir.grid(row=17, column=0, columnspan=2, sticky="w", pady=(5, 15))

ventana.mainloop()