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
            if "peca" in item:
                lista_pedidos.controls.append(
                    ft.Text(f"{item['tipo']} - {item['peca']} - {item['quantidade']} ({item['unidade']}) - R$ {item['preco']}")
                )
            else:
                # Exibe detalhes de peças por Kg, mas oculta a quantidade se não for informada
                detalhes_pecas = ", ".join(
                    [f"{p['peca']} ({p['quantidade']})" if p['quantidade'] else p['peca'] for p in item["detalhes_pecas"]]
                )
                lista_pedidos.controls.append(
                    ft.Text(f"{item['tipo']} - {item['quantidade_kg']} Kg" +
                            (f" - {item['quantidade_total']} peças" if item['quantidade_total'] else "") +
                            f" - {detalhes_pecas} - R$ {item['preco']}")
                )
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
        # Verifica se a quantidade e o preço são válidos
        try:
            quantidade_kg_valor = float(quantidade_kg.value)
            if quantidade_kg_valor <= 0:
                page.add(ft.Text("A quantidade de kg deve ser maior que 0", color="red"))
                return
        except ValueError:
            page.add(ft.Text("A quantidade de kg deve ser um número válido", color="red"))
            return

        # Verifica o preço baseado no tipo de serviço
        if servico_kg.value == "Máquina":
            preco_por_kg = 12.00
        elif servico_kg.value == "Completo":
            preco_por_kg = 19.90
        else:
            preco_por_kg = 0.0  # Se não for especificado, preço será 0

        # Calcula o preço com base na quantidade e no tipo de serviço
        servico = {
            "tipo": servico_kg.value,
            "quantidade_kg": quantidade_kg.value,
            "quantidade_total": quantidade_total_pecas.value,  # Total de peças informadas
            "detalhes_pecas": pecas_por_kg.copy(),  # Copia os detalhes das peças
            "unidade": "Kg",
            "preco": quantidade_kg_valor * preco_por_kg
        }
        servicos_adicionados.append(servico)
        pecas_por_kg.clear()  # Limpa a lista temporária de detalhes de peças
        atualizar_detalhes_pecas()  # Limpa a exibição das peças detalhadas
        atualizar_lista()

    # Função para adicionar serviço por peça
    def adicionar_por_peca(e):
        servico = {
            "tipo": servico_peca.value,
            "peca": tipo_peca.value,  # Nome da peça selecionada
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
    quantidade_total_pecas = ft.TextField(label="Quantidade Total de Peças", width=150)  # Quantidade total de peças
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
    preco_peca = ft.TextField(label="Preço fixo por Peça", width=100, value="15.0")  # Exemplo de preço fixo por peça
    botao_adicionar_peca = ft.ElevatedButton("Adicionar por Peça", on_click=adicionar_por_peca)

    # Lista para mostrar os serviços adicionados
    lista_pedidos = ft.Column(scroll="adaptive")

    # Layout principal
    page.add(
        ft.Text("Serviços por Kg"),
        ft.Row([servico_kg, quantidade_kg, quantidade_total_pecas, botao_adicionar_kg]),
        ft.Text("Detalhar Peças no Serviço por Kg"),
        ft.Row([tipo_peca_kg, quantidade_peca_kg, botao_adicionar_peca_kg]),
        lista_detalhes_pecas,  # Exibe a lista de detalhes de peças para o serviço por Kg
        ft.Divider(),
        ft.Text("Serviços por Peça"),
        ft.Row([servico_peca, tipo_peca, quantidade_peca, preco_peca, botao_adicionar_peca]),
        ft.Divider(),
        ft.Text("Itens do Pedido:"),
        lista_pedidos
    )

ft.app(target=main)
