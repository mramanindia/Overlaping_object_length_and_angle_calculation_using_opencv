import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

#median blur to cover salt paper issues
def noise_removal(img, unit=3):
    clear_image = cv2.medianBlur(img, 3)
    return clear_image

#Gray scale and canny edge detection 
def img_preprocessing(img, unit=100):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    edges = cv2.Canny(gray_image, 50, 150)
    return edges

# Using HoughLinesP for line over the edges

##PPI = Pixel per inch
def length_angle(img, clear_img, PPI=72):
    clean_img = clear_img.copy()
    length_of_pencil = []
    lines = cv2.HoughLinesP(img, rho=1, theta=np.pi/180, threshold=20, minLineLength=200, maxLineGap=100)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        cv2.line(clean_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        length_cm = length / PPI * 2.54
        length_of_pencil.append(length_cm)
        
    if len(lines) > 2:
        x3, y3, x4, y4 = lines[1][0]
        angle = math.atan2((y4 - y3), (x4 - x3)) - math.atan2((y2 - y1), (x2 - x1))
    else:
        angle = 0

    return clean_img, length_of_pencil, math.degrees(angle)

#UI
def upload_image():
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path)
    clear_img = noise_removal(img)
    edges = img_preprocessing(clear_img)
    output_img, length, angle = length_angle(edges, clear_img, 65)

    # Convert input_img, clear_img, and output_img to RGB format
    input_img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    clear_img_rgb = cv2.cvtColor(clear_img, cv2.COLOR_BGR2RGB)
    output_img_rgb = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

    # Resize images
    input_img_rgb = cv2.resize(input_img_rgb, (300, 200))
    clear_img_rgb = cv2.resize(clear_img_rgb, (300, 200))
    output_img_rgb = cv2.resize(output_img_rgb, (300, 200))

    # Convert images to PIL format
    input_img_pil = Image.fromarray(input_img_rgb)
    clear_img_pil = Image.fromarray(clear_img_rgb)
    output_img_pil = Image.fromarray(output_img_rgb)

    # Convert PIL images to Tkinter format
    input_img_tk = ImageTk.PhotoImage(input_img_pil)
    clear_img_tk = ImageTk.PhotoImage(clear_img_pil)
    output_img_tk = ImageTk.PhotoImage(output_img_pil)

    # Update image labels
    input_img_label.config(image=input_img_tk)
    input_img_label.image = input_img_tk
    clear_img_label.config(image=clear_img_tk)
    clear_img_label.image = clear_img_tk
    output_img_label.config(image=output_img_tk)
    output_img_label.image = output_img_tk

    length_label.config(text=f"Length of pencil B: {length[2]:.2f} cm", font=("Arial", 14, "bold"))
    angle_label.config(text=f"Angle: {angle:.2f} degrees", font=("Arial", 14, "bold"))

    # # Update image name labels
    # input_name_label.config(text="Input Image", font=("Arial", 12, "bold"))
    # filtered_name_label.config(text="Filtered Image", font=("Arial", 12, "bold"))
    # output_name_label.config(text="Output Image", font=("Arial", 12, "bold"))

# Create Tkinter window
window = tk.Tk()
window.title("Pencil Analysis")
window.configure(bg="#f0f0f0")  # Set background color

# Set window size
window.geometry("1200x700")

# Create upload button
upload_button = tk.Button(window, text="Upload Image", command=upload_image, bg="#4CAF50", fg="white")  # Set button colors
upload_button.pack(pady=10)

# Create labels for length and angle
length_label = tk.Label(window, text="Length of pencil B: ", bg="#f0f0f0")
length_label.pack()
angle_label = tk.Label(window, text="Angle: ", bg="#f0f0f0")
angle_label.pack()

# Create label for input image name
input_name_label = tk.Label(window, bg="#f0f0f0")
input_name_label.pack()
# Create label to display input_img
input_img_label = tk.Label(window, bg="#ffffff")
input_img_label.pack(side="left", padx=20)

# Create label for filtered image name
filtered_name_label = tk.Label(window, bg="#f0f0f0")
filtered_name_label.pack()
# Create label to display clear_img
clear_img_label = tk.Label(window, bg="#ffffff")
clear_img_label.pack(side="left", padx=20)

# Create label for output image name
output_name_label = tk.Label(window, bg="#f0f0f0")
output_name_label.pack()
# Create label to display output_img
output_img_label = tk.Label(window, bg="#ffffff")
output_img_label.pack(side="left", padx=20)

window.mainloop()
