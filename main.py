from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from plyer import notification


class Interface(MDBoxLayout):
    milli_seconds = 0
    seconds = 0
    minutes = 0
    timer_running = False
    def timer(self, *args):
        Interface.milli_seconds += 10
        if Interface.milli_seconds == 100:
            Interface.milli_seconds = 0
            Interface.seconds += 1
            if Interface.seconds == 60:
                Interface.minutes += 1
                Interface.seconds = 0
        self.ids.timer_placeholder.text = f"{'{0:0=2d}'.format(Interface.minutes)} : {'{0:0=2d}'.format(Interface.seconds)} : {'{0:0=2d}'.format(Interface.milli_seconds)}"

    def start_timer(self):
        if not Interface.timer_running:
            Clock.schedule_interval(self.timer, 1/10)
            Interface.timer_running = True
            self.ids.progressbar.start()
            self.ids.icon_placeholder.icon = "timer-pause-outline"
        else:
            Clock.unschedule(self.timer)
            Interface.timer_running = False
            self.ids.progressbar.stop()
            Interface.milli_seconds = 0
            Interface.seconds = 0
            Interface.minutes = 0
            self.ids.icon_placeholder.icon = "timer-play-outline"
            notification.notify(title="Timer Duration", message=str(self.ids.timer_placeholder.text))

class CustomButton(ButtonBehavior, CommonElevationBehavior, MDAnchorLayout):
    pass

class TimerApp(MDApp):
    def change_theme(self, app_bar):
        if self.theme_cls.theme_style == 'Light':
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_palette = 'Teal'
            self.theme_cls.accent_hue = "50"
            app_bar.right_action_items=[["weather-sunny", lambda x: self.change_theme(app_bar)]]
        else:
            self.theme_cls.primary_palette = 'Purple'
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.accent_hue = "900"
            app_bar.right_action_items = [["weather-night", lambda x: self.change_theme(app_bar)]]

    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        self.theme_cls.accent_palette = "Gray"
        self.theme_cls.accent_hue = "900"
        self.theme_cls.theme_style = 'Light'

TimerApp().run()