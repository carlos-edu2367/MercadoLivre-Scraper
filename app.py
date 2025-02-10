import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser
import menorValorML

def buscar_produto():
    nome = entrada_produto.get()
    if not nome:
        messagebox.showwarning("Aviso", "Digite um nome de produto!")
        return
    
    resultado_label.config(text="Buscando...", fg="blue")
    botao_buscar.config(state=tk.DISABLED)
    
    def executar_busca():
        resultado = menorValorML.valorML(nome)
        if resultado:
            titulo, link, preco = resultado
            resultado_label.config(text=f"{titulo} - R$ {preco:.2f}", fg="green")
            link_label.config(text="Clique aqui para ver o produto", fg="blue", cursor="hand2")
            link_label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
        else:
            resultado_label.config(text="Nenhum produto encontrado.", fg="red")
            link_label.config(text="")
        botao_buscar.config(state=tk.NORMAL)
    
    threading.Thread(target=executar_busca, daemon=True).start()

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Busca Mercado Livre")
janela.geometry("400x200")

# Widgets
tk.Label(janela, text="Produto:").pack(pady=5)
entrada_produto = tk.Entry(janela, width=40)
entrada_produto.pack(pady=5)

botao_buscar = tk.Button(janela, text="Buscar", command=buscar_produto)
botao_buscar.pack(pady=5)

resultado_label = tk.Label(janela, text="", wraplength=350)
resultado_label.pack(pady=5)

link_label = tk.Label(janela, text="", fg="blue", cursor="hand2")
link_label.pack()

# Iniciando a interface
janela.mainloop()
