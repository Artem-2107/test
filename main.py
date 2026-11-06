import sys
import os

# Говорим Python'у, что наши экраны лежат в папке frontend
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

import flet as ft
from views import (
    login_view, register_view, catalog_view, product_view,
    cart_view, orders_view, profile_view, admin_view, favorites_view
)

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Спорт лайф"
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.update()

    def go(self, name, **kw):
        self.page.controls.clear()
        
        try:
            views = {
                "login": lambda: login_view.build(self),
                "register": lambda: register_view.build(self),
                "catalog": lambda: catalog_view.build(self),
                "product": lambda: product_view.build(self, kw.get("product_id")),
                "cart": lambda: cart_view.build(self),
                "orders": lambda: orders_view.build(self),
                "profile": lambda: profile_view.build(self),
                "admin": lambda: admin_view.build(self),
                "favorites": lambda: favorites_view.build(self),
            }
            
            if name in views:
                control = views[name]()
                if control:
                    self.page.controls.append(control)
                else:
                    self.page.controls.append(ft.Text(f"Ошибка: экран {name} пуст"))
            else:
                self.page.controls.append(ft.Text(f"Ошибка: экран {name} не найден"))
        except Exception as e:
            self.page.controls.append(
                ft.Column([
                    ft.Text("ОШИБКА:", color=ft.Colors.RED, weight=ft.FontWeight.BOLD),
                    ft.Text(str(e), color=ft.Colors.WHITE)
                ])
            )
        self.page.update()

    def ok(self, m):
        s = ft.SnackBar(ft.Text(m, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN)
        self.page.overlay.append(s)
        s.open = True
        self.page.update()

    def error(self, m):
        s = ft.SnackBar(ft.Text(m, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
        self.page.overlay.append(s)
        s.open = True
        self.page.update()

def main(page: ft.Page):
    try:
        app = App(page)
        app.go("login")
    except Exception as e:
        page.add(ft.Text(f"Критическая ошибка: {str(e)}", color=ft.Colors.RED))

if __name__ == "__main__":
    # Проверка для разных версий Flet (для ПК и для телефона)
    if hasattr(ft, "run"):
        ft.run(main)
    else:
        ft.app(target=main)
