
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            data_row_color={"hovered": "0x30FF0000"},
            columns=[
                ft.DataColumn(
                    ft.Text("Usuário"),
                ),
                ft.DataColumn(
                    ft.Text("E-mail"),
                ),
            ],
            rows=[
                ft.DataRow(
                    cells = [
                        ft.DataCell(
                            ft.Text("João da Silva")
                        ), 
                        ft.DataCell(
                            ft.Text(
                                value="joaodasilva@mail.com", 
                                max_lines=1, 
                                overflow=ft.TextOverflow.ELLIPSIS,
                                width=100,
                            )
                        ),
                    ],
                ),
                ft.DataRow(
                    cells = [
                        ft.DataCell(
                            ft.Text("Maria da Silva")
                        ), 
                        ft.DataCell(
                            ft.Text("mariadasilva@mail.com")
                        ),
                    ]
                ),
            ],
        ),
    )

ft.app(target=main)