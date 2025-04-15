import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class NodeProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Node-Based Image Processor")
        self.image = None
        
        # GUI Elements
        self.load_btn = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_btn.pack()
        
        self.gray_btn = tk.Button(root, text="Grayscale", command=self.apply_grayscale, state=tk.DISABLED)
        self.gray_btn.pack()
        
        self.blur_btn = tk.Button(root, text="Blur", command=self.apply_blur, state=tk.DISABLED)
        self.blur_btn.pack()
        
        self.edge_btn = tk.Button(root, text="Edge Detect", command=self.apply_edge, state=tk.DISABLED)
        self.edge_btn.pack()
        
        # self.save_btn = tk.Button(root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        # self.save_btn.pack()
        self.save_btn = tk.Button(
            root, 
            text="Save Image", 
            command=self.save_image,
            bg="#ffcccc",  # Light red color
            state=tk.DISABLED  # Disabled until image is loaded
    )
        self.save_btn.pack(pady=5)  # pady adds spacing
        
        self.preview_label = tk.Label(root)
        self.preview_label.pack()

        # Add to the GUI class
        self.brightness_scale = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL, label="Brightness")
        self.brightness_scale.pack()
        self.brightness_btn = tk.Button(root, text="Apply Brightness", command=self.adjust_brightness)
        self.brightness_btn.pack()

        # Add to the GUI class # upd 2
        self.blend_btn = tk.Button(root, text="Blend Images", command=self.blend_images)
        self.blend_btn.pack()

        self.blend_ratio = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Blend Ratio (%)")
        self.blend_ratio.set(50)  # Default 50-50 blend
        self.blend_ratio.pack()

    #up 2 fn
    def blend_images(self):
    # First check if we have a base image loaded
        if self.image is None:
            messagebox.showerror("Error", "Please load a base image first!")
            return
    
        # Open the second image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if not file_path:
            return
        
        # Read and resize the second image to match the first
        img2 = cv2.imread(file_path)
        if img2 is None:
            messagebox.showerror("Error", "Failed to load the second image!")
            return
        
        # Resize the second image to match the first
        if img2.shape != self.image.shape:
            img2 = cv2.resize(img2, (self.image.shape[1], self.image.shape[0]))
            messagebox.showinfo("Notice", "The second image was resized to match the first")
        
        # Convert both images to same color space if needed
        if len(self.image.shape) == 2:  # If base is grayscale
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        elif len(img2.shape) == 2:  # If blend image is grayscale but base is color
            img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        
        # Blend the images
        self.image = cv2.addWeighted(self.image, 0.5, img2, 0.5, 0)
        self.update_preview()

        alpha = self.blend_ratio.get() / 100.0  # Convert to 0.0-1.0
        beta = 1.0 - alpha
        self.image = cv2.addWeighted(self.image, alpha, img2, beta, 0)

    # def blend_images(self):
    #     file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
    #     if file_path:
    #         img2 = cv2.imread(file_path)
    #         if img2.shape == self.image.shape:
    #             self.image = cv2.addWeighted(self.image, 0.5, img2, 0.5, 0)
    #             self.update_preview()
    
    #up 1 fn
    def adjust_brightness(self):
        brightness = self.brightness_scale.get()
        self.image = cv2.convertScaleAbs(self.image, alpha=1, beta=brightness)
        self.update_preview()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.update_preview()
            self.enable_buttons()

    def apply_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.update_preview()

    def apply_blur(self):
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)
        self.update_preview()

    def apply_edge(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(self.image.shape) == 3 else self.image
        self.image = cv2.Canny(gray, 100, 200)
        self.update_preview()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            cv2.imwrite(file_path, self.image)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    
    def update_preview(self):
        img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB) if len(self.image.shape) == 3 else cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil.resize((300, 300)))
        self.preview_label.config(image=img_tk)
        self.preview_label.image = img_tk

    # def enable_buttons(self):
    #     for btn in [self.gray_btn, self.blur_btn, self.edge_btn, self.save_btn]:
    #         btn.config(state=tk.NORMAL)

    # """Activate buttons when an image is loaded"""
    def enable_buttons(self):
        for btn in [self.gray_btn, self.blur_btn, self.edge_btn, self.save_btn, self.blend_btn]:
            btn.config(state=tk.NORMAL)

root = tk.Tk()
app = NodeProcessor(root)
root.mainloop() 
