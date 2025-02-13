import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading
import time

# Load the saved YOLOv8 model
model = YOLO('final_model.pt')

# Function to open file dialog and select an image
def select_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    
    if file_path:
        # Start processing the image in a new thread to avoid blocking the GUI
        status_var.set("Processing image... Please wait.")
        show_loading_animation(True)
        threading.Thread(target=process_image, args=(file_path,)).start()

# Function to process the image
def process_image(file_path):
    try:
        # Run inference on the selected image
        results = model(file_path)
        
        # If results are a list, access the first element
        if isinstance(results, list):
            result_image = results[0].plot()  # Plot the results
        else:
            result_image = results.plot()  # Plot the results for single output

        # Convert the result image to a format suitable for Tkinter (PIL Image)
        result_image_pil = Image.fromarray(result_image)

        # Update the Tkinter window with the result image
        display_image(result_image_pil)

        # Update the status label
        status_var.set("Image Processed Successfully!")
        show_loading_animation(False)

    except Exception as e:
        show_loading_animation(False)
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to display the image in the Tkinter window
def display_image(image):
    image = image.resize((640, 640))  # Resize to fit the window
    img_tk = ImageTk.PhotoImage(image)

    # If there's an existing image in the window, remove it
    if hasattr(display_image, "current_image_label"):
        display_image.current_image_label.destroy()

    # Create a new label with the image
    display_image.current_image_label = tk.Label(frame, image=img_tk, bd=5, relief="solid", padx=10, pady=10, bg="#f0f0f0")
    display_image.current_image_label.image = img_tk  # Keep a reference to avoid garbage collection
    display_image.current_image_label.pack(padx=10, pady=10)

# Function to show or hide loading animation
def show_loading_animation(show):
    if show:
        loading_label.pack()
    else:
        loading_label.pack_forget()

# Create the main Tkinter window
window = tk.Tk()
window.title("Solar Panel Detection (A Project by Rochan Awasthi)")
window.geometry("700x700")  # Set window size

# Center the window on the screen
window_width = 700
window_height = 700
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Set background color of the entire window
window.configure(bg="#f0f0f0")

# Add a title label with background color and custom font
title_label = tk.Label(window, text="Solar Panel Detection", font=("Arial", 24, "bold"), fg="#4CAF50", bg="#f0f0f0")
title_label.pack(pady=20)

# Instructions label with a custom color
instructions_label = tk.Label(window, text="Click the button below to select an image for detection.", font=("Arial", 12), bg="#f0f0f0", fg="#555")
instructions_label.pack(pady=10)

# Create a frame to hold the image and buttons (background color added here)
frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(pady=20)

# Create a button to select an image with hover effect
def on_enter(e):
    button['background'] = "#45a049"  # Darken the button on hover

def on_leave(e):
    button['background'] = "#4CAF50"  # Return to original color when mouse leaves

button = tk.Button(window, text="Select Image", command=select_image, font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", padx=20, pady=10)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)
button.pack()

# Status label (to show information like 'Image loaded' or 'Processing...')
status_var = tk.StringVar()
status_var.set("Waiting for user input...")
status_label = tk.Label(window, textvariable=status_var, font=("Arial", 12), fg="blue", bg="#f0f0f0")
status_label.pack(pady=10)

# Loading animation (a spinning wheel)
loading_label = tk.Label(window, text="Processing... Please wait.", font=("Arial", 14), fg="blue", bg="#f0f0f0")

# Start the Tkinter event loop
# Add the "Created by Rochan Awasthi" label at the bottom
footer_label = tk.Label(window, text="Created by Rochan Awasthi", font=("Arial", 10), fg="gray", bg="#f0f0f0")
footer_label.pack(side="bottom", pady=10)

window.mainloop()
