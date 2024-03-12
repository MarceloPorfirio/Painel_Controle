import flet as ft

def main(page: ft.Page):
    page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    images = [
        'assets/card_1.png',
        'assets/card_2.png',
        'assets/card_3.png',
        'assets/card_4.png',
        'assets/card_5.png',
        'assets/card_6.png',
        'assets/card_7.png',
    ]

    cards = ft.Stack(
        height=400,
        controls=[
            ft.Dismissible(
                content=ft.Container(
                    image_src=img,  # Assuming img is correctly defined elsewhere
                    border_radius=ft.border_radius.all(10),
                    aspect_ratio=9/16,
                    scale=ft.Offset(x=0, y=0),
                    opacity=1,
                    shadow=ft.BoxShadow(blur_radius=50, color=ft.colors.BLUE_200),
                    animate=ft.Animation(duration=300, curve=ft.AnimationCurve.DECELERATE),
                    animate_offset=True,
                    animate_opacity=True
                )
            ) for img in images  # Use img directly if it's a list of image paths
        ]
    )

    layout = ft.Row(controls=[cards], alignment=ft.MainAxisAlignment.CENTER)
    page.add(layout)

    for card in cards.controls:
        if card.content is not None:  # Check if content exists before accessing offset
            card.content.offset.x += card.data * 0.2

    page.update()

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
