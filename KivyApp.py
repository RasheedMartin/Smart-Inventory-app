from barcode_reader import scan_barcodes, get_price, create_database, update_database

try:
    from kivy.app import App
except ImportError:
    import pip._internal as pip

    pip.main(['install', 'kivy'])
    from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty


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
            pass
        elif MainWindow.action == "Stock Prediction":
            pass
        else:
            pass


class CreationWindow(Screen):

    def on_release_button(self):
        category = self.ids.newlist.text
        # barcode_data = scan_barcodes()
        barcode_data = "021200523588"
        # Check the SQL data first
        # If it exists, show it popup window that it already exists
        # If it doesn't exist in SQL check the APIs
        name, price = get_price(barcode_data)
        # Go to the manual entry
        if name or price is None:
            # Pass the barcode and category to the third screen
            self.pass_info(barcode_data, category)
            self.manager.current = 'manualform'  # Go to manual Form
        # It is successful and update the database
        else:
            # Display a successful popup window
            update_database(name, barcode_data, price, category)


class ManualWindow(Screen):
    barcode_data = StringProperty("")
    category = StringProperty("")

    def on_release_button(self):
        name = self.ids.newName.text
        price = self.ids.newPrice.text
        update_database(name, self.barcode_data, price, self.category)


class WindowManager(ScreenManager):
    def pass_info(self, barcode_data, category):
        self.add_widget(ManualWindow(barcode_data=barcode_data, category=category))


# Designate Our .kv design file
kv = Builder.load_file('KivyApp.kv')


class MainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    create_database()
    app = MainApp()
    app.run()
