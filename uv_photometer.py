import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import math


def select_image():
    """Open a file dialog and return the selected image path."""
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
    )
    return path


def brightest_pixel(image_path):
    """Return the coordinates and value of the brightest pixel in the image."""
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    arr = np.array(img)

    # Coordinates of max brightness
    y, x = np.unravel_index(arr.argmax(), arr.shape)
    brightness = arr[y, x]

    return x, y, brightness


def run():
    """Select two images, compute brightest pixels, and calculate absorbance."""
    path1 = select_image()
    path2 = select_image()

    x1, y1, I0 = brightest_pixel(path1)   # intensity without sample
    x2, y2, I  = brightest_pixel(path2)   # intensity with sample

    # Avoid division by zero
    if I == 0:
        absorbance = float('inf')
    else:
        absorbance = math.log10(I0 / I)

    result = f"""
Image 1 (I₀):
  Brightest pixel → (x={x1}, y={y1}), value={I0}

Image 2 (I):
  Brightest pixel → (x={x2}, y={y2}), value={I}

Absorbance:
  A = log10(I₀ / I) = {absorbance:.4f}
"""

    result_text.set(result)


# GUI
window = tk.Tk()
window.title("UV Absorbance Meter (254 nm)")

result_text = tk.StringVar()

button = tk.Button(window, text="Select images and calculate", command=run)
button.pack(pady=20)

label = tk.Label(window, textvariable=result_text, justify="left")
label.pack(pady=20)

window.mainloop()
