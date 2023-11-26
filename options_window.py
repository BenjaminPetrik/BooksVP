from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen


class OptionsWindow(Screen):
    def delete_all_books_popup(self):
        content = RelativeLayout()

        buttons = BoxLayout(orientation="horizontal",
                            size_hint=(1, 0.15),
                            pos_hint={"center_x": 0.5, "center_y": 0.05},
                            spacing=10)
        yes_modal_btn = Button(text="Yes")
        no_modal_btn = Button(text="No")
        buttons.add_widget(yes_modal_btn)
        buttons.add_widget(no_modal_btn)

        label = Label(text="Are you sure you want to delete all books?\nThis action cannot be undone!",
                      size_hint=(1, 0.2),
                      pos_hint={"center_x": 0.5, "center_y": 0.6},
                      color=(1, 0, 0, 1))

        content.add_widget(label)
        content.add_widget(buttons)
        remove_popup = Popup(title="Delete all books",
                             content=content)
        remove_popup.open()
        no_modal_btn.bind(on_release=remove_popup.dismiss)
        yes_modal_btn.bind(on_release=lambda instance: self.delete_all_books(remove_popup))

    def delete_all_books(self, popup):
        popup.dismiss()
        app = App.get_running_app()
        rec_view = app.root.ids.books_menu.children[0].ids.rec_view
        rec_view.books.clear()
        rec_view.save()
        rec_view.update_data()
        rec_view.children[0].clear_selection()
