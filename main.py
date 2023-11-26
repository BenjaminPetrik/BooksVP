from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy import Config
Config.set('graphics', 'fullscreen', 'auto')


class MainWindow(Screen):
    def books_menu_clicked(self):
        self.ids.scr_mngr.current = 'books_menu'
        self.ids.books_btn.state = 'down'
        self.ids.options_btn.state = 'normal'

    def options_menu_clicked(self):
        self.ids.scr_mngr.current = 'options_menu'
        self.ids.books_btn.state = 'normal'
        self.ids.options_btn.state = 'down'


class BooksApp(App):
    def build(self):
        main_window = MainWindow()
        return main_window


if __name__ == '__main__':
    BooksApp().run()
