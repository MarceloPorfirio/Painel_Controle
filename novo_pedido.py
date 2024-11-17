import flet as ft

def main(page: ft.Page):
    page.title = "Sistema de Lavanderia - Pedido"
    page.scroll = "adaptive"

    # Lista para armazenar os serviços adicionados
    servicos_adicionados = []
    # Lista temporária para detalhar peças por Kg
    pecas_por_kg = []

    def atualizar_lista():
        tabela_pedidos.rows.clear()
        for item in servicos_adicionados:
            if "peca" in item:
                tabela_pedidos.rows.append(
                    

                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(item["tipo"])),
                        ft.DataCell(ft.Text(item["peca"])),
                        ft.DataCell(ft.Text(item["quantidade"])),
                        ft.DataCell(ft.Text(item["unidade"])),
                        ft.DataCell(ft.Text(f"R$ {item['preco']}")),
                        ft.DataCell(ft.Text("-"))  # Sem detalhes para serviços por peça
                    ])
                )
            else:
                detalhes_button = ft.IconButton(
                    icon=ft.icons.VISIBILITY,
                    tooltip="Ver detalhes das peças",
                    on_click=lambda e, item=item: mostrar_detalhes_pecas(item["detalhes_pecas"]) if "detalhes_pecas" in item else None
                )
                tabela_pedidos.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(item["tipo"])),
                        ft.DataCell(ft.Text(f"{item['quantidade_kg']} Kg")),
                        ft.DataCell(ft.Text(item["quantidade_total"])),
                        ft.DataCell(ft.Text(item["unidade"])),
                        ft.DataCell(ft.Text(f"R$ {item['preco']}")),
                        ft.DataCell(detalhes_button)
                    ])
                )
        page.update()

    def mostrar_detalhes_pecas(detalhes_pecas):
        detalhes_texto = "\n".join([f"{p['peca']} - {p['quantidade']} peças" for p in detalhes_pecas])
        dialog = ft.AlertDialog(
            title=ft.Text("Detalhes das Peças por Kg"),
            content=ft.Text(detalhes_texto),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def adicionar_peca_por_kg(e):
        # Cria o dicionário da peça detalhada
        peca_detalhada = {
            "peca": tipo_peca_kg.value,
            "quantidade": quantidade_peca_kg.value,
        }
        # Adiciona a peça à lista
        pecas_por_kg.append(peca_detalhada)

        # Atualiza os detalhes das peças
        atualizar_detalhes_pecas()

        # Zera os campos dos TextFields
        tipo_peca_kg.value = ""
        quantidade_peca_kg.value = ""

        # Atualiza os TextFields na interface
        tipo_peca_kg.update()
        quantidade_peca_kg.update()


    def atualizar_detalhes_pecas():
        # Limpa e recria as colunas no painel de expansão
        lista_detalhes_pecas.controls.clear()

        # Cria colunas com containers para adicionar espaço lateral
        col1 = ft.Container(content=ft.Column(), padding=ft.padding.only(left=10, right=10))
        col2 = ft.Container(content=ft.Column(), padding=ft.padding.only(left=10, right=10))
        col3 = ft.Container(content=ft.Column(), padding=ft.padding.only(left=10, right=10))
        col4 = ft.Container(content=ft.Column(), padding=ft.padding.only(left=10, right=10))
        colunas = [col1.content, col2.content, col3.content, col4.content]

        # Divide os itens entre as colunas (6 itens por coluna)
        for i, p in enumerate(pecas_por_kg):
            colunas[i // 5 % 4].controls.append(
                ft.Text(f"{p['peca']} - {p['quantidade']} peças")
            )

        # Adiciona as colunas ao painel
        lista_detalhes_pecas.controls.append(
            ft.Row(controls=[col1, col2, col3, col4], alignment="start")
        )
        lista_detalhes_pecas.update()

    def adicionar_por_kg(e):
        try:
            quantidade_kg_valor = float(quantidade_kg.value)
            if quantidade_kg_valor <= 0:
                page.add(ft.Text("A quantidade de kg deve ser maior que 0", color="red"))
                return
        except ValueError:
            page.add(ft.Text("A quantidade de kg deve ser um número válido", color="red"))
            return

        # Define o preço por kg com base no tipo de serviço
        if servico_kg.value == "Máquina":
            preco_por_kg = 12.00
        elif servico_kg.value == "Completo":
            preco_por_kg = 19.90
        elif servico_kg.value == "Esfregar":
            preco_por_kg = 17.90
        elif servico_kg.value == "Secar":
            preco_por_kg = 10.00
        else:
            preco_por_kg = 0.0

        # Cria o dicionário do serviço
        servico = {
            "tipo": servico_kg.value,
            "quantidade_kg": quantidade_kg.value,
            "quantidade_total": quantidade_total_pecas.value,
            "detalhes_pecas": pecas_por_kg.copy(),
            "unidade": "Kg",
            "preco": round(quantidade_kg_valor * preco_por_kg, 2),
        }

        # Adiciona o serviço à lista e atualiza a interface
        servicos_adicionados.append(servico)
        pecas_por_kg.clear()
        atualizar_detalhes_pecas()
        atualizar_lista()

        # Zera os campos dos TextFields
        servico_kg.value = ""
        quantidade_kg.value = ""
        quantidade_total_pecas.value = ""

        # Atualiza os TextFields na interface
        servico_kg.update()
        quantidade_kg.update()
        quantidade_total_pecas.update()


    def adicionar_por_peca(e):
        servico = {
            "tipo": servico_peca.value,
            "peca": tipo_peca.value,
            "quantidade": quantidade_peca.value,
            "unidade": "Peça(s)",
            "preco": float(preco_peca.value)
        }
        servicos_adicionados.append(servico)
        atualizar_lista()

    # Elementos de entrada para o serviço por kg
    servico_kg = ft.Dropdown(
        label="Serviço",
        options=[ft.dropdown.Option("Completo"), ft.dropdown.Option("Esfregar"), ft.dropdown.Option("Máquina"), ft.dropdown.Option("Secar")],
    )
    quantidade_kg = ft.TextField(label="Peso (kg)", width=150)
    quantidade_total_pecas = ft.TextField(label="Quantidade", width=150)
    botao_adicionar_kg = ft.ElevatedButton("Adicionar Serviço por Kg", on_click=adicionar_por_kg)

    tipo_peca_kg = ft.Dropdown(
        label="Tipo de Peça",
        options=[ft.dropdown.Option("Bermuda"), ft.dropdown.Option("Camiseta"), ft.dropdown.Option("Cueca"), ft.dropdown.Option("Meia")]
    )
    quantidade_peca_kg = ft.TextField(label="Quantidade")
    botao_adicionar_peca_kg = ft.ElevatedButton("Adicionar Peça", on_click=adicionar_peca_por_kg)
    lista_detalhes_pecas = ft.Column(scroll="adaptive")

    servico_peca = ft.Dropdown(
        label="Serviço por Peça",
        options=[ft.dropdown.Option("Lavagem"), ft.dropdown.Option("Passagem"), ft.dropdown.Option("Secagem")],
    )
    tipo_peca = ft.Dropdown(
        label="Tipo de Peça",
        options=[ft.dropdown.Option("Casaco"), ft.dropdown.Option("Jaqueta"), ft.dropdown.Option("Edredom"), ft.dropdown.Option("Cobertor")]
    )
    quantidade_peca = ft.TextField(label="Quantidade (Peça)", width=100)
    preco_peca = ft.TextField(label="Preço fixo por Peça", width=100)
    botao_adicionar_peca = ft.ElevatedButton("Adicionar por Peça", on_click=adicionar_por_peca)

    detalhes_container = ft.Container(
    content=ft.Row([
        ft.Column(
            controls=[
                ft.ExpansionPanelList(
                    expand_icon_color=ft.colors.AMBER,
                    width=1000,
                    elevation=8,
                    divider_color=ft.colors.AMBER,
                    controls=[
                        ft.ExpansionPanel(
                            header=ft.ListTile(title=ft.Text("Detalhar Peças por Kg")),
                            content=ft.Container(
                                padding=10,  # Adiciona padding ao conteúdo
                                content=ft.Row(
                                    controls=[
                                            ft.Column(
                                                controls=[
                                                    tipo_peca_kg,
                                                    quantidade_peca_kg,
                                                    botao_adicionar_peca_kg,
                                                ]
                                            ),
                                            ft.Column(
                                                controls=[
                                                    lista_detalhes_pecas
                                                ]
                                            )
                                    
                                ],spacing=30)
                            )
                        )
                    ]
                )
            ]
        ),
        
    ])
)


    tabela_pedidos = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Tipo")),
            ft.DataColumn(label=ft.Text("Peça/Quantidade")),
            ft.DataColumn(label=ft.Text("Quantidade Total")),
            ft.DataColumn(label=ft.Text("Unidade")),
            ft.DataColumn(label=ft.Text("Preço")),
            ft.DataColumn(label=ft.Text("Detalhes")),
        ]
    )

    page.add(
        ft.Text("Serviços por Kg"),
        ft.Row([servico_kg, quantidade_kg, quantidade_total_pecas]),
        detalhes_container,
        ft.Divider(color=ft.colors.TRANSPARENT),
        botao_adicionar_kg,
        ft.Divider(),
        ft.Text("Serviços por Peça"),
        ft.Row([servico_peca, tipo_peca, quantidade_peca, preco_peca, botao_adicionar_peca]),
        ft.Divider(),
        ft.Text("Itens do Pedido:"),
        tabela_pedidos
    )

ft.app(target=main)
