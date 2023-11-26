import json
from operator import itemgetter

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """Adds selection and focus behaviour to the view."""
    touch_deselect_last = BooleanProperty(True)


class SelectableLabelAndImage(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    text_content = StringProperty()
    image_source = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabelAndImage, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabelAndImage, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        books_window = rv.parent.parent
        if rv.layout_manager.selected_nodes:
            rv.index = rv.layout_manager.selected_nodes[0]
            books_window.ids.remove_btn.disabled = False
            books_window.ids.complete_btn.disabled = False
            books_window.ids.edit_btn.disabled = False
        else:
            rv.index = None
            books_window.ids.remove_btn.disabled = True
            books_window.ids.complete_btn.disabled = True
            books_window.ids.edit_btn.disabled = True


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.books = []
        self.load()
        self.index = None

    def load(self):
        try:
            with open("./data/data.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            pass
        self.sort_books()
        self.update_data()

    def save(self):
        with open("./data/data.json", "w") as f:
            json.dump(self.books, f)

    def sort_books(self):
        self.books.sort(key=itemgetter(0, 1, 2))

    def update_data(self):
        self.sort_books()
        self.data = [
            {
                "text_content": f"{author}: {book_name}",
                "image_source": "./icons/tick.png" if status else "./icons/empty.png"
            }
            for status, author, book_name in self.books
        ]
