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
        # Verifica se os campos obrigatórios estão preenchidos
        if not servico_kg.value or not quantidade_kg.value:
            # Exibe o AlertDialog se algum campo estiver vazio
            page.dialog = ft.AlertDialog(
                title=ft.Text("Campos obrigatórios"),
                content=ft.Text("Por favor, preencha todos os campos antes de continuar."),
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())
                ]
            )
            page.dialog.open = True
            page.update()
            return  # Sai da função sem continuar

        try:
            # Converte a quantidade de kg para número e valida
            quantidade_kg_valor = float(quantidade_kg.value)
            if quantidade_kg_valor <= 0:
                raise ValueError("Quantidade de kg deve ser maior que 0.")
        except ValueError:
            # Exibe o AlertDialog se a quantidade de kg não for válida
            page.dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("A quantidade de kg deve ser um número válido e maior que 0."),
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())
                ]
            )
            page.dialog.open = True
            page.update()
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
        filled=True,
        border_color='transparent',
        bgcolor='white',
        hint_text="Serviço",
        width=500,
        options=[ft.dropdown.Option("Completo"), ft.dropdown.Option("Esfregar"), ft.dropdown.Option("Máquina"), ft.dropdown.Option("Secar")],
    )
    quantidade_kg = ft.TextField(hint_text="Peso (kg)", width=500,filled=True,border_color='transparent', bgcolor='white')
    quantidade_total_pecas = ft.TextField(hint_text="Total Peças", width=500,filled=True,border_color='transparent', bgcolor='white')
    botao_adicionar_kg = ft.ElevatedButton("Salvar", on_click=adicionar_por_kg,width=200)

    tipo_peca_kg = ft.Dropdown(
        filled=True,
        border_color='transparent',
        bgcolor='white',
        hint_text='Tipo de peça',
        options=[ft.dropdown.Option("Bermuda"), ft.dropdown.Option("Camiseta"), ft.dropdown.Option("Cueca"), ft.dropdown.Option("Meia")]
    )
    quantidade_peca_kg = ft.TextField(hint_text="Quantidade",filled=True,border_color='transparent', bgcolor='white')
    botao_adicionar_peca_kg = ft.ElevatedButton("Adicionar Peça", on_click=adicionar_peca_por_kg)
    lista_detalhes_pecas = ft.Column(scroll="adaptive")

    servico_peca = ft.Dropdown(
        border_color='transparent',
        bgcolor='white',
        filled=True,
        hint_text='Serviço por Peça',
        width=500,
        options=[ft.dropdown.Option("Lavagem"), ft.dropdown.Option("Passagem"), ft.dropdown.Option("Secagem")],
    )
    tipo_peca = ft.Dropdown(
        hint_text="Tipo de Peça",
        filled=True,
        bgcolor='white',
        border_color='transparent',
        width=500,
        options=[ft.dropdown.Option("Casaco"), ft.dropdown.Option("Jaqueta"), ft.dropdown.Option("Edredom"), ft.dropdown.Option("Cobertor")]
    )
    quantidade_peca = ft.TextField(hint_text="Quantidade (Peça)",width=246,filled=True,border_color='transparent', bgcolor='white')
    preco_peca = ft.TextField(hint_text="Preço fixo por Peça",width=246,filled=True,border_color='transparent', bgcolor='white')
    botao_adicionar_peca = ft.ElevatedButton("Adicionar por Peça", on_click=adicionar_por_peca,width=300)

    

    # Função para abrir o AlertDialog com o conteúdo do antigo ExpansionPanel
    def abrir_alert_dialog():
        dialog = ft.AlertDialog(
            title=ft.Text("Detalhar Peças por Kg"),
            content=ft.Container(
                padding=10,  # Adiciona padding ao conteúdo
                content=ft.Column(
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
                        
                    ],
                    spacing=30
                ),
                
            ),
            
            actions=[
                ft.Row(controls=[
                    ft.TextButton("Fechar"),
                    ft.TextButton("Salvar",on_click=salvar_pecas),
                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
            ]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def salvar_pecas(e):
        page.dialog.open = False
        page.update()

        # Cria uma SnackBar para exibir a mensagem
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Peças adicionadas com sucesso!"),
            duration=2000  # Duração da mensagem em milissegundos
        )
        page.snack_bar.open = True  # Abre a SnackBar
        page.update()
        

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

    container_kg = ft.Container(
        width=600,
        height=370,
        padding=20,
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.colors.BLUE_200,
        content=ft.Column(
            controls=[
                ft.Row([ft.Text('Serviços por kg',color='white',size=25)],alignment='center'),
                ft.Divider(color='transparent'),
                ft.Row([servico_kg],alignment='center'),
                ft.Row([quantidade_kg],alignment='center'),
                ft.Row([quantidade_total_pecas],alignment='center'),
                ft.Divider(color='transparent'),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                        "Detalhar",
                        icon=ft.icons.ADD,
                        width=200,
                        on_click=lambda e: abrir_alert_dialog()
                ), 
                        botao_adicionar_kg,
                    ],alignment=ft.MainAxisAlignment.SPACE_AROUND
                )

            ]
        )
    )
    
    container_pc = ft.Container(
        width=600,
        height=370,
        padding=20,
        border_radius=ft.border_radius.all(15),
        bgcolor=ft.colors.GREEN_ACCENT_200,
        content=ft.Column(
            controls=[
                ft.Row([ft.Text('Serviços por peça',color='white',size=25)],alignment='center'),
                ft.Divider(color='transparent'),
                ft.Row([servico_peca],alignment='center'),
                ft.Row([tipo_peca],alignment='center'),
                ft.Row([quantidade_peca,preco_peca],alignment='center'),
                ft.Divider(color='transparent'),
                ft.Row([botao_adicionar_peca],alignment='center'),

            ],spacing=12
        )

    )
    
    page.add(
        ft.Row(
            controls=[
                container_kg,container_pc
            ],alignment=ft.MainAxisAlignment.CENTER
        ),
        
        
        
        # ft.Text("Serviços por Peça"),
        # ft.Row([servico_peca, tipo_peca, quantidade_peca, preco_peca, botao_adicionar_peca]),
        ft.Divider(),
        ft.Text("Itens do Pedido:"),
        tabela_pedidos
    )

ft.app(target=main)
