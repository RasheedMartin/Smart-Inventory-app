from kivy.uix.behaviors import FocusBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.clock import Clock
from barcode_reader import scan_barcodes, \
    get_price, create_database, update_database, get_unique_categories, \
    checking, create_user_database, add_user, login, get_name, get_products, \
    get_password, get_username, get_email, verify_password, verify_username

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
# from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle

# from kivy.uix.image import AsyncImage

# Window.clearcolor = (0.5, 0.5, 0.5, 1)
# Window.size = (400, 400)
Window.minimum_width, Window.minimum_height = (400, 400)


class HomeWindow(Screen):
    pass


class ForgotPasswordWindow(Screen):
    def on_release_button(self):
        username = self.ids.username_vertification.text
        email = self.ids.email_vertification.text

        username_result, email_result, result = get_password(username, email)
        if username_result and email_result:
            self.ids.get_password.text = result
        else:
            self.ids.get_password.text = ''
            ForgotPasswordErrorPopup().open()


class ForgotUsernameWindow(Screen):
    def on_release_button(self):
        firstname = self.ids.firstname_vertification.text
        lastname = self.ids.lastname_vertification.text
        email = self.ids.email1_vertification.text

        firstname_result, lastname_result, email_result, result = get_username(firstname, lastname, email)
        if firstname_result and lastname_result and email_result:
            self.ids.get_username.text = result
        else:
            self.ids.get_username.text = ''
            ForgotUsernameErrorPopup().open()


class SignUpWindow(Screen):
    def on_release_button(self):
        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        email = self.ids.email.text
        username = self.ids.username.text
        password = self.ids.password_text.text

        # Check to see if any field is blank or is all spaces

        for x in [firstname, lastname, email, username, password]:
            if x.isspace() or x == '' or x is None:
                SignUpErrorPopup().open()
                break
        else:
            self.manager.userid = add_user(username, password, firstname, lastname, email)
            if self.manager.userid == '':
                if get_email(self.ids.email.text):
                    self.ids.firstname.text = ''
                    self.ids.lastname.text = ''
                    self.ids.email.text = ''
                    self.ids.username.text = ''
                    self.ids.password_text.text = ''
                    ExistingEmailErrorPopup().open()
                elif verify_username(self.ids.username.text):
                    self.ids.firstname.text = ''
                    self.ids.lastname.text = ''
                    self.ids.email.text = ''
                    self.ids.username.text = ''
                    self.ids.password_text.text = ''
                    UsernameTakenErrorPopup().open()
                elif not verify_password(self.ids.email.text):
                    self.ids.firstname.text = ''
                    self.ids.lastname.text = ''
                    self.ids.email.text = ''
                    self.ids.username.text = ''
                    self.ids.password_text.text = ''
                    SimplePasswordErrorPopup().open()

            else:
                self.ids.firstname.text = ''
                self.ids.lastname.text = ''
                self.ids.email.text = ''
                self.ids.username.text = ''
                self.ids.password_text.text = ''
                SignUpSuccessPopup().open()
                self.manager.current = 'login'


class LoginWindow(Screen):
    def on_release_button(self):

        username, password, result = login(self.ids.username_login.text,
                                           self.ids.password_login.text)

        if self.ids.username_login.text == '':
            self.ids.username_login.text = ''
            self.ids.password_login.text = ''
            UsernameBlankErrorPopup().open()

        elif self.ids.password_login.text == '':
            self.ids.username_login.text = ''
            self.ids.password_login.text = ''
            PasswordBlankErrorPopup().open()

        elif not username:
            self.ids.username_login.text = ''
            self.ids.password_login.text = ''
            UsernameErrorPopup().open()

        elif not password:
            self.ids.username_login.text = ''
            self.ids.password_login.text = ''
            PasswordErrorPopup().open()
        else:
            self.ids.username_login.text = ''
            self.ids.password_login.text = ''
            self.manager.userid = str(result)
            firstname, lastname = get_name(self.manager.userid)
            self.manager.get_screen('main').ids.welcome.text = f'Welcome Back ' \
                                                               f'{firstname} ' \
                                                               f'{lastname}! '
            self.manager.current = 'main'


class MainWindow(Screen):
    checks = []
    action = ' '

    def checkbox_click(self, instance, value, topping):
        if value:
            MainWindow.checks.append(topping)
            tops = ''
            for x in MainWindow.checks:
                tops = f'{tops} {x}'
            MainWindow.action = x

        else:
            MainWindow.checks.remove(topping)
            tops = ''
            for x in MainWindow.checks:
                tops = f'{tops} {x}'

    def on_press_button(self):

        if MainWindow.action == 'Create List':
            self.manager.current = "creation"
            pass
        elif MainWindow.action == "Edit List":
            self.manager.current = "selection"
            pass
        elif MainWindow.action == "Stock Prediction":
            pass
        else:
            pass

    def on_logout_button(self):
        self.manager.userid = ''
        self.manager.category = ''
        self.manager.current = 'home'


class CreationWindow(Screen):
    # category = StringProperty('')

    def on_release_button(self):
        self.manager.category = self.ids.category.text
        self.ids.category.text = ''
        self.manager.current = 'product'

    def on_logout_button(self):
        self.manager.userid = ''
        self.manager.category = ''
        self.manager.current = 'home'


class ManualWindow(Screen):
    barcode_data = StringProperty("")

    # category = StringProperty("")

    def on_release_button(self):
        name = self.ids.newName.text
        price = self.ids.newPrice.text
        if self.barcode_data is not None:
            update_database(name, self.barcode_data, price,
                            self.manager.category,
                            self.manager.userid)
            SuccessPopup().open()

    def on_logout_button(self):
        self.manager.userid = ''
        self.manager.category = ''
        self.manager.current = 'home'


