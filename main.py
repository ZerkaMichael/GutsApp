from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from classes.score_counter_window import ScoreCounterWindow
from classes.admin_window import AdminWindow
from classes.tournament_window import TournamentWindow
from classes.match_history_window import MatchHistoryWindow

Factory.register('ScoreCounterWindow', cls=ScoreCounterWindow)
Factory.register('AdminWindow', cls=AdminWindow)
Factory.register('TournamentWindow', cls=TournamentWindow)
Factory.register('MatchHistoryWindow', cls=MatchHistoryWindow)


class HomeWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        kv = Builder.load_file('screens.kv')
        return kv


if __name__ == '__main__':
    MyApp().run()
