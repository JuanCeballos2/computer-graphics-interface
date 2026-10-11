import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import librerias as lib

img_original = None  # Variable global que almacenará el arreglo de NumPy

def mostrar_imagen(img_input):
    """
    Recibe una imagen (ya sea PIL Image o NumPy ndarray) 
    y la despliega en el etiqueta_imagen de Tkinter.
    """
    # Si viene como matriz de NumPy, la convertimos a PIL Image
    if isinstance(img_input, np.ndarray):
        img_pil = Image.fromarray(img_input)
    else:
        img_pil = img_input

    img_redimensionada = img_pil.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img_redimensionada)
    etiqueta_imagen.config(image=img_tk)
    etiqueta_imagen.image = img_tk  # Guardar referencia para evitar Garbage Collection

def abrir_imagen():
    global img_original
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")],
    )
    if ruta:
        # 1. Cargar imagen con PIL
        pil_img = Image.open(ruta).convert("RGB")
        
        # 2. Guardar en la variable global como matriz NumPy para la librería
        img_original = np.array(pil_img)
        
        # 3. Mostrar la imagen cargada
        mostrar_imagen(pil_img)

def actualizar_brillo(valor_slider):
    global img_original
    if img_original is None:
        return
    
    valor = int(valor_slider)
    
    # Pasamos mostrar=False para evitar que abra ventanas emergentes de Matplotlib
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

    # Pasamos mostrar=False
    img_modificada = lib.binarizar_imagen(img_original, umbral=umbral, mostrar=False)
    
    mostrar_imagen(img_modificada)

# -----------------------------------------------------------------
# INTERFAZ GRÁFICA (TKINTER)
# -----------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Ventana de Ejemplo")
ventana.geometry("1000x500")
ventana.configure(bg="lightblue")
ventana.resizable(False, False)

etiqueta = tk.Label(
    ventana,
    text="Imagen de ejemplo",
    font=("Arial", 16, "bold"),
    fg="black",
    bg="white",
    width=20,
    height=1,
)
etiqueta.place(x=350, y=50)

etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.place(x=350, y=200)

boton = tk.Button(
    ventana,
    text="Subir una imagen",
    font=("Arial", 14),
    fg="white",
    bg="blue",
    width=20,
    height=2,
    command=abrir_imagen,
)
boton.place(x=350, y=100)

# Slider para Ajuste de Brillo
slider_brillo = tk.Scale(
    ventana,
    from_=-100,
    to=100,
    orient="horizontal",
    label="Ajustar Brillo",
    bg="gray",
    command=actualizar_brillo,
)
slider_brillo.place(x=350, y=420)

# Entrada y botón para Binarización
lbl_umbral = tk.Label(ventana, text="Umbral", font=("Arial", 14), fg="black", bg="lightblue")
lbl_umbral.place(x=900, y=350)

entrada_umbral = tk.Entry(ventana, font=("Arial", 14), width=10)
entrada_umbral.place(x=900, y=380)
entrada_umbral.insert(0, "128")

btn_binarizar = tk.Button(
    ventana,
    text="Binarizar",
    command=aplicar_binarizacion,
    font=("Arial", 14),
)
btn_binarizar.place(x=900, y=420)

ventana.mainloop()