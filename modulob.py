import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd

def exibir_tabela(dados, tree, status_label):
    for i in tree.get_children():
        tree.delete(i)
    
    total_pecas = len(dados)
    aprovadas = 0
    rejeitadas = 0
    
    for index, row in dados.iterrows():
        if (50 <= row['Peso (g)'] <= 100) and (10 <= row['Tamanho (cm)'] <= 20) and (row['Acabamento'] > 7):
            status = "Aprovada"
            motivo_rejeicao = ""
            aprovadas += 1
        else:
            status = "Rejeitada"
            if not (50 <= row['Peso (g)'] <= 100):
                motivo_rejeicao = "Peso fora do intervalo (50-100g)"
            elif not (10 <= row['Tamanho (cm)'] <= 20):
                motivo_rejeicao = "Tamanho fora do intervalo (10-20cm)"
            elif row['Acabamento'] <= 7:
                motivo_rejeicao = "Acabamento abaixo de 7"
            rejeitadas += 1
        
        tree.insert("", "end", values=(row['ID'], row['Peso (g)'], row['Tamanho (cm)'], row['Acabamento'], status, motivo_rejeicao))
    
    status_label.config(text=f"Total de peças: {total_pecas} | Aprovadas: {aprovadas} | Rejeitadas: {rejeitadas}")
    
    if total_pecas > 0 and (rejeitadas / total_pecas) * 100 > 20:
        messagebox.showwarning("Alerta de Revisão", f"Mais de 20% das peças foram rejeitadas. Reveja o processo de produção!")

def executar_analise(tree, status_label):
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if caminho_arquivo:
        dados = pd.read_csv(caminho_arquivo)
        exibir_tabela(dados, tree, status_label)

root = tk.Tk()
root.title("Análise de Peças - QualityAI Solutions")
root.geometry("1000x800")
root.configure(bg="#1A1A2E")

estilo = ttk.Style()
estilo.configure("Treeview", background="#1A1A2E", foreground="white", fieldbackground="#1A1A2E", font=("Arial", 14))
estilo.configure("Treeview.Heading", font=("Arial", 16, "bold"), background="#16213E", foreground="black")

titulo_label = tk.Label(root, text="Guiyan Solutions - Análise de peças", font=("Arial", 20, "bold"), fg="white", bg="#1A1A2E")
titulo_label.pack(pady=10)

tree_frame = tk.Frame(root, bg="#1A1A2E")
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("ID", "Peso (g)", "Tamanho (cm)", "Acabamento", "Status", "Motivo"), show="headings", height=20)
for col in ("ID", "Peso (g)", "Tamanho (cm)", "Acabamento", "Status", "Motivo"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=300)
tree.pack()

status_label = tk.Label(root, text="Total de peças: 0 | Aprovadas: 0 | Rejeitadas: 0", font=("Arial", 18), fg="white", bg="#1A1A2E")
status_label.pack(pady=10)

botao_analise = tk.Button(root, text="Selecionar Arquivo CSV", font=("Arial", 18, "bold"), fg="white", bg="#0F3460", padx=10, pady=5, command=lambda: executar_analise(tree, status_label))
botao_analise.pack(pady=20)

root.mainloop()
