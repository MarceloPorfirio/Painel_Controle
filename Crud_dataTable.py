import flet as ft
import sqlite3

# CRIAR BANCO DE DADOS
conn = sqlite3.connect('Novo_banco.db',check_same_thread=False)
cursor = conn.cursor()

def tabela_base():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS cadastrar( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT,
                   age INT
                   
                   )
 """)
tabela_base()

def main(page:ft.Page):
    name = ft.TextField(label="Nome")
    age = ft.TextField(label="Idade")
    
    # CRIAR E EDITAR ENTRADA
    edit_name = ft.TextField(label="Nome")
    edit_age = ft.TextField(label="Idade")
    edit_id = ft.Text()
    
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('id')),
            ft.DataColumn(ft.Text('Nome')),
            ft.DataColumn(ft.Text('Idade')),
            ft.DataColumn(ft.Text('Ações')),
        ],
        rows=[]
    )
    
    # DELETE FUNCTION
    def deletebtn(e):
        try:
            # Monta a consulta SQL e os valores dos parâmetros
            sql = "DELETE FROM cadastrar WHERE id = ?"
            val = (e.control.data['id'],)  # passando o ID como um valor nos dados

            # Executa a consulta SQL
            cursor.execute(sql, val)
            conn.commit()

            # Recarrega os dados da tabela após a exclusão
            tabela.rows.clear()
            load_data()

            # Adiciona um SnackBar para indicar que o dado foi excluído com sucesso
            page.snack_bar = ft.SnackBar(
                ft.Text('Registro excluído com sucesso', size=30),
                bgcolor='red'
            )
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            print(ex)
            print('Erro ao excluir o registro')
    
    def savedata(e):
       try:
           # Monta a consulta SQL e os valores dos parâmetros
            sql = "UPDATE cadastrar SET name = ?, age = ? WHERE id = ?"
            val = (edit_name.value,edit_age.value,edit_id.value)  # Valores de cada componente
            cursor.execute(sql,val)
            conn.commit()
            dialog.open = False
            page.update()
            
            # LIMPAR CAMPOS DO EDIT
            edit_name.value = ""
            edit_age.value = ""
            edit_id.value = ""
            page.update()
            # Recarrega os dados da tabela após a exclusão
            tabela.rows.clear()
            load_data()

            # Adiciona um SnackBar para indicar que o dado foi alterado com sucesso
            page.snack_bar = ft.SnackBar(
                ft.Text('Registro alterado com sucesso', size=30),
                bgcolor='blue'
            )
            page.snack_bar.open = True
            page.update()
            
       except Exception as e:
           print(e)
           print('Error')
    # CRIAR UM DIALOG QUANDO CLICAR NO EDIT BUTTON
    dialog = ft.AlertDialog(
        title=ft.Text('Edit data'),
        content=ft.Column([
            edit_name,
            edit_age,
        ]),
        actions=[
            ft.TextButton("Save",
                          on_click=savedata)
        ]
    )
    def editbtn(e):
        edit_name.value = e.control.data['name']
        edit_age.value = e.control.data['age']
        edit_id.value = e.control.data['id']
        
        page.dialog = dialog
        dialog.open = True
        page.update()
        
    def load_data():
        cursor.execute("SELECT * FROM cadastrar")
        result  = cursor.fetchall()
        
        # Trasnforma o resultado de uma consulta SQL em uma lista de dicionários
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row))for row in result]
        
        for row in rows:
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['id'])),
                        ft.DataCell(ft.Text(row['name'])),
                        ft.DataCell(ft.Text(row['age'])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton('delete',icon_color='red',
                                              data=row,on_click=deletebtn),
                                 ft.IconButton('create',icon_color='blue',
                                              data=row,on_click=editbtn),
                            ])
                        )
                    ]
                )
            )
        page.update()
    # Chamar a função quando o app é aberto    
    load_data()    
        
    def addtodb(e):
        try:
            cursor.execute("INSERT INTO cadastrar (name,age) VALUES (?, ? )",(name.value,age.value))
            conn.commit()
            tabela.rows.clear()
            load_data()
            
            # Adicionar SnackBar
            page.snack_bar = ft.SnackBar(
                ft.Text('Dados adicionados com Sucesso',size=30),
                bgcolor='green'
            )
            page.snack_bar.open = True
            page.update()
            
        except Exception as e:
            print(e)
            print('Error')
            
        # Após adicionar com sucesso, limpar os campos de input
        name.value = ""
        age.value = ""
        page.update()
        
        
    page.add(
        ft.Column([
            ft.Text('Cadastrar Dados',size=30),
            name,
            age,
            ft.ElevatedButton('Adicionar',on_click=addtodb),
            tabela
            
        ])
    )
    
ft.app(target=main)