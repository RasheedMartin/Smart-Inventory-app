
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget

# Designate Our .kv design file
Builder.load_file('KivyApp.kv')


class MainWidget(Widget):
    checks = []
    action = ' '

    def checkbox_click(self, instance, value, topping):
        if value:
            MainWidget.checks.append(topping)
            tops = ''
            for x in MainWidget.checks:
                tops = f'{tops} {x}'
            MainWidget.action = x

        else:
            MainWidget.checks.remove(topping)
            tops = ''
            for x in MainWidget.checks:
                tops = f'{tops} {x}'

    def on_press_button(self):
        if MainWidget.action == 'Create List':
            pass
        elif MainWidget.action == "Edit List":
            pass
        elif MainWidget.action == "Stock Prediction":
            pass
        else:
            pass


class MainApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    app = MainApp()
    app.run()
