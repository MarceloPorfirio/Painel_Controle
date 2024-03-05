import flet as ft


def main(page:ft.Page):
    
    page.window_maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def calc_area(e):
        ...
        
    title = ft.Text('Cálculo Facilitado para construção',size=30)
    area_container = ft.Container(
        width=500,
        border=ft.border.all(width=2),
        border_radius=ft.border_radius.all(10),
        padding=10,
        content= ft.Row(
        
            [
            ft.Column(
            
            controls=[
                area1 := ft.TextField(label='Area 1'),
                area2 := ft.TextField(label='Area 2'),
                ft.ElevatedButton('Calcular',on_click=calc_area)
            ],
            
        ),
            ft.Container(
                width=100,
                height=100,
                margin=ft.margin.only(bottom=40,left=40),
                border_radius=ft.border_radius.all(10),
                border=ft.border.all(width=2),
                alignment=ft.alignment.center,
                # bgcolor=ft.colors.RED,
                content=ft.Text('Resultado')
            )
        ]),
        
        
        
        
        
    )
    
    main_container = ft.Container(
        bgcolor=ft.colors.CYAN,
        expand=True,
        content=ft.Column(
            controls=[
                
                area_container,
            ]
        )
    )
    
    page.add(title,main_container)

ft.app(target=main)