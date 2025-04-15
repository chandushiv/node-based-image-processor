import cv2
import numpy as np
from tkinter import Tk, filedialog, simpledialog, messagebox

# --- Core Functions (Nodes) ---
def load_image():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
    return cv2.imread(file_path) if file_path else None

def save_image(image):
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        cv2.imwrite(file_path, image)
        messagebox.showinfo("Success", f"Image saved to {file_path}")

def grayscale_node(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blur_node(image):
    kernel_size = simpledialog.askinteger("Blur", "Enter kernel size (odd number, e.g., 5):", minvalue=3, maxvalue=25)
    if kernel_size:
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return image

def edge_detection_node(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

def brightness_node(image):
    brightness = simpledialog.askinteger("Brightness", "Enter brightness (-100 to 100):", minvalue=-100, maxvalue=100)
    if brightness:
        return cv2.convertScaleAbs(image, alpha=1, beta=brightness)
    return image

# --- Main Program ---
def main():
    image = load_image()
    if image is None:
        print("No image selected. Exiting.")
        return

    while True:
        choice = simpledialog.askstring(
            "Node Selection",
            "Choose a node:\n1. Grayscale\n2. Blur\n3. Edge Detection\n4. Brightness\n5. Save & Exit",
        )
        if choice == "1":
            image = grayscale_node(image)
        elif choice == "2":
            image = blur_node(image)
        elif choice == "3":
            image = edge_detection_node(image)
        elif choice == "4":
            image = brightness_node(image)
        elif choice == "5":
            save_image(image)
            break
        else:
            messagebox.showerror("Error", "Invalid choice!")
        
        cv2.imshow("Processed Image", image)
        cv2.waitKey(1000)  # Refresh display

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()