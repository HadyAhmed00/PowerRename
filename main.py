import tkinter as tk
from tkinter import filedialog
import os
import re
import glob
import datetime
import img2pdf
mainDir = "TestImage"


def merge_images_to_pdf(image_list, output_pdf, output_dir, dpi=200, compress_level=1, verbose=True):
    output_path = os.path.join(os.path.join(output_dir, "PDF"), output_pdf)
    pdf_file = img2pdf.convert(image_list, dpi=dpi, compress_level=compress_level,rotation=img2pdf.Rotation.ifvalid)
    with open(output_path, 'wb') as f:
        f.write(pdf_file)
    if verbose:
        print(f"PDF created successfully: {output_path}")

def formulate_name(work_images, start_image_idx, arc_number, dom_number, number_of_pages, output_dir):
    count = 1
    curr_work_image = start_image_idx
    renamed_images = []
    for i in range(number_of_pages):
        name = ""
        if i == 0:
            name = f'{arc_number}.jpeg'
        elif i == 1:
            name = f'{arc_number}_{dom_number}_{datetime.datetime.now().year}.jpeg'
        else:
            name = f'{arc_number}_{dom_number}_{datetime.datetime.now().year}00{count}.jpeg'
            count += 1
        new_name = os.path.join(
            os.path.dirname(work_images[curr_work_image]),
            name
        )
        os.rename(work_images[curr_work_image], new_name)
        renamed_images.append(new_name)
        curr_work_image += 1
    pdf_filename = f"{arc_number}_{dom_number}_{datetime.datetime.now().year}.pdf"
    merge_images_to_pdf(renamed_images, pdf_filename, output_dir)
    return curr_work_image - start_image_idx


def get_images(user_input, directory, prefix):
    working_images = glob.glob(os.path.join(directory, f"{prefix}*"))
    start_imge = 0
    total_renamed = 0

    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0

    working_images.sort(key=extract_number)
    input_list = user_input.strip().splitlines()
    for data in input_list:
        arc_number, dom_number, number_of_pages = data.split(".")
        number_of_pages = int(number_of_pages.strip())
        renamed_count = formulate_name(working_images, start_imge, arc_number.strip(), dom_number.strip(),
                                       number_of_pages,directory)
        total_renamed += renamed_count
        start_imge += number_of_pages
    return total_renamed


class ImageRenamerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Renamer")
        self.geometry("500x500")

        # Input area
        self.input_label = tk.Label(self, text="Enter data (one per line):")
        self.input_label.pack(pady=10)
        self.input_text = tk.Text(self, width=50, height=10)
        self.input_text.pack()

        # Prefix input area
        self.prefix_label = tk.Label(self, text="Enter prefix:")
        self.prefix_label.pack(pady=5)
        self.prefix_entry = tk.Entry(self, width=20)
        self.prefix_entry.pack()

        # Folder selection area
        self.folder_label = tk.Label(self, text="Select image folder:")
        self.folder_label.pack(pady=10)
        self.folder_path = tk.StringVar()
        self.folder_button = tk.Button(self, text="Browse", command=self.browse_folder)
        self.folder_button.pack()
        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, state="disabled")
        self.folder_entry.pack()

        # Rename button
        self.rename_button = tk.Button(self, text="Rename Images", command=self.rename_images)
        self.rename_button.pack(pady=15)

        # Made with heart by Trasol Team label
        self.made_by_label = tk.Label(self, text="Made with ❤️ by Trasol Team \n V 1.0.2 (PDF)")
        self.made_by_label.pack(side=tk.BOTTOM)

    def browse_folder(self):
        self.folder_path.set(filedialog.askdirectory())

    def rename_images(self):
        user_input = self.input_text.get("1.0", tk.END)
        folder_path = self.folder_path.get()
        output_folder = os.path.join(folder_path, "PDF")
        os.makedirs(output_folder, exist_ok=True)
        prefix = self.prefix_entry.get()
        if not user_input or not folder_path:
            tk.messagebox.showerror("Error", "Please enter data and select a folder.")
            return
        total_renamed = get_images(user_input, folder_path, prefix)
        tk.messagebox.showinfo("Success", f"{total_renamed} images renamed successfully!")


if __name__ == '__main__':
    app = ImageRenamerGUI()
    app.mainloop()
