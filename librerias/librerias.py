import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def _obtener_valor_maximo(imagen):
    if np.issubdtype(imagen.dtype, np.integer):
        return np.iinfo(imagen.dtype).max
    else:
        return 1.0

    
def canal_rojo(imagen, mostrar=True):
    capaR = np.copy(imagen)
    capaR[:, :, 1] = capaR[:, :, 2] = 0  
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capaR)
        plt.axis("off")
        plt.title("Imagen cargada a rojo")
        plt.tight_layout()
        plt.show()
        
    return capaR


def canal_verde(imagen, mostrar=True):
    capaG = np.copy(imagen)
    capaG[:, :, 0] = capaG[:, :, 2] = 0  
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capaG)
        plt.axis("off")
        plt.title("Imagen cargada a verde")
        plt.tight_layout()
        plt.show()
        
    return capaG


def canal_azul(imagen, mostrar=True):
    capaB = np.copy(imagen)
    capaB[:, :, 0] = capaB[:, :, 1] = 0  
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capaB)
        plt.axis("off")
        plt.title("Imagen cargada a azul")
        plt.tight_layout()
        plt.show()
        
    return capaB

def canal_magenta(imagen, mostrar=True):
    capaM = np.copy(imagen)
    capaM[:, :, 0] = capaM[:, :, 2] = 255  
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capaM)
        plt.axis("off")
        plt.title("Imagen cargada a magenta")
        plt.tight_layout()
        plt.show()
        
    return capaM


def canal_cyan(imagen, mostrar=True):
    capaC = np.copy(imagen)
    capaC[:, :, 1] = capaC[:, :, 2] = 255  
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capaC)
        plt.axis("off")
        plt.title("Imagen cargada a cyan")
        plt.tight_layout()
        plt.show()
        
    return capaC


def canal_amarillo(imagen, mostrar=True):
    capaA = np.copy(imagen)
    capaA[:, :, 0] = capaA[:, :, 1] = 255 
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capaA)
        plt.axis("off")
        plt.title("Imagen cargada a amarillo")
        plt.tight_layout()
        plt.show()
        
    return capaA

def invertir_imagen(imagen, mostrar=True):
    capa_inv = np.copy(imagen)
    val_max = _obtener_valor_maximo(imagen)

    capa_inv[:, :, :3] = val_max - capa_inv[:, :, :3]
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(capa_inv)
        plt.axis("off")
        plt.title("Imagen invertida")
        plt.tight_layout()
        plt.show()
        
    return capa_inv

def suma_ponderada(imagen1, imagen2, alfa=0.5, mostrar=True):
    h, w = imagen1.shape[0], imagen1.shape[1]

    img2_pil = Image.fromarray((imagen2 * (255 if imagen2.dtype == np.float32 or imagen2.dtype == np.float64 else 1)).astype(np.uint8))
    img2_resized = np.array(img2_pil.resize((w, h)))
    
    val_max = _obtener_valor_maximo(imagen1)
    
    img1_f = imagen1.astype(np.float32)
    img2_f = img2_resized.astype(np.float32)
    
    fusion = (img1_f * alfa) + (img2_f * (1.0 - alfa))
    
    fusion = np.clip(fusion, 0, val_max).astype(imagen1.dtype)
    
    if mostrar:
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        plt.imshow(imagen1)
        plt.axis("off")
        plt.title("Imagen 1")

        plt.subplot(1, 3, 2)
        plt.imshow(img2_resized)
        plt.axis("off")
        plt.title("Imagen 2 (Ajustada)")

        plt.subplot(1, 3, 3)
        plt.imshow(fusion)
        plt.axis("off")
        plt.title(f"Suma ponderada alpha = {alfa}") 

        plt.tight_layout()
        plt.show()
        
    return fusion

