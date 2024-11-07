import firebase_admin
from firebase_admin import credentials, firestore
import flet as ft

# Inicialize o Firebase com a chave do serviço
cred = credentials.Certificate("Tutorial_Firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Conectar ao Firestore
db = firestore.client()

def main(page: ft.Page):
    page.title = "Aplicação Flet com Firestore"
    
    # Função para carregar dados do Firestore
    def carregar_dados():
        docs = db.collection("colecao_exemplo").stream()
        dados = [{"id": doc.id, "nome": doc.get("nome"), "idade": doc.get("idade"), "telefone": doc.to_dict().get("telefone","N/A")} for doc in docs]
        return dados

    # Função para excluir dados do Firestore
    def excluir_dado(id):
        try:
            db.collection("colecao_exemplo").document(id).delete()  # Deleta o documento com o ID fornecido
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Documento com ID {id} excluído com sucesso!"))
            page.snack_bar.open = True
            page.update()
            atualizar_tabela()  # Atualiza a tabela após a exclusão
        except Exception as e:
            print(f"Erro ao excluir o documento: {e}")
            page.snack_bar = ft.SnackBar(content=ft.Text("Erro ao excluir o documento!"))
            page.snack_bar.open = True
            page.update()

    # Cria uma tabela em Flet para exibir os dados
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Idade")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("Ações"))
        ],
        rows=[]
    )

    # Função para atualizar a tabela
    def atualizar_tabela():
        tabela.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(dado["nome"])),
                    ft.DataCell(ft.Text(str(dado["idade"]))),
                    ft.DataCell(ft.Text(dado.get("telefone", "N/A"))),
                    ft.DataCell(ft.IconButton(ft.icons.DELETE, on_click=lambda e, id=dado["id"]: excluir_dado(id)))  # Ícone de exclusão
                ]
            ) for dado in carregar_dados()
        ]
        page.update()

    # Campos de entrada para nome e idade
    nome_input = ft.TextField(label="Nome", width=200)
    idade_input = ft.TextField(label="Idade", width=100)
    telefone_input = ft.TextField(label="Telefone", width=200)  # Novo campo de telefone

    # Função para salvar dados no Firestore
    def salvar_dados(e):
        nome = nome_input.value
        idade = idade_input.value
        telefone = telefone_input.value

        # Verifica se os campos estão preenchidos
        if nome and idade and telefone:
            try:
                idade = int(idade)  # Tenta converter a idade para inteiro
                # Adiciona os dados ao Firestore
                db.collection("colecao_exemplo").add({"nome": nome, "idade": idade, "telefone": telefone})
                
                # Limpa os campos de entrada após salvar
                nome_input.value = ""
                idade_input.value = ""
                telefone_input.value = ""

                # Atualiza a tabela para mostrar o novo dado
                atualizar_tabela()
                page.snack_bar = ft.SnackBar(content=ft.Text("Dados salvos com sucesso!"))
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Idade deve ser um número!"))
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Por favor, preencha todos os campos!"))
        
        page.snack_bar.open = True
        page.update()

    # Botão para salvar os dados
    btn_salvar = ft.ElevatedButton(text="Salvar Dados", on_click=salvar_dados)
    # Botão para carregar os dados e atualizar a tabela
    btn_carregar = ft.ElevatedButton(
        text="Carregar Dados",
        on_click=lambda e: atualizar_tabela()
    )

    # Adiciona componentes à página
    page.add(nome_input, idade_input, telefone_input, btn_salvar, btn_carregar, tabela)

# Executar a aplicação Flet
ft.app(target=main)
