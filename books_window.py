from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class BooksWindow(Screen):
    def add_btn_clicked(self):
        content = RelativeLayout()

        inputs = BoxLayout(orientation="vertical",
                           size_hint=(1, 0.3),
                           pos_hint={"center_x": 0.5, "center_y": 0.5},
                           spacing=10)
        author_field = TextInput(hint_text="Author name...")
        book_name_field = TextInput(hint_text="Book name...")
        inputs.add_widget(author_field)
        inputs.add_widget(book_name_field)

        buttons = BoxLayout(orientation="horizontal",
                            size_hint=(1, 0.15),
                            pos_hint={"center_x": 0.5, "center_y": 0.05},
                            spacing=10)
        add_modal_btn = Button(text="Add")
        cancel_modal_btn = Button(text="Cancel")
        buttons.add_widget(add_modal_btn)
        buttons.add_widget(cancel_modal_btn)

        label = Label(size_hint=(1, 0.2),
                      pos_hint={"center_x": 0.5, "center_y": 0.8},
                      color=(1, 0, 0, 1))

        content.add_widget(label)
        content.add_widget(inputs)
        content.add_widget(buttons)
        add_popup = Popup(title="Please, enter an author and a book name in the fields below:",
                          content=content)
        add_popup.open()
        cancel_modal_btn.bind(on_release=add_popup.dismiss)
        add_modal_btn.bind(on_release=lambda instance: self.add_new_book(author=author_field,
                                                                         book_name=book_name_field,
                                                                         label=label,
                                                                         popup=add_popup))

    def add_new_book(self, *, author, book_name, popup, label):
        if author.text and book_name.text:
            self.ids.rec_view.books.append([False, author.text.strip(), book_name.text.strip()])
            self.ids.rec_view.save()
            self.ids.rec_view.update_data()
            popup.dismiss()

            ind = self.ids.rec_view.books.index([False, author.text.strip(), book_name.text.strip()])
            self.select_node(ind)

        else:
            label.text = "Fields cannot be empty"
            if not author.text:
                with author.canvas:
                    Color(1, 0, 0, 1)
                    Line(width=2, rectangle=(author.x, author.y, author.width, author.height))
            if not book_name.text:
                with book_name.canvas:
                    Color(1, 0, 0, 1)
                    Line(width=2, rectangle=(book_name.x, book_name.y, book_name.width, book_name.height))

    def edit_btn_clicked(self):
        content = RelativeLayout()

        inputs = BoxLayout(orientation="vertical",
                           size_hint=(1, 0.3),
                           pos_hint={"center_x": 0.5, "center_y": 0.5},
                           spacing=10)
        author_field = TextInput(hint_text="Author name...")
        book_name_field = TextInput(hint_text="Book name...")
        inputs.add_widget(author_field)
        inputs.add_widget(book_name_field)

        buttons = BoxLayout(orientation="horizontal",
                            size_hint=(1, 0.15),
                            pos_hint={"center_x": 0.5, "center_y": 0.05},
                            spacing=10)
        edit_modal_btn = Button(text="Edit")
        cancel_modal_btn = Button(text="Cancel")
        buttons.add_widget(edit_modal_btn)
        buttons.add_widget(cancel_modal_btn)

        label = Label(size_hint=(1, 0.2),
                      pos_hint={"center_x": 0.5, "center_y": 0.8},
                      color=(1, 0, 0, 1))

        content.add_widget(label)
        content.add_widget(inputs)
        content.add_widget(buttons)
        edit_popup = Popup(title="Please, edit an author, a book name or both in the fields below:",
                           content=content)
        edit_popup.open()
        cancel_modal_btn.bind(on_release=edit_popup.dismiss)
        edit_modal_btn.bind(on_release=lambda instance: self.edit_book(author=author_field,
                                                                       book_name=book_name_field,
                                                                       label=label,
                                                                       popup=edit_popup))

    def edit_book(self, *, author, book_name, popup, label):
        if author.text or book_name.text:
            status, old_author, old_book_name = self.ids.rec_view.books[self.ids.rec_view.index]
            self.ids.rec_view.books[self.ids.rec_view.index] = (
                [False,
                 author.text.strip() if author.text else old_author,
                 book_name.text.strip() if book_name.text else old_book_name])
            self.ids.rec_view.save()
            self.ids.rec_view.update_data()
            popup.dismiss()

            ind = self.ids.rec_view.books.index(
                [False,
                 author.text.strip() if author.text else old_author,
                 book_name.text.strip() if book_name.text else old_book_name])
            self.select_node(ind)

        else:
            label.text = "Fields cannot be empty"
            if not author.text and not book_name.text:
                with author.canvas:
                    Color(1, 0, 0, 1)
                    Line(width=2, rectangle=(author.x, author.y, author.width, author.height))
                with book_name.canvas:
                    Color(1, 0, 0, 1)
                    Line(width=2, rectangle=(book_name.x, book_name.y, book_name.width, book_name.height))

    def remove_btn_clicked(self):
        content = RelativeLayout()

        buttons = BoxLayout(orientation="horizontal",
                            size_hint=(1, 0.15),
                            pos_hint={"center_x": 0.5, "center_y": 0.05},
                            spacing=10)
        yes_modal_btn = Button(text="Yes")
        no_modal_btn = Button(text="No")
        buttons.add_widget(yes_modal_btn)
        buttons.add_widget(no_modal_btn)

        label = Label(text="Are you sure you want to delete the book?",
                      size_hint=(1, 0.2),
                      pos_hint={"center_x": 0.5, "center_y": 0.6},
                      color=(1, 0, 0, 1))

        content.add_widget(label)
        content.add_widget(buttons)
        remove_popup = Popup(title="Delete book",
                           content=content)
        remove_popup.open()
        no_modal_btn.bind(on_release=remove_popup.dismiss)
        yes_modal_btn.bind(on_release=lambda instance: self.delete_book(remove_popup))

    def delete_book(self, popup):
        popup.dismiss()
        self.ids.rec_view.books.pop(self.ids.rec_view.index)
        self.ids.rec_view.children[0].clear_selection()
        self.ids.rec_view.save()
        self.ids.rec_view.update_data()

    def complete_btn_clicked(self):
        status, author, book_name = self.ids.rec_view.books[self.ids.rec_view.index]
        status = not status
        self.ids.rec_view.books[self.ids.rec_view.index] = [status, author, book_name]
        self.ids.rec_view.save()
        self.ids.rec_view.update_data()
        ind = self.ids.rec_view.books.index([status, author, book_name])
        self.select_node(ind)

    def select_node(self, ind):
        rv_layout = self.ids.rec_view.children[0]
        rv_layout.select_node(ind)
