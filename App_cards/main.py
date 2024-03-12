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
    
    
        
    
    def change_cards():
        for card in cards.controls:
            card.content.offset.x += card.data * 0.2
            card.content.scale.scale -= card.data * 0.1
            card.content.opacity -= card.data * 0.3
        cards.update()
        
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
                    shadow=ft.BoxShadow(blur_radius=30,color=ft.colors.BLUE_200),
                    animate=ft.Animation(duration=300,curve=ft.AnimationCurve.DECELERATE),
                    animate_offset=True,
                    animate_scale=True,
                    animate_opacity=True
                                        
                    
                     
                ),
                data=pos,
                on_dismiss=handle_dismiss
                
            )for pos, img in reversed(list(enumerate(images)))
        ]
    )
                
            card.data -=1
            card.content.offset.x = 0
            card.content.opacity = 1
            card.content.scale.scale = 1
        change_cards()
        
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
                    shadow=ft.BoxShadow(blur_radius=30,color=ft.colors.BLUE_200),
                    animate=ft.Animation(duration=300,curve=ft.AnimationCurve.DECELERATE),
                    animate_offset=True,
                    animate_scale=True,
                    animate_opacity=True
                                        
                    
                     
                ),
                data=pos,
                on_dismiss=handle_dismiss
                
            )for pos, img in reversed(list(enumerate(images)))
        ]
    )
    
    title = ft.Container(
        margin=ft.margin.only(bottom=40),
        content=ft.Image(
            src='assets/logo_poke.png',
            width=300
            
        )
    )
    layout = ft.Row(controls=[cards], alignment=ft.MainAxisAlignment.CENTER)
    
    
    page.add(title,layout)
    
    for card in cards.controls:
        card.content.offset.x += card.data * 0.2
        card.content.scale.scale -= card.data * 0.1
        card.content.opacity -= card.data * 0.3
        
        
    page.update()
    
if __name__ == '__main__':
    ft.app(target=main,assets_dir='assets')