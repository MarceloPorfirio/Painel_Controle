import flet as ft

def main(page: ft.Page):
    page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.BLUE_700



    # Função para abrir o AlertDialog de adicionar Pokémon
    def open_add_dialog(e):
        text_field_name = ft.TextField(label="Nome do Pokémon", autofocus=True)
        text_field_url = ft.TextField(label="url da imagem")

        actions = ft.Row(
            controls=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton("Adicionar",on_click=lambda e: add_pokemon(text_field_name.value, text_field_url.value, dialog)),
                
            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
       
        dialog = ft.AlertDialog(
            title=ft.Text("Adicionar Pokémon"),
            content=ft.Column(
                width=300,
                height=200,
                controls=[text_field_name,text_field_url,actions]
            ),
            
        )
        page.dialog = dialog
        dialog.open = True
        page.update()


    page.appbar = ft.AppBar(
        
        # leading=ft.Icon(ft.icons.PALETTE),
        leading_width=20,
        title=ft.Text('Minha Coleção',size=28,weight=ft.FontWeight.BOLD,color='white'),
        center_title=True,
        bgcolor=ft.colors.BLUE_700,
        actions=[
        ft.Container(
            content=ft.IconButton(
                icon=ft.icons.ADD,
                icon_size=30,
                icon_color=ft.colors.BLUE_500,
                bgcolor=ft.colors.WHITE,
                tooltip='add card',
                on_click=open_add_dialog
            ),
            padding=ft.padding.only(right=10,top=6)  # Define o padding desejado
        ),
    ]
)
    
    # Lista de imagens das cartas, nomeadas pelo nome dos Pokémon
    images = {
        'squirtle': 'card_1.png',
        'pikachu': 'card_2.png',
        'bulbasaur': 'card_3.png',
        'charmander': 'card_4.png',
        'psyduck': 'card_5.png',
        'pidgey': 'card_6.png',
        'vulpix': 'card_7.png',
    }

    # Função para realizar animações nas cartas
    def change_cards():
        for card in cards.controls:
            card.content.offset.x += card.data * 0.2
            card.content.scale.scale -= card.data * 0.1
            card.content.opacity -= card.data * 0.3
        cards.update()

    # Função para fechar o diálogo
    def close_dialog(e):
        page.dialog.open = False
        page.update()

     # Função para adicionar novo Pokémon ao dicionário e atualizar a exibição
    def add_pokemon(name, url, dialog):
        # Adiciona ao dicionário `images`
        images[name.lower()] = url
        
        # Atualiza as cartas para incluir a nova
        cards.controls.append(
            ft.Dismissible(
                content=ft.Container(
                    image_src=url,
                    border_radius=ft.border_radius.all(10),
                    aspect_ratio=9/16,
                    offset=ft.Offset(x=0, y=0),
                    scale=ft.Scale(scale=1),
                    opacity=1,
                    shadow=ft.BoxShadow(blur_radius=30, color=ft.colors.BLUE_200),
                    animate=ft.Animation(duration=300, curve=ft.AnimationCurve.DECELERATE),
                    animate_offset=True,
                    animate_scale=True,
                    animate_opacity=True
                ),
                data=len(cards.controls),
                on_dismiss=handle_dismiss
            )
        )
        
        # Fecha o diálogo e atualiza a página
        close_dialog(None)
        cards.update()
        page.update()

    # Função para exibir a carta do Pokémon pesquisado
    def search_pokemon(name, dialog):
        name = name.lower()
        if name in images:
            selected_card = ft.Container(
                image_src=images[name],
                border_radius=ft.border_radius.all(10),
                aspect_ratio=9/16,
                offset=ft.Offset(x=0, y=0),
                scale=ft.Scale(scale=1),
                opacity=1,
                shadow=ft.BoxShadow(blur_radius=30, color=ft.colors.BLUE_200),
                animate_offset=True,
                animate_scale=True,
                animate_opacity=True,
                animate=ft.Animation(duration=300, curve=ft.AnimationCurve.DECELERATE)
            )
            dialog.content = ft.Column(
                width=200,
                height=450,
                controls=[
                    selected_card,
                    ft.Row(controls=[
                        ft.TextButton("Fechar", on_click=close_dialog)
                    ], alignment=ft.MainAxisAlignment.END)
                ]
            )
        else:
            dialog.content = ft.Column(
                width=200,
                height=100,
                controls=[
                    ft.Text(f"{name.capitalize()} não encontrado.", color=ft.colors.RED,size=20,weight=ft.FontWeight.BOLD),
                    ft.Row(controls=[
                        ft.TextButton("Fechar", on_click=close_dialog)
                    ], alignment=ft.MainAxisAlignment.END)
                ]
            )
        page.update()

    # Função para abrir o AlertDialog de busca
    def open_search_dialog(e):
        text_field = ft.TextField(label="Nome do Pokémon", autofocus=True)
        search_button = ft.TextButton("Buscar", on_click=lambda e: search_pokemon(text_field.value, dialog))
        
        dialog = ft.AlertDialog(
            title=ft.Text("Buscar Pokémon"),
            content=ft.Column(
                width=200,
                height=100,
                controls=[text_field, search_button]),
            actions=[],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Função para gerenciar o dismiss
    def handle_dismiss(e):
        for num, card in enumerate(cards.controls):
            if e.control == cards.controls[0]:
                cards.controls.clear()
                cards.controls.extend([
                    ft.Dismissible(
                        content=ft.Container(
                            image_src=img,
                            border_radius=ft.border_radius.all(10),
                            aspect_ratio=9/16,
                            offset=ft.Offset(x=0, y=0),
                            scale=ft.Scale(scale=1),
                            opacity=1,
                            shadow=ft.BoxShadow(blur_radius=30, color=ft.colors.BLUE_200),
                            animate=ft.Animation(duration=300, curve=ft.AnimationCurve.DECELERATE),
                            animate_offset=True,
                            animate_scale=True,
                            animate_opacity=True
                        ),
                        data=pos,
                        on_dismiss=handle_dismiss
                    ) for pos, img in reversed(list(enumerate(images.values())))
                ])
            card.data -= 1
            card.content.offset.x = 0
            card.content.opacity = 1
            card.content.scale.scale = 1
        change_cards()

    # Stack com as cartas animadas
    cards = ft.Stack(
        height=400,
        controls=[
            ft.Dismissible(
                content=ft.Container(
                    image_src=img,
                    border_radius=ft.border_radius.all(10),
                    aspect_ratio=9/16,
                    offset=ft.Offset(x=0, y=0),
                    scale=ft.Scale(scale=1),
                    opacity=1,
                    shadow=ft.BoxShadow(blur_radius=30, color=ft.colors.BLUE_200),
                    animate=ft.Animation(duration=300, curve=ft.AnimationCurve.DECELERATE),
                    animate_offset=True,
                    animate_scale=True,
                    animate_opacity=True
                ),
                data=pos,
                on_dismiss=handle_dismiss
            ) for pos, img in reversed(list(enumerate(images.values())))
        ]
    )

    # Configurando o título e o layout
    title = ft.Container(
        margin=ft.margin.only(bottom=40),
        content=ft.Image(
            src='logo_poke.png',
            width=280
        )
    )
    layout = ft.Row(controls=[cards], alignment=ft.MainAxisAlignment.CENTER)

    # Adicionando o FloatingActionButton
    search_button = ft.FloatingActionButton(
        icon=ft.icons.SEARCH,
        tooltip="Buscar Carta",
        on_click=open_search_dialog
    )

    page.add(title, layout)
    page.floating_action_button = search_button
  
    # Aplicando animações iniciais às cartas
    for card in cards.controls:
        card.content.offset.x += card.data * 0.2
        card.content.scale.scale -= card.data * 0.1
        card.content.opacity -= card.data * 0.3

    page.update()

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