class ProductWindow(Screen):
    # category = StringProperty('Test')
    barcode_data = StringProperty('')

    def on_release_button(self):
        # barcode_data = "021200523588"
        self.barcode_data = self.ids.barcode.text
        self.ids.barcode.text = ''
        self.data_retrieval(self.barcode_data)

    def launch_camera(self):
        try:
            self.barcode_data = scan_barcodes()
        except ValueError:
            self.barcode_data = ''
            pass
        if self.barcode_data is not None and self.barcode_data != '':
            self.data_retrieval(self.barcode_data)
        else:
            self.ids.barcode.text = ''  # clear text
            ErrorPopup().open()  # pop up error

    def data_retrieval(self, barcode_data):
        # Check the SQL data first
        exists = checking(barcode_data, self.manager.userid, self.manager.category)
        # If it exists, show it popup window that it already exists
        if exists:
            ExistsPopup().open()
        # If it doesn't exist in SQL check the APIs
        else:
            price, name = get_price(barcode_data)
            # Go to the manual entry
            if name is None or price is None:
                # Pass the barcode and category to the third screen
                # self.manager.pass_info(barcode_data, self.category)
                self.manager.current = 'manualform'  # Go to manual Form
            # It is successful and update the database
            else:
                # Display a successful popup window
                update_database(name, barcode_data, price,
                                self.manager.category,
                                self.manager.userid)
                SuccessPopup().open()

    def on_logout_button(self):
        self.manager.userid = ''
        self.manager.category = ''
        self.manager.current = 'home'


class SelectionWindow(Screen):
    def on_enter(self):
        # First access the desired screen
        selection = self.manager.get_screen('selection')
        selection.add_widget(CustomDropDown())
        # Then access the target drop-down by id.
        drop_down = selection.ids.drop_content
        __safe_id: [drop_down.__self]
        drop_down.clear_widgets()
        # Now iterate over...
        categories = get_unique_categories(self.manager.userid)
        for name in enumerate(categories):
            btn = Button(
                text=name[1],
                size_hint_y=None,
                height=35,
                background_color='white',
                color='black'
            )
            btn.bind(on_release=lambda btn_obj: drop_down.select(btn_obj.text))
            drop_down.add_widget(btn)

    def on_logout_button(self):
        self.manager.userid = ''
        self.manager.category = ''
        self.manager.current = 'home'


class EditWindow(Screen):
    def on_enter(self):
        # First access the desired screen
        selection = self.manager.get_screen('edit')
        # Then access the target drop-down by id.
        drop_down = selection.ids.rv
        drop_down.clear_widgets()
        drop_down.add_widget(RV())

    def on_logout_button(self):
        self.manager.userid = ''
        self.manager.category = ''
        self.manager.current = 'home'


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    selected_row = NumericProperty(0)

    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None

        selected = self.selected_nodes
        if not selected:  # nothing selected, select the first
            self.select_node(nodes[0])
            self.selected_row = 0
            return None, None

        if len(nodes) == 1:  # the only selectable node is selected already
            return None, None

        last = nodes.index(selected[-1])
        self.clear_selection()
        return last, nodes

    def select_next(self):
        ''' Select next row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if last == len(nodes) - 1:
            self.select_node(nodes[0])
            self.selected_row = nodes[0]
        else:
            self.select_node(nodes[last + 1])
            self.selected_row = nodes[last + 1]

    def select_previous(self):
        ''' Select previous row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if not last:
            self.select_node(nodes[-1])
            self.selected_row = nodes[-1]
        else:
            self.select_node(nodes[last - 1])
            self.selected_row = nodes[last - 1]

    def select_current(self):
        ''' Select current row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        self.select_node(nodes[self.selected_row])


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        self.rv_data = rv.data
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class RV(RecycleView):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        Clock.schedule_once(self.after_init)

    def after_init(self, dt):
        root = App.get_running_app().root
        userid = root.userid
        category = root.category
        ads = get_products(userid, category)
        self.data = [{'text': str(ads[x][1]), 'selected': False} for x in range(len(ads))]


class CustomDropDown(DropDown):
    pass


######################## Popup Section  #####################################
class ErrorPopup(Popup):
    pass


class SuccessPopup(Popup):
    pass


class ExistsPopup(Popup):
    pass


class SignUpErrorPopup(Popup):
    pass


class SignUpSuccessPopup(Popup):
    pass


class UsernameErrorPopup(Popup):
    pass


class PasswordErrorPopup(Popup):
    pass


class UsernameBlankErrorPopup(Popup):
    pass


class PasswordBlankErrorPopup(Popup):
    pass


class ForgotPasswordErrorPopup(Popup):
    pass


class ForgotUsernameErrorPopup(Popup):
    pass


class ExistingEmailErrorPopup(Popup):
    pass


class SimplePasswordErrorPopup(Popup):
    pass


class UsernameTakenErrorPopup(Popup):
    pass


class WindowManager(ScreenManager):
    userid = StringProperty('')
    category = StringProperty('')

    def pass_info(self, barcode_data, category):
        self.add_widget(ManualWindow(barcode_data=barcode_data,
                                     category=category))

    def pass_categ(self, category):
        self.add_widget(ProductWindow(category=category))

    def pass_name(self, name):
        self.add_widget(MainWindow(firstname=name))


# Designate Our .kv design file
kv = Builder.load_file('KivyApp.kv')


class MainApp(App):
    title = "Smart Inventory Management App"

    def build(self):
        return kv


if __name__ == '__main__':
    create_database()
    create_user_database()
    app = MainApp()
    app.run()