def suma_imagenes(imagen1, imagen2, mostrar=True):
    h, w = imagen1.shape[0], imagen1.shape[1]
    
    if np.issubdtype(imagen2.dtype, np.floating):
        img2_pil = Image.fromarray((imagen2 * 255).astype(np.uint8))
    else:
        img2_pil = Image.fromarray(imagen2.astype(np.uint8))
        
    img2_resized = np.array(img2_pil.resize((w, h)))
    
    val_max = _obtener_valor_maximo(imagen1)
    
    A = imagen1.astype(np.float32)
    B = img2_resized.astype(np.float32)

    fusion = (A + B) // 2 
    fusion = np.clip(fusion, 0, val_max).astype(imagen1.dtype)

    if mostrar:
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 3, 1)
        plt.imshow(imagen1)
        plt.axis("off")
        plt.title("Imagen 1")

        plt.subplot(1, 3, 2)
        plt.imshow(img2_resized)
        plt.axis("off")
        plt.title("Imagen 2 (Ajustada)")

        plt.subplot(1, 3, 3)
        plt.imshow(fusion)
        plt.axis("off")
        plt.title("Suma de matrices") 

        plt.tight_layout()
        plt.show()
        
    return fusion

def escala_grises_tonalidad(imagen, mostrar=True):

    img_f = imagen.astype(np.float32)
    val_max = _obtener_valor_maximo(imagen)
    
    max_c = np.max(img_f[:, :, :3], axis=2)
    min_c = np.min(img_f[:, :, :3], axis=2)
    
    gris = (max_c + min_c) / 2.0
    gris = np.clip(gris, 0, val_max).astype(imagen.dtype)
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(gris, cmap="gray")
        plt.axis("off")
        plt.title("Escala de grises (Tonalidad)")
        plt.tight_layout()
        plt.show()
        
    return gris

def escala_grises_luminosidad(imagen, mostrar=True):

    img_f = imagen.astype(np.float32)
    val_max = _obtener_valor_maximo(imagen)
    
    gris = 0.299 * img_f[:, :, 0] + 0.587 * img_f[:, :, 1] + 0.114 * img_f[:, :, 2]
    gris = np.clip(gris, 0, val_max).astype(imagen.dtype)
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(gris, cmap="gray")
        plt.axis("off")
        plt.title("Escala de grises (Luminosidad)")
        plt.tight_layout()
        plt.show()
        
    return gris

def escala_grises_promedio(imagen, mostrar=True):

    img_f = imagen.astype(np.float32)
    val_max = _obtener_valor_maximo(imagen)
    
    gris = (img_f[:, :, 0] + img_f[:, :, 1] + img_f[:, :, 2]) / 3.0
    gris = np.clip(gris, 0, val_max).astype(imagen.dtype)
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(gris, cmap="gray")
        plt.axis("off")
        plt.title("Escala de grises (Promedio)")
        plt.tight_layout()
        plt.show()
        
    return gris

def ajustar_brillo_general(imagen, valor=0, mostrar=True):
    val_max = _obtener_valor_maximo(imagen)

    factor = valor if np.issubdtype(imagen.dtype, np.integer) else (valor / 255.0)
    
    img_f = imagen.astype(np.float32)
    img_brillo = np.clip(img_f + factor, 0, val_max).astype(imagen.dtype)
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(img_brillo)
        plt.axis("off")
        plt.title(f"Brillo ajustado ({' + ' if valor >= 0 else ''}{valor})")
        plt.tight_layout()
        plt.show()
        
    return img_brillo


def ajustar_brillo_canal(imagen, canal=0, valor=60, mostrar=True):
    """
    Ajusta el brillo de un solo canal de color (0: Rojo, 1: Verde, 2: Azul).
    
    Parámetros:
    - imagen: Imagen de entrada.
    - canal: Índice del canal a modificar (0=Rojo, 1=Verde, 2=Azul).
    - valor: Cantidad de brillo a sumar o restar.
    - mostrar: Muestra la comparación gráfica si es True.
    """
    val_max = _obtener_valor_maximo(imagen)
    factor = valor if np.issubdtype(imagen.dtype, np.integer) else (valor / 255.0)
    
    nombres_canales = {0: "Rojo", 1: "Verde", 2: "Azul"}
    
    img_brillo = imagen.copy().astype(np.float32)
    img_brillo[:, :, canal] = np.clip(img_brillo[:, :, canal] + factor, 0, val_max)
    img_brillo = img_brillo.astype(imagen.dtype)
    
    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(img_brillo)
        plt.axis("off")
        plt.title(f"Brillo canal {nombres_canales.get(canal, canal)} ({' + ' if valor >= 0 else ''}{valor})")
        plt.tight_layout()
        plt.show()
        
    return img_brillo

