import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import base64
import os
import google.generativeai as genai  # Corrected import

# Replace with your actual Gemini API key
GEMINI_API_KEY = "YOUR_API_KEY"

# Initialize the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def call_gemini_api(prompt, image_path=None, temperature=0.8):
    """
    Calls the Gemini 2.0 Flash model with a text prompt and optional image.
    """
    try:
        # Prepare request content
        model = genai.GenerativeModel("gemini-2.0-flash")

        contents = [prompt]

        if image_path:
            try:
                with open(image_path, "rb") as img_file:
                    image_data = img_file.read()
                contents.append({"mime_type": "image/jpeg", "data": image_data})
            except Exception as e:
                return {"response": f"Error: Could not process the image. {e}"}

        response = model.generate_content(contents)
        return {"response": response.text if response else "No response from API."}
    except Exception as e:
        return {"response": f"Error calling API: {e}"}

def browse_image():
    """Opens a file dialog for the user to select an image file."""
    filename = filedialog.askopenfilename(
        title="Select City Map Image",
        filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp"), ("All Files", ".*")]
    )
    if filename:
        image_path_var.set(filename)

def generate_design():
    """
    Calls the AI model with user input and displays the generated response.
    """
    prompt = prompt_text.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showwarning("Input Error", "Please enter a design prompt.")
        return

    image_path = image_path_var.get()
    if image_path and not os.path.exists(image_path):
        messagebox.showwarning("Input Error", "Selected image file does not exist.")
        return

    # Call API
    result = call_gemini_api(prompt, image_path=image_path, temperature=0.8)

    # Display response
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result["response"])

# -----------------------------
# Tkinter GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Urban Green Space Architect Model")
root.geometry("600x500")

# Frame for design prompt entry
prompt_frame = tk.Frame(root)
prompt_frame.pack(pady=10, padx=10, fill=tk.X)
prompt_label = tk.Label(prompt_frame, text="Enter Design Prompt:")
prompt_label.pack(anchor="w")
prompt_text = tk.Text(prompt_frame, height=6, width=70)
prompt_text.pack()

# Frame for image selection
image_frame = tk.Frame(root)
image_frame.pack(pady=10, padx=10, fill=tk.X)
image_path_var = tk.StringVar()
image_label = tk.Label(image_frame, text="City Map Image:")
image_label.pack(side=tk.LEFT, padx=5)
image_entry = tk.Entry(image_frame, textvariable=image_path_var, width=40)
image_entry.pack(side=tk.LEFT, padx=5)
browse_button = tk.Button(image_frame, text="Browse", command=browse_image)
browse_button.pack(side=tk.LEFT, padx=5)

# Button to generate design suggestion
generate_button = tk.Button(root, text="Generate Green Space Design",
                            command=generate_design, bg="green", fg="white",
                            font=("Helvetica", 12, "bold"))
generate_button.pack(pady=10)

# Frame for displaying output
output_frame = tk.Frame(root)
output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
output_label = tk.Label(output_frame, text="Generated Design Suggestion:")
output_label.pack(anchor="w")
output_text = scrolledtext.ScrolledText(output_frame, height=10, width=70)
output_text.pack(fill=tk.BOTH, expand=True)

# Run the Tkinter event loop
root.mainloop()
