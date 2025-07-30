import tkinter as tk 
from tkinter import filedialog,messagebox,simpledialog
from tkinter import ttk
from PyPDF2 import PdfMerger,PdfReader,PdfWriter
import os


class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini IlovePDF")
        self.root.geometry("500x400")
        self.pdf_files = []

        self.listbox = tk.Listbox(root, height=8)
        self.listbox.pack(fill="both", padx=10, pady=(10, 0))
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        # ttk.Button(btn_frame, text="Mover arriba", command=self.mover_arriba).pack(side="left", padx=5)
        # ttk.Button(btn_frame, text="Mover abajo", command=self.mover_abajo).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar lista", command=self.limpiar_lista).pack(side="left", padx=5)
        
        ttk.Button(root, text="Agregar PDF", command=self.select_pdf).pack(pady=10)
        ttk.Button(root, text="Unir PDFs", command=self.merge_pdfs).pack(pady=10)
        ttk.Button(root, text="Dividir por rango", command=self.split_pdf).pack(pady=10)
        ttk.Button(root, text="Dividir por página", command=self.split_bypages).pack(pady=10)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for f in self.pdf_files:
            self.listbox.insert(tk.END, os.path.basename(f))
        
    def select_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files","*.pdf")])
        self.pdf_files=list(files)
        self.update_listbox()
        messagebox.showinfo("Seleccionados",f"{len(files)} archivos selecionados")
        
    def merge_pdfs(self):
        if len(self.pdf_files)< 2:
            messagebox.showwarning("Advertencia","Para esta funcion se necesitan minimo 2 archivos")
            return
        merger=PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)
        
        output_path=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")])
        if output_path:
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Exito",f"PDFs_unidos en {output_path}")
    
    def split_pdf(self):
        if not self.pdf_files:
            messagebox.showwarning("Advertencia", "Tienes que seleccionar un PDF")
            return

        pdf_path = self.pdf_files[0]
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        rang = simpledialog.askstring("Dividir", f"Total de páginas: {total_pages}\nIngresa rango, ejemplo: 1-3")
        if not rang or "-" not in rang:
            messagebox.showerror("Error", "Debes ingresar un rango válido como 1-3")
            return

        try:
            inicio, fin = map(int, rang.split("-"))
        except ValueError:
            messagebox.showerror("Error", "El rango debe ser numérico, ejemplo: 1-3")
            return

        if inicio < 1 or fin > total_pages or inicio > fin:
            messagebox.showerror("Error", "Rango fuera de los límites del PDF")
            return

        writer = PdfWriter()
        for i in range(inicio - 1, fin):
            writer.add_page(reader.pages[i])

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Éxito", "Archivo dividido y guardado.")
            
    def split_bypages(self):
        if not self.pdf_files:
            messagebox.showwarning("Advertencia","Tienes que seleccionar un pdf")
            return
        pdf_path= self.pdf_files[0]
        reader = PdfReader(pdf_path)
        output_folder= filedialog.askdirectory(title="Selecciona una carpeta para guardar las paginas")
        if not output_folder:
            return
        for i, page in enumerate(reader.pages):
            write = PdfWriter()
            write.add_page(page)
            output_path = os.path.join(output_folder,f"paginas_{i+1}.pdf")
            with open(output_path,"wb")as f:
                write.write(f)
                
        messagebox.showinfo("Éxito", f"PDF dividido en {len(reader.pages)} páginas")


    def limpiar_lista(self):
        self.pdf_files.clear()
        self.update_listbox()
        
        






if __name__=="__main__":
    root=tk.Tk()
    app= PDFApp(root)
    root.mainloop()