def binarizar_imagen(imagen, umbral=128, mostrar=True):
    val_max = _obtener_valor_maximo(imagen)
    
    if len(imagen.shape) == 3 and imagen.shape[2] >= 3:
        img_f = imagen.astype(np.float32)
        gris = 0.299 * img_f[:, :, 0] + 0.587 * img_f[:, :, 1] + 0.114 * img_f[:, :, 2]
    else:
        gris = imagen.astype(np.float32)

    T = umbral if np.issubdtype(imagen.dtype, np.integer) else (umbral / 255.0)
    
    img_binaria = np.where(gris > T, val_max, 0).astype(imagen.dtype)

    if mostrar:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(img_binaria, cmap="gray")
        plt.axis("off")
        plt.title(f"Imagen Binaria (T={umbral})")
        plt.tight_layout()
        plt.show()
        
    return img_binaria

def recortar_imagen(imagen, x_ini=210, x_fin=600, y_ini=200, y_fin=500, mostrar=True):

    if len(imagen.shape) == 3:
        img_recortada = imagen[y_ini:y_fin, x_ini:x_fin, :]
    else:
        img_recortada = imagen[y_ini:y_fin, x_ini:x_fin]
        
    if mostrar:
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        plt.imshow(imagen)
        plt.axis("on")  
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(img_recortada)
        plt.axis("on")
        plt.title(f"Imagen Recortada [{y_ini}:{y_fin}, {x_ini}:{x_fin}]")
        
        plt.tight_layout()
        plt.show()
        
    return img_recortada


def rotar_imagen(imagen, ang_deg, fondo=0, interpolacion=cv2.INTER_NEAREST, mostrar=True):
    H, W = imagen.shape[:2]
    centro = ((W - 1) / 2.0, (H - 1) / 2.0)

    M = cv2.getRotationMatrix2D(centro, ang_deg, 1.0)

    cos_t, sin_t = abs(M[0, 0]), abs(M[0, 1])
    out_W = int(np.ceil(H * sin_t + W * cos_t))
    out_H = int(np.ceil(H * cos_t + W * sin_t))

    M[0, 2] += (out_W - 1) / 2.0 - centro[0]
    M[1, 2] += (out_H - 1) / 2.0 - centro[1]

    rotada = cv2.warpAffine(
        imagen,
        M,
        (out_W, out_H),
        flags=interpolacion,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(fondo, fondo, fondo, fondo),
    )

    if mostrar:
        plt.figure(figsize=(10, 4))

        plt.subplot(1, 2, 1)
        plt.imshow(imagen, cmap="gray" if imagen.ndim == 2 else None)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(rotada, cmap="gray" if rotada.ndim == 2 else None)
        plt.axis("off")
        plt.title(f"Imagen rotada ({ang_deg}°)")

        plt.tight_layout()
        plt.show()

    return rotada

def reducir_resolucion(imagen, factor=4, mostrar=True):
    if len(imagen.shape) == 3:
        img_reducida = imagen[::factor, ::factor, :]
    else:
        img_reducida = imagen[::factor, ::factor]
        
    print("Tamaño original:", imagen.shape)
    print("Tamaño reducido:", img_reducida.shape)
    
    if mostrar:
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        plt.imshow(imagen, cmap="gray" if imagen.ndim == 2 else None)
        plt.axis("off")
        plt.title("Imagen original")

        plt.subplot(1, 2, 2)
        plt.imshow(img_reducida, cmap="gray" if img_reducida.ndim == 2 else None)
        plt.axis("off")
        plt.title(f"Imagen Reducida (Factor 1/{factor})")
        
        plt.tight_layout()
        plt.show()
        
    return img_reducida

