import flet as ft

class Painel:
    def __init__(self,page: ft.Page):
        self.page = page
        
        self.main_page()
        
    def table_container(self):
        return ft.Container
             
    def main_page(self):
        name = ft.TextField(label='Digite seu nome')
        fone = ft.TextField(label='Digite seu telefone')
        email = ft.TextField(label='Digite seu email')
        adress = ft.TextField(label='Digite seu endereço')
        
        
        
        
        container_cadastro = ft.Column(
            
                [name,fone,email,adress]
                    )
        
        table = ft.DataTable(
                    columns=[
                        ft.DataColumn(label=ft.Text("ID")),
                        ft.DataColumn(label=ft.Text("Nome")),
                        ft.DataColumn(label=ft.Text("Telefone"),numeric=True),
                        ft.DataColumn(label=ft.Text("Email")),
                        ft.DataColumn(label=ft.Text('Endereço'))
                    ],
                    rows=[]
            
        )
        
        def add_new(e):
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(len(table.rows))),
                        ft.DataCell(name.value),
                        ft.DataCell(fone.value),
                        ft.DataCell(email.value),
                        ft.DataCell(name.value),

                    ],
            # on_select_changed=lambda e:editindex(e.control.cells[0].content.value,e.control.cells[1].content.value,e.control.cells[2].content.value,e.control.cells[3].content.value)
                )
            )
            name.value = ""
            self.page.update()
        enviar = ft.ElevatedButton('Enviar',on_click=add_new)
    
        self.page.add(container_cadastro,enviar,table)
        
        
    
ft.app(target=Painel)