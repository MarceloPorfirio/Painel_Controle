import flet as ft
total_result = ""

def main(page:ft.Page):
    
    page.window_maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def calc_area(e):
        area1_value = float(area1.value) 
        area2_value = float(area2.value)
        calculo_area.content.value = str(round(area1_value * area2_value, 2)) + 'm²'
        page.update()
        
        
    title = ft.Text('Cálculo Facilitado para construção',size=30)
    area_container = ft.Container(
        width=500,
        border=ft.border.all(width=2),
        border_radius=ft.border_radius.all(10),
        padding=10,
        content= ft.Row([
            ft.Column(
            
            controls=[
                area1 := ft.TextField(label='Area 1'),
                area2 := ft.TextField(label='Area 2'),
                ft.ElevatedButton('Calcular',on_click=calc_area)
            ],
            
        ),
           calculo_area :=  ft.Container(
                width=100,
                height=100,
                margin=ft.margin.only(bottom=40,left=40),
                border_radius=ft.border_radius.all(10),
                border=ft.border.all(width=2),
                alignment=ft.alignment.center,
                # bgcolor=ft.colors.RED,
                content=ft.Text(size=20)
                
            ),
           
           
        ]),
  
        
    )
    
    wall_container = ft.Container(
        width=500,
        border=ft.border.all(width=2),
        border_radius=ft.border_radius.all(10),
        padding=10,
        content= ft.Row([
            ft.Column(
            
            controls=[
                area1 := ft.TextField(label='Area 1'),
                area2 := ft.TextField(label='Area 2'),
                ft.ElevatedButton('Calcular',on_click=calc_area)
            ],
            
        ),
        ])
        
    )
    
    main_container = ft.Container(
        bgcolor=ft.colors.CYAN,
        expand=True,
        content=ft.Column(
            controls=[
                
                area_container,
                wall_container
                
            ]
        )
    )
    
    page.add(title,main_container)

ft.app(target=main)