def ampliar_region(imagen, centro_x=None, centro_y=None, ancho_region=100, alto_region=100, zoom_factor=4, mostrar=True):
    h, w = imagen.shape[:2]
    
    if centro_x is None:
        centro_x = w // 2
    if centro_y is None:
        centro_y = h // 2
        
    start_col = max(0, centro_x - ancho_region // 2)
    end_col = min(w, centro_x + ancho_region // 2)
    start_row = max(0, centro_y - alto_region // 2)
    end_row = min(h, centro_y + alto_region // 2)
    
    recorte = imagen[start_row:end_row, start_col:end_col]
    
    if recorte.ndim == 3:
        matriz_zoom = np.ones((zoom_factor, zoom_factor, 1))
    else:
        matriz_zoom = np.ones((zoom_factor, zoom_factor))
        
    zoomed = np.kron(recorte, matriz_zoom)
    zoomed = np.clip(zoomed, 0, _obtener_valor_maximo(imagen)).astype(imagen.dtype)
    
    if mostrar:
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 2, 1)
        plt.imshow(imagen, cmap="gray" if imagen.ndim == 2 else None)

        rect_x = [start_col, end_col, end_col, start_col, start_col]
        rect_y = [start_row, start_row, end_row, end_row, start_row]
        plt.plot(rect_x, rect_y, color="red", linewidth=1.5)
        plt.axis("off")
        plt.title("Imagen original (Área en rojo)")

        plt.subplot(1, 2, 2)
        plt.imshow(zoomed, cmap="gray" if zoomed.ndim == 2 else None)
        plt.axis("off")
        plt.title(f"Región ampliada (Zoom x{zoom_factor})")
        
        plt.tight_layout()
        plt.show()
        
    return zoomed

def calcular_histograma(imagen, mostrar=True):
    img_temp = np.copy(imagen)
    
    if np.issubdtype(img_temp.dtype, np.floating) or img_temp.max() <= 1.0:
        img_temp = (img_temp * 255).astype(np.uint8)
    else:
        img_temp = img_temp.astype(np.uint8)
        
    hist_datos = {}

    if len(img_temp.shape) == 3 and img_temp.shape[2] >= 3:
        R = img_temp[:, :, 0]
        G = img_temp[:, :, 1]
        B = img_temp[:, :, 2]
        
        hist_datos["rojo"] = np.histogram(R, bins=256, range=(0, 256))[0]
        hist_datos["verde"] = np.histogram(G, bins=256, range=(0, 256))[0]
        hist_datos["azul"] = np.histogram(B, bins=256, range=(0, 256))[0]

        if mostrar:
            plt.figure(figsize=(10, 6))

            plt.subplot(3, 1, 1)
            plt.hist(R.ravel(), bins=256, range=(0, 256), color='red', alpha=0.7)
            plt.title("Histograma canal rojo")
            plt.xlim([0, 256])

            plt.subplot(3, 1, 2)
            plt.hist(G.ravel(), bins=256, range=(0, 256), color='green', alpha=0.7)
            plt.title("Histograma canal verde")
            plt.xlim([0, 256])

            plt.subplot(3, 1, 3)
            plt.hist(B.ravel(), bins=256, range=(0, 256), color='blue', alpha=0.7)
            plt.title("Histograma canal azul")
            plt.xlim([0, 256])

            plt.tight_layout()
            plt.show()

    else:
        hist_datos["gris"] = np.histogram(img_temp, bins=256, range=(0, 256))[0]

        if mostrar:
            plt.figure(figsize=(8, 4))
            plt.hist(img_temp.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.8)
            plt.title("Histograma en escala de grises")
            plt.xlim([0, 256])
            plt.tight_layout()
            plt.show()

    return hist_datos
def segmentar_hsv(imagen, lower_color=(5, 100, 100), upper_color=(25, 255, 255), es_bgr=False, mostrar=True):
    if es_bgr:
        img_bgr = np.copy(imagen)
        img_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    else:
        img_temp = np.copy(imagen)
        # Corregido: evaluamos img_temp, no img_rgb
        if np.issubdtype(img_temp.dtype, np.floating) or img_temp.max() <= 1.0:
            img_temp = (img_temp * 255).astype(np.uint8)
        
        # Ahora sí asignamos img_rgb para que el resto del código funcione
        img_rgb = img_temp
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))
    seg_color_bgr = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
    seg_color_rgb = cv2.cvtColor(seg_color_bgr, cv2.COLOR_BGR2RGB)

    if mostrar:
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 3, 1)
        plt.title("Imagen original")
        plt.imshow(img_rgb)
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.title("Mascara del color")
        plt.imshow(mask, cmap="gray")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.title("Segmentacion color")
        plt.imshow(seg_color_rgb)
        plt.axis("off")

        plt.tight_layout()
        plt.show()

    return mask, seg_color_rgb