import flet as ft

def main(page: ft.Page):
    page.title = "Sistema de Lavanderia - Pedido"
    page.scroll = "adaptive"

    # Lista para armazenar os serviços adicionados
    servicos_adicionados = []
    # Lista temporária para detalhar peças por Kg
    pecas_por_kg = []

    def atualizar_lista():
        lista_pedidos.controls.clear()
        for item in servicos_adicionados:
            # Ícone para visualizar detalhes das peças por Kg
            icon_button = ft.IconButton(
                icon=ft.icons.VISIBILITY,
                tooltip="Ver detalhes das peças",
                on_click=lambda e, item=item: mostrar_detalhes_pecas(item["detalhes_pecas"]) if "detalhes_pecas" in item else None
            )

            if "peca" in item:
                lista_pedidos.controls.append(
                    ft.Row(
                        [ft.Text(f"{item['tipo']} - {item['peca']} - {item['quantidade']} ({item['unidade']}) - R$ {item['preco']}")]
                    )
                )
            else:
                lista_pedidos.controls.append(
                    ft.Row(
                        [ft.Text(f"{item['tipo']} - {item['quantidade_kg']} Kg - R$ {item['preco']}"), icon_button]
                    )
                )
        page.update()

    # Função para exibir um dialog com detalhes das peças por Kg
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

    # Função para adicionar peça ao detalhe de peças por Kg
    def adicionar_peca_por_kg(e):
        peca_detalhada = {
            "peca": tipo_peca_kg.value,
            "quantidade": quantidade_peca_kg.value,
        }
        pecas_por_kg.append(peca_detalhada)
        atualizar_detalhes_pecas()

    # Função para atualizar a exibição das peças por Kg detalhadas
    def atualizar_detalhes_pecas():
        lista_detalhes_pecas.controls.clear()
        for p in pecas_por_kg:
            lista_detalhes_pecas.controls.append(
                ft.Text(f"{p['peca']} - {p['quantidade']} peças")
            )
        page.update()

    # Função para adicionar o serviço por Kg com os detalhes das peças e quantidade total
    def adicionar_por_kg(e):
        try:
            quantidade_kg_valor = float(quantidade_kg.value)
            if quantidade_kg_valor <= 0:
                page.add(ft.Text("A quantidade de kg deve ser maior que 0", color="red"))
                return
        except ValueError:
            page.add(ft.Text("A quantidade de kg deve ser um número válido", color="red"))
            return

        if servico_kg.value == "Máquina":
            preco_por_kg = 12.00
        elif servico_kg.value == "Completo":
            preco_por_kg = 19.90
        else:
            preco_por_kg = 0.0

        servico = {
            "tipo": servico_kg.value,
            "quantidade_kg": quantidade_kg.value,
            "quantidade_total": quantidade_total_pecas.value,
            "detalhes_pecas": pecas_por_kg.copy(),
            "unidade": "Kg",
            "preco": quantidade_kg_valor * preco_por_kg
        }
        servicos_adicionados.append(servico)
        pecas_por_kg.clear()
        atualizar_detalhes_pecas()
        atualizar_lista()

    # Função para adicionar serviço por peça
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
        label="Serviço por Kg",
        options=[ft.dropdown.Option("Completo"), ft.dropdown.Option("Secagem"), ft.dropdown.Option("Máquina")],
    )
    quantidade_kg = ft.TextField(label="Quantidade (Kg)", width=100)
    quantidade_total_pecas = ft.TextField(label="Quantidade Total de Peças", width=150)
    botao_adicionar_kg = ft.ElevatedButton("Adicionar Serviço por Kg", on_click=adicionar_por_kg)

    # Campos para detalhar peças no serviço por Kg
    tipo_peca_kg = ft.Dropdown(
        label="Tipo de Peça",
        options=[
            ft.dropdown.Option("Bermuda"),
            ft.dropdown.Option("Camiseta"),
            ft.dropdown.Option("Cueca"),
            ft.dropdown.Option("Meia")
        ]
    )
    quantidade_peca_kg = ft.TextField(label="Quantidade", width=100)
    botao_adicionar_peca_kg = ft.ElevatedButton("Adicionar Peça", on_click=adicionar_peca_por_kg)

    # Lista para mostrar os detalhes das peças adicionadas ao serviço por Kg
    lista_detalhes_pecas = ft.Column(scroll="adaptive")

    # Elementos de entrada para o serviço por peça
    servico_peca = ft.Dropdown(
        label="Serviço por Peça",
        options=[ft.dropdown.Option("Lavagem à mão"), ft.dropdown.Option("Passagem")],
    )
    tipo_peca = ft.Dropdown(
        label="Tipo de Peça",
        options=[
            ft.dropdown.Option("Casaco"),
            ft.dropdown.Option("Jaqueta"),
            ft.dropdown.Option("Edredom"),
            ft.dropdown.Option("Cobertor")
        ]
    )
    quantidade_peca = ft.TextField(label="Quantidade (Peça)", width=100)
    preco_peca = ft.TextField(label="Preço fixo por Peça", width=100, value="15.0")
    botao_adicionar_peca = ft.ElevatedButton("Adicionar por Peça", on_click=adicionar_por_peca)

    # Lista para mostrar os serviços adicionados
    lista_pedidos = ft.Column(scroll="adaptive")

    # Layout principal
    page.add(
        ft.Text("Serviços por Kg"),
        ft.Row([servico_kg, quantidade_kg, quantidade_total_pecas, botao_adicionar_kg]),
        ft.Text("Detalhar Peças no Serviço por Kg"),
        ft.Row([tipo_peca_kg, quantidade_peca_kg, botao_adicionar_peca_kg]),
        lista_detalhes_pecas,
        ft.Divider(),
        ft.Text("Serviços por Peça"),
        ft.Row([servico_peca, tipo_peca, quantidade_peca, preco_peca, botao_adicionar_peca]),
        ft.Divider(),
        ft.Text("Itens do Pedido:"),
        lista_pedidos
    )

ft.app(target=main)
