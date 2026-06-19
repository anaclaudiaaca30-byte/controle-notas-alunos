import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Sistema de Notas e Atividades")
janela.geometry("900x650")

titulo = ctk.CTkLabel(
    janela,
    text="Sistema de Notas e Atividades dos Alunos",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=20)

frame = ctk.CTkFrame(janela)
frame.pack(pady=10, padx=20, fill="both", expand=True)

# Dados do aluno
entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome do aluno", width=300)
entry_nome.grid(row=0, column=0, padx=10, pady=10)

entry_turma = ctk.CTkEntry(frame, placeholder_text="Turma", width=150)
entry_turma.grid(row=0, column=1, padx=10, pady=10)

entry_bimestre = ctk.CTkEntry(frame, placeholder_text="Bimestre", width=150)
entry_bimestre.grid(row=0, column=2, padx=10, pady=10)

# Avaliação
label_avaliacao = ctk.CTkLabel(frame, text="Cálculo da Avaliação", font=("Arial", 18, "bold"))
label_avaliacao.grid(row=1, column=0, columnspan=3, pady=15)

entry_acertos = ctk.CTkEntry(frame, placeholder_text="Quantidade de acertos", width=220)
entry_acertos.grid(row=2, column=0, padx=10, pady=10)

entry_erros = ctk.CTkEntry(frame, placeholder_text="Quantidade de erros", width=220)
entry_erros.grid(row=2, column=1, padx=10, pady=10)

entry_valor_acerto = ctk.CTkEntry(frame, placeholder_text="Valor por acerto ex: 0.25", width=220)
entry_valor_acerto.grid(row=3, column=0, padx=10, pady=10)

entry_valor_erro = ctk.CTkEntry(frame, placeholder_text="Valor por erro ex: -0.25", width=220)
entry_valor_erro.grid(row=3, column=1, padx=10, pady=10)

# Atividades
label_atividades = ctk.CTkLabel(frame, text="Cálculo das Atividades", font=("Arial", 18, "bold"))
label_atividades.grid(row=4, column=0, columnspan=3, pady=15)

entry_total_atividades = ctk.CTkEntry(frame, placeholder_text="Total de atividades propostas", width=220)
entry_total_atividades.grid(row=5, column=0, padx=10, pady=10)

entry_atividades_feitas = ctk.CTkEntry(frame, placeholder_text="Atividades realizadas", width=220)
entry_atividades_feitas.grid(row=5, column=1, padx=10, pady=10)

entry_valor_atividade = ctk.CTkEntry(frame, placeholder_text="Valor por atividade ex: 0.50", width=220)
entry_valor_atividade.grid(row=6, column=0, padx=10, pady=10)

# Resultado
label_resultado = ctk.CTkLabel(
    frame,
    text="Nota final: 0.00",
    font=("Arial", 20, "bold")
)
label_resultado.grid(row=7, column=0, columnspan=3, pady=20)

def calcular():
    try:
        acertos = float(entry_acertos.get())
        erros = float(entry_erros.get())
        valor_acerto = float(entry_valor_acerto.get().replace(",", "."))
        valor_erro = float(entry_valor_erro.get().replace(",", "."))

        atividades_feitas = float(entry_atividades_feitas.get())
        valor_atividade = float(entry_valor_atividade.get().replace(",", "."))

        nota_avaliacao = (acertos * valor_acerto) + (erros * valor_erro)
        nota_atividades = atividades_feitas * valor_atividade
        nota_final = nota_avaliacao + nota_atividades

        label_resultado.configure(
            text=f"Nota avaliação: {nota_avaliacao:.2f} | Nota atividades: {nota_atividades:.2f} | Nota final: {nota_final:.2f}"
        )

    except:
        messagebox.showerror("Erro", "Preencha os campos numéricos corretamente.")

def limpar():
    entry_nome.delete(0, "end")
    entry_turma.delete(0, "end")
    entry_bimestre.delete(0, "end")
    entry_acertos.delete(0, "end")
    entry_erros.delete(0, "end")
    entry_valor_acerto.delete(0, "end")
    entry_valor_erro.delete(0, "end")
    entry_total_atividades.delete(0, "end")
    entry_atividades_feitas.delete(0, "end")
    entry_valor_atividade.delete(0, "end")
    label_resultado.configure(text="Nota final: 0.00")

botao_calcular = ctk.CTkButton(frame, text="Calcular Nota", command=calcular)
botao_calcular.grid(row=8, column=0, padx=10, pady=20)

botao_limpar = ctk.CTkButton(frame, text="Limpar Campos", command=limpar)
botao_limpar.grid(row=8, column=1, padx=10, pady=20)

janela.mainloop()