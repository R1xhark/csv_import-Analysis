import pandas as pd
import tkinter as tk
import logging
from tkinter import filedialog
import os

class MainWindow(tk.Frame):
    
    log_folder_location = 'C:\\Users\\C2204001\\Documents\\Logy/'
    log_base_name = "CSV_analysis TEST"
    i = 1
    existing_logs = [f for f in os.listdir(log_folder_location) if f.startswith("CSV_analysis TEST")]
    if existing_logs:
        existing_numbers = [int(log.split('.')[1]) for log in existing_logs]
        i = max(existing_numbers) + 1
    else:
        i = 1

    log_name = f"{log_base_name}{i}.log"

    log_location = os.path.join(log_folder_location,log_name)

    logging.basicConfig(filename=log_location,level=logging.DEBUG)
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title('CSV_analysis')
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text='CSV Analýza')
        self.label.pack()

        self.output_text = tk.Text(self, height=10, width=40)
        self.output_text.pack()

        button_go = tk.Button(self, text='Go', width=25, command=self.load_csv)
        button_go.pack()

        button_exit = tk.Button(self, text='Exit', width=25, command=self.parent.destroy)
        button_exit.pack()

    def load_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                logging.info('Feeding CSV file_path')
                try:
                    if os.path.exists(file_path):
                        analysis = pd.read_csv(file_path)
                        output_str = str(analysis.head())
                        self.output_text.delete(1.0, tk.END)  # Clear previous content
                        self.output_text.insert(tk.END, output_str)
                except (FileNotFoundError) as err:
                    logging.CRITICAL(f'File {file_path} ')
            except (SyntaxError, UnicodeError) as err:
                logging.CRITICAL('Syntax or Unicode error recorded')
                logging.ERROR(f'{err} recorded')
                self.output_text.delete(1.0, tk.END)  # Clear previous content
                self.output_text.insert(tk.END, f'Error: {err}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.mainloop()
