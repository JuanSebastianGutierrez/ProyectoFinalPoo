# -- coding: utf-8 --
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
import calendar

class Participantes:
    path = r'C:\Users\junas\Documents\Ingenieria_Electrica\2024-2\Programacion Orientada a Objetos\Proyecto final\venv'
    db_name = path + r'/Participantes.db'
    actualiza = None
    
    def _init_(self, master=None):
        self.win = tk.Tk() if master is None else tk.Toplevel()
        self.win.configure(background="#d9f0f9")
        self.win.geometry("800x500")
        self.win.iconbitmap(self.path + r'/Logo_guardianpass.ico')
        self.win.resizable(False, False)
        self.win.title("Conferencia MACSS - Inscripción")

        # Marco de datos
        self.lblfrm_Datos = tk.LabelFrame(self.win, text=" Inscripción ", font=("Helvetica", 13, "bold"))
        self.lblfrm_Datos.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        labels = ["Identificación", "Nombre", "Dirección", "Celular", "Entidad", "Fecha", "Ciudad"]
        self.entries = {}
        
        for i, text in enumerate(labels):
            ttk.Label(self.lblfrm_Datos, text=text, width=12).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if text == "Ciudad":
                self.entries[text] = ttk.Combobox(self.lblfrm_Datos, state="readonly", width=27)
                self.entries[text].grid(row=i, column=1, padx=5, pady=5)
                self.cargar_ciudades()
            else:
                self.entries[text] = tk.Entry(self.lblfrm_Datos, width=30)
                self.entries[text].grid(row=i, column=1, padx=5, pady=5)
        
        # Botones
        botones = [("Grabar", self.adiciona_Registro), ("Editar", self.edita_tablaTreeView),
                   ("Eliminar", self.elimina_Registro), ("Cancelar", self.limpia_Campos)]
        
        for i, (text, cmd) in enumerate(botones):
            btn = ttk.Button(self.win, text=text, width=10, command=cmd)
            btn.grid(row=1, column=i, padx=5, pady=10, sticky="w")

        # Tabla TreeView
        self.treeDatos = ttk.Treeview(self.win, columns=("Nombre", "Dirección", "Celular", "Entidad", "Fecha", "Ciudad"),
                                      height=10, show="headings")
        for col in self.treeDatos["columns"]:
            self.treeDatos.heading(col, text=col)
            self.treeDatos.column(col, width=100)

        self.treeDatos.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self.win, orient="vertical", command=self.treeDatos.yview)
        self.treeDatos.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, sticky="ns")

        self.lee_tablaTreeView()

    def run(self):
        self.win.mainloop()

    def run_Query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result

    def cargar_ciudades(self):
        """Carga las ciudades desde la base de datos en el Combobox."""
        query = "SELECT nombre FROM ciudades"
        db_rows = self.run_Query(query)
        ciudades = [row[0] for row in db_rows]
        self.entries["Ciudad"]["values"] = ciudades

    def lee_tablaTreeView(self):
        """Carga los datos de la BD en el TreeView."""
        for item in self.treeDatos.get_children():
            self.treeDatos.delete(item)

        query = "SELECT * FROM t_participantes ORDER BY Id DESC"
        db_rows = self.run_Query(query)
        for row in db_rows:
            self.treeDatos.insert("", 0, values=row)

    def valida(self):
        """Valida que el campo Identificación no esté vacío."""
        return bool(self.entries["Identificación"].get())

    def limpia_Campos(self):
        """Limpia los campos de entrada."""
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, "end")

    def adiciona_Registro(self):
        """Añade o actualiza un registro en la base de datos."""
        if self.actualiza:
            query = """UPDATE t_participantes SET Nombre=?, Dirección=?, Celular=?, 
                       Entidad=?, Fecha=?, Ciudad=? WHERE Id=?"""
            parametros = tuple(self.entries[key].get() for key in self.entries) + (self.entries["Identificación"].get(),)
            self.run_Query(query, parametros)
            mssg.showinfo("Éxito", "Registro actualizado correctamente")
            self.actualiza = None
        else:
            if self.valida():
                query = "INSERT INTO t_participantes VALUES (?, ?, ?, ?, ?, ?, ?)"
                parametros = tuple(self.entries[key].get() for key in self.entries)
                self.run_Query(query, parametros)
                mssg.showinfo("Éxito", f"Registro {self.entries['Identificación'].get()} agregado")
            else:
                mssg.showerror("Error", "El campo Identificación no puede estar vacío")
        
        self.limpia_Campos()
        self.lee_tablaTreeView()

    def edita_tablaTreeView(self):
        """Carga los datos del TreeView en los campos de entrada para editar."""
        try:
            seleccionado = self.treeDatos.selection()[0]
            valores = self.treeDatos.item(seleccionado)["values"]
            for i, key in enumerate(self.entries):
                self.entries[key].delete(0, "end")
                self.entries[key].insert(0, valores[i])
            self.actualiza = True
        except IndexError:
            mssg.showerror("Error", "Seleccione un registro para editar")

    def elimina_Registro(self):
        """Elimina un registro seleccionado."""
        seleccionado = self.treeDatos.selection()
        if not seleccionado:
            mssg.showerror("Error", "Seleccione un registro para eliminar")
            return

        respuesta = mssg.askyesno("Confirmar", "¿Seguro que quiere eliminar este registro?")
        if respuesta:
            id_seleccionado = self.treeDatos.item(seleccionado[0])["values"][0]
            query = "DELETE FROM t_participantes WHERE Id = ?"
            self.run_Query(query, (id_seleccionado,))
            self.lee_tablaTreeView()
            mssg.showinfo("Éxito", "Registro eliminado correctamente")

if _name_ == "_main_":
    app = Participantes()
    app.run()