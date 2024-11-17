import flet as ft


class SistemaLavanderia(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.servicos_adicionados = []
        self.pecas_por_kg = []

    def atualizar_lista(self):
        self.tabela_pedidos.rows.clear()
        for item in self.servicos_adicionados:
            if "peca" in item:
                self.tabela_pedidos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["tipo"])),
                            ft.DataCell(ft.Text(item["peca"])),
                            ft.DataCell(ft.Text(item["quantidade"])),
                            ft.DataCell(ft.Text(item["unidade"])),
                            ft.DataCell(ft.Text(f"R$ {item['preco']}")),
                            ft.DataCell(ft.Text("-")),
                        ]
                    )
                )
            else:
                detalhes_button = ft.IconButton(
                    icon=ft.icons.VISIBILITY,
                    tooltip="Ver detalhes das peças",
                    on_click=lambda e, item=item: self.mostrar_detalhes_pecas(item["detalhes_pecas"])
                    if "detalhes_pecas" in item
                    else None,
                )
                self.tabela_pedidos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["tipo"])),
                            ft.DataCell(ft.Text(f"{item['quantidade_kg']} Kg")),
                            ft.DataCell(ft.Text(item["quantidade_total"])),
                            ft.DataCell(ft.Text(item["unidade"])),
                            ft.DataCell(ft.Text(f"R$ {item['preco']}")),
                            ft.DataCell(detalhes_button),
                        ]
                    )
                )
        self.update()

    def mostrar_detalhes_pecas(self, detalhes_pecas):
        detalhes_texto = "\n".join(
            [f"{p['peca']} - {p['quantidade']} peças" for p in detalhes_pecas]
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Detalhes das Peças por Kg"),
            content=ft.Text(detalhes_texto),
            actions=[ft.TextButton("Fechar", on_click=lambda e: self.page.dialog.close())],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.update()

    def adicionar_peca_por_kg(self, e):
        peca_detalhada = {
            "peca": self.tipo_peca_kg.value,
            "quantidade": self.quantidade_peca_kg.value,
        }
        self.pecas_por_kg.append(peca_detalhada)
        self.atualizar_detalhes_pecas()

    def atualizar_detalhes_pecas(self):
        self.lista_detalhes_pecas.controls.clear()

        col1, col2, col3, col4 = ft.Column(), ft.Column(), ft.Column(), ft.Column()
        colunas = [col1, col2, col3, col4]

        for i, p in enumerate(self.pecas_por_kg):
            colunas[i // 6 % 4].controls.append(
                ft.Text(f"{p['peca']} - {p['quantidade']} peças")
            )

        self.lista_detalhes_pecas.controls.append(
            ft.Row(
                controls=[col1, col2, col3, col4],
                alignment="start",
            )
        )
        self.update()

    def adicionar_por_kg(self, e):
        try:
            quantidade_kg_valor = float(self.quantidade_kg.value)
            if quantidade_kg_valor <= 0:
                self.page.add(ft.Text("A quantidade de kg deve ser maior que 0", color="red"))
                return
        except ValueError:
            self.page.add(ft.Text("A quantidade de kg deve ser um número válido", color="red"))
            return

        preco_por_kg = 12.00 if self.servico_kg.value == "Máquina" else 19.90 if self.servico_kg.value == "Completo" else 0.0

        servico = {
            "tipo": self.servico_kg.value,
            "quantidade_kg": self.quantidade_kg.value,
            "quantidade_total": self.quantidade_total_pecas.value,
            "detalhes_pecas": self.pecas_por_kg.copy(),
            "unidade": "Kg",
            "preco": quantidade_kg_valor * preco_por_kg,
        }
        self.servicos_adicionados.append(servico)
        self.pecas_por_kg.clear()
        self.atualizar_detalhes_pecas()
        self.atualizar_lista()

    def adicionar_por_peca(self, e):
        servico = {
            "tipo": self.servico_peca.value,
            "peca": self.tipo_peca.value,
            "quantidade": self.quantidade_peca.value,
            "unidade": "Peça(s)",
            "preco": float(self.preco_peca.value),
        }
        self.servicos_adicionados.append(servico)
        self.atualizar_lista()

    def build(self):
        self.servico_kg = ft.Dropdown(
            label="Serviço",
            options=[
                ft.dropdown.Option("Completo"),
                ft.dropdown.Option("Esfregar"),
                ft.dropdown.Option("Máquina"),
                ft.dropdown.Option("Secagem"),
            ],
        )
        self.quantidade_kg = ft.TextField(label="Peso (kg)", width=150)
        self.quantidade_total_pecas = ft.TextField(label="Total de Peças", width=150)
        self.botao_adicionar_kg = ft.ElevatedButton(
            "Adicionar Serviço por Kg", on_click=self.adicionar_por_kg
        )

        self.tipo_peca_kg = ft.Dropdown(
            label="Tipo de Peça",
            options=[
                ft.dropdown.Option("Bermuda"),
                ft.dropdown.Option("Camiseta"),
                ft.dropdown.Option("Cueca"),
                ft.dropdown.Option("Meia"),
            ],
        )
        self.quantidade_peca_kg = ft.TextField(label="Quantidade", width=100)
        self.botao_adicionar_peca_kg = ft.ElevatedButton(
            "Adicionar Peça", on_click=self.adicionar_peca_por_kg
        )
        self.lista_detalhes_pecas = ft.Column(scroll="adaptive")

        self.servico_peca = ft.Dropdown(
            label="Serviço por Peça",
            options=[
                ft.dropdown.Option("Lavagem"),
                ft.dropdown.Option("Passagem"),
                ft.dropdown.Option("Secagem"),
            ],
        )
        self.tipo_peca = ft.Dropdown(
            label="Tipo de Peça",
            options=[
                ft.dropdown.Option("Casaco"),
                ft.dropdown.Option("Jaqueta"),
                ft.dropdown.Option("Edredom"),
                ft.dropdown.Option("Cobertor"),
            ],
        )
        self.quantidade_peca = ft.TextField(label="Quantidade (Peça)", width=100)
        self.preco_peca = ft.TextField(label="Preço fixo por Peça", width=100)
        self.botao_adicionar_peca = ft.ElevatedButton(
            "Adicionar por Peça", on_click=self.adicionar_por_peca
        )

        detalhes_panel = ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text("Detalhes das Peças por Kg")),
                    content=self.lista_detalhes_pecas,
                )
            ]
        )

        self.tabela_pedidos = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Tipo")),
                ft.DataColumn(label=ft.Text("Peça/Quantidade")),
                ft.DataColumn(label=ft.Text("Quantidade Total")),
                ft.DataColumn(label=ft.Text("Unidade")),
                ft.DataColumn(label=ft.Text("Preço")),
                ft.DataColumn(label=ft.Text("Detalhes")),
            ]
        )

        return ft.Column(
            controls=[
                ft.Text("Serviços por Kg"),
                ft.Row([self.servico_kg, self.quantidade_kg, self.quantidade_total_pecas]),
                detalhes_panel,
                ft.Divider(),
                self.botao_adicionar_kg,
                ft.Divider(),
                ft.Text("Serviços por Peça"),
                ft.Row(
                    [
                        self.servico_peca,
                        self.tipo_peca,
                        self.quantidade_peca,
                        self.preco_peca,
                        self.botao_adicionar_peca,
                    ]
                ),
                ft.Divider(),
                ft.Text("Itens do Pedido:"),
                self.tabela_pedidos,
            ]
        )


def main(page: ft.Page):
    page.title = "Sistema de Lavanderia - Pedido"
    page.add(SistemaLavanderia())


ft.app(target=main)
