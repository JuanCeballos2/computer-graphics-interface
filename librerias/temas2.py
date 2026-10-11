import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import librerias as lib

img_original = None  # Variable global que almacenará el arreglo de NumPy

def mostrar_imagen(img_input):
    """
    Recibe una imagen (PIL Image o NumPy ndarray)
    y la despliega en el contenedor principal escalándola para ocupar el espacio.
    """
    if isinstance(img_input, np.ndarray):
        img_pil = Image.fromarray(img_input)
    else:
        img_pil = img_input

    img_pil.thumbnail((680, 450))
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
        mostrar_imagen(pil_img)

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


ventana = tk.Tk()
ventana.title("Visor de Imágenes")
ventana.geometry("1000x550")
ventana.configure(bg="#F0F0F0")
ventana.resizable(False, False)

# Título Superior
lbl_titulo = tk.Label(
    ventana,
    text="Visor de Imágenes",
    font=("Arial", 18, "bold"),
    fg="darkred",
    bg="#F0F0F0"
)
lbl_titulo.pack(pady=10)

# Contenedor Principal (Visor a la izquierda | Panel de Controles a la derecha)
frame_principal = tk.Frame(ventana, bg="#F0F0F0")
frame_principal.pack(fill="both", expand=True, padx=20, pady=10)

# 1. ÁREA DE IMAGEN
frame_visor = tk.Frame(frame_principal, bg="white", width=700, height=460, relief="sunken", bd=1)
frame_visor.pack(side="left", fill="both", expand=True, padx=(0, 20))
frame_visor.pack_propagate(False)

etiqueta_imagen = tk.Label(frame_visor, bg="white")
etiqueta_imagen.pack(expand=True)

# 2. PANEL DE CONTROLES
frame_controles = tk.Frame(frame_principal, bg="#F0F0F0", width=220)
frame_controles.pack(side="right", fill="y", padx=5)

# Botón Cargar Imagen
btn_cargar = tk.Button(
    frame_controles,
    text="Cargar Imagen",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#0055B8",
    width=18,
    height=2,
    command=abrir_imagen
)
btn_cargar.pack(pady=(10, 25))

# Control de Brillo
lbl_brillo = tk.Label(frame_controles, text="Ajustar Brillo", font=("Arial", 11, "bold"), bg="#F0F0F0")
lbl_brillo.pack(anchor="w")

slider_brillo = tk.Scale(
    frame_controles,
    from_=-100,
    to=100,
    orient="horizontal",
    bg="#F0F0F0",
    length=200,
    command=actualizar_brillo
)
slider_brillo.pack(pady=(0, 25))

# Control de Binarización
lbl_binarizar = tk.Label(frame_controles, text="Binarización", font=("Arial", 11, "bold"), bg="#F0F0F0")
lbl_binarizar.pack(anchor="w")

frame_umbral = tk.Frame(frame_controles, bg="#F0F0F0")
frame_umbral.pack(fill="x", pady=5)

lbl_umbral = tk.Label(frame_umbral, text="Umbral:", font=("Arial", 10), bg="#F0F0F0")
lbl_umbral.pack(side="left")

entrada_umbral = tk.Entry(frame_umbral, font=("Arial", 10), width=8)
entrada_umbral.pack(side="right")
entrada_umbral.insert(0, "128")

btn_binarizar = tk.Button(
    frame_controles,
    text="Binarizar",
    font=("Arial", 10, "bold"),
    command=aplicar_binarizacion,
    width=18,
    bg="#E0E0E0"
)
btn_binarizar.pack(pady=10)

ventana.mainloop()