import pandas as pd
import tkinter as tk
import logging
from tkinter import filedialog
import os

class MainWindow(tk.Frame):
    
    log_folder_location = 'C:\\Users\\C2204001\\Documents\\Logy'
    log_base_name = "CSV_analysis TEST"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title('CSV_analysis')

        # Move the log-related code inside the __init__ method
        self.i = 1
        self.existing_logs = [f for f in os.listdir(self.log_folder_location) if f.startswith("CSV_analysis TEST")]
        if self.existing_logs:
            existing_numbers = [self.extract_numeric_part(log) for log in self.existing_logs]
            self.i = max(existing_numbers) + 1
        else:
            self.i = 1

        self.log_name = f"{self.log_base_name}{self.i}.log"
        self.log_location = os.path.join(self.log_folder_location, self.log_name)

        logging.basicConfig(filename=self.log_location, level=logging.DEBUG)

        self.create_widgets()

    def extract_numeric_part(self, filename):
        try:
            return int(filename.split('.')[1])
        except (IndexError, ValueError):
            return 0

    def create_widgets(self):
        self.label = tk.Label(self, text='CSV Analýza')
        self.label.pack()

        self.output_text = tk.Text(self, wrap=tk.WORD, height=10, width=40)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        button_go = tk.Button(self, text='Go', width=25, command=self.load_csv)
        button_go.pack()
        
        button_clear = tk.Button(self, text='Clear',width=25,command=self.output_text.delete)
        button_clear.pack()

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
                        output_str = str(analysis.head(n=3))
                        self.output_text.delete(1.0, tk.END)
                        self.output_text.insert(tk.END, output_str)
                except FileNotFoundError:
                    logging.CRITICAL(f'File {file_path} not found')
            except (SyntaxError, UnicodeError) as err:
                logging.CRITICAL('Syntax or Unicode error recorded')
                logging.ERROR(f'{err} recorded')
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f'Error: {err}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
