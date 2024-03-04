import flet as ft

def main(page:ft.Page):
    def change_route(e):
        match e.control.selected_index:
            case 0:
                page.go('/')
            case 1:
                page.go('/novo_cliente')
            case 2:
                page.go('/novo_pedido')
            case 3:
                page.go('/consultar_pedido')
            case 4:
                page.go('/nova_despesa')
                
    def route_change(route):
        page.window_maximized = True
        page.views.clear()
        page.views.append(
            ft.View(
                
                route='/',
                appbar=ft.AppBar(
                    title=ft.Text('Menu'),
                   
                ),
                controls=[
                     ft.Container(
                        alignment=ft.alignment.center,
                        expand=True,
                        )
                    
                ],
                drawer=ft.NavigationDrawer(
                    controls=[
                        ft.NavigationDrawerDestination(
                           label='Home',
                           icon=ft.icons.HOME 
                        ),
                         ft.NavigationDrawerDestination(
                           label='Calculo de área',
                           icon=ft.icons.PERSON_2_ROUNDED 
                        ),
                          ft.NavigationDrawerDestination(
                           label='Novo Pedido',
                           icon=ft.icons.ADD
                        ),
                          ft.NavigationDrawerDestination(
                            label='Consultar Pedido',
                            icon=ft.icons.SEARCH                              
                        ),
                          ft.Divider(),
                          ft.NavigationDrawerDestination(
                            label='Adicionar Despesas',
                            icon=ft.icons.ADD                             
                        ),
                    ],
                    on_change=change_route
                  
                )
                
            )
            
        )
        
        if page.route == '/novo_cliente':
            page.views.append(
                ft.View(
                route='/novo_cliente',
                appbar=ft.AppBar(
                    title=ft.Text('Novo Cliente')
                ),
                controls=[
                   ft.Container(
                        alignment=ft.alignment.center,
                        expand=True,
                        )
                    
                ],vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
            )
        if page.route == '/novo_pedido': 
            page.views.append(    
                ft.View(
                route='/novo_pedido',
                appbar=ft.AppBar(
                    title=ft.Text('Novo Pedido')
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        expand=True,
                        )
                
                ]        
            )
            )
        if page.route == '/consultar_pedido': 
            page.views.append(    
                ft.View(
                route='/consultar_pedido',
                appbar=ft.AppBar(
                    title=ft.Text('Consultar Pedidos')
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        expand=True,
                        )
                
                ]        
            )
            )
        if page.route == '/nova_despesa': 
            page.views.append(    
                ft.View(
                route='/nova_despesa',
                appbar=ft.AppBar(
                    title=ft.Text('Adicionar Despesa')
                ),
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        expand=True,
                        )
                
                ]        
            )
            )
        
        page.update()
        
    def view_pop(view):
        page.views.pop() # remove a ultima view
        page.update()
        top_view = page.views[-1] # volta para a ultima tela
        page.go(top_view.route)
        
   
        
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    

ft.app(target=main)