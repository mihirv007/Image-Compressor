import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def compress_image(input_path, output_path, quality):
    try:
        image = Image.open(input_path)
        ext = os.path.splitext(output_path)[1].lower()

        if ext in [".jpg", ".jpeg"]:
            image = image.convert("RGB")  # Required for JPEG
            image.save(
                output_path,
                quality=quality,
                optimize=True
            )

        elif ext == ".png":
            # Map quality (1–100) → PNG compress_level (0–9)
            compress_level = int((100 - quality) / 11)
            image.save(
                output_path,
                optimize=True,
                compress_level=compress_level
            )

        else:
            messagebox.showerror("Error", "Unsupported file format")
            return

        messagebox.showinfo("Success", "Image compressed successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Compression failed:\n{e}")

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if file_path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save Image As",
        defaultextension=".jpg",
        filetypes=[
            ("JPEG Image", "*.jpg"),
            ("PNG Image", "*.png")
        ]
    )
    if file_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, file_path)

def compress():
    if not entry_input.get() or not entry_output.get():
        messagebox.showwarning("Missing Info", "Please select input and output files.")
        return

    quality = scale_quality.get()
    compress_image(entry_input.get(), entry_output.get(), quality)

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Image Compressor (JPG + PNG)")
root.resizable(False, False)

tk.Label(root, text="Select Image:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_input = tk.Entry(root, width=45)
entry_input.grid(row=0, column=1, padx=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10)

tk.Label(root, text="Compression Level:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
scale_quality = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL)
scale_quality.set(75)
scale_quality.grid(row=1, column=1, padx=10)

tk.Label(root, text="Save As:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_output = tk.Entry(root, width=45)
entry_output.grid(row=2, column=1, padx=10)
tk.Button(root, text="Browse", command=save_file).grid(row=2, column=2, padx=10)

tk.Button(root, text="Compress", width=20, command=compress)\
    .grid(row=3, column=1, pady=20)

root.mainloop()
