from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from Character import hero, Enemy, Weapon, Armor, enemy, Character, Hero
import sqlite3
import random

class Gui(Screen):
    def __init__(self, **kwargs):
        super(Gui, self).__init__(**kwargs)
        layout = GridLayout(cols= 2, spacing=5, padding= 50)
        self.add_widget(layout)

        self.char_name_label = Label(text=f'{hero.name}                                                   Level {hero.level}', size_hint_y=None, height=60)
        layout.add_widget(self.char_name_label)

        self.enemy_name_label = Label(text="", size_hint_y=None, height=60)
        layout.add_widget(self.enemy_name_label)

        self.char_label = Label(text='')
        layout.add_widget(self.char_label)

        self.enemy_label = Label(text="")
        layout.add_widget(self.enemy_label)

        self.char_lifebar = ProgressBar(max=hero.max_hp, size_hint_y=None, height=60)
        self.char_lifebar.value = hero.hp
        
        self.enemy_lifebar = ProgressBar(max=0, size_hint_y=None, height=60)
        self.enemy_lifebar.value = 0
        
        self.char_lifebar_label = Label(text=f"{self.char_lifebar.value} / {self.char_lifebar.max}", size_hint_y=None, height=10)
        layout.add_widget(self.char_lifebar_label)

        self.enemy_lifebar_label = Label(text=f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}", size_hint_y=None, height=10)
        layout.add_widget(self.enemy_lifebar_label)

        layout.add_widget(self.char_lifebar)
        layout.add_widget(self.enemy_lifebar)

        self.top_left_button = Button(text='Kämpfen', size_hint_y=None, height=60)
        layout.add_widget(self.top_left_button)

        self.top_right_button = Button(text='Inventar', height=60, size_hint_y=None)
        layout.add_widget(self.top_right_button)

        self.down_left_button = Button(text='Stadt besuchen', size_hint_y=None, height=60)
        layout.add_widget(self.down_left_button)

        self.down_right_button = Button(text='Attribute', height=60, size_hint_y=None)
        layout.add_widget(self.down_right_button)


class StartScreen(Gui, Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.top_left_button.bind(on_release=self.switch_screen_fight)
        self.top_right_button.bind(on_release=self.switch_screen_inventar)
        self.down_left_button.bind(on_release=self.switch_screen_city)
        self.down_right_button.bind(on_release=self.switch_screen_attribute)

    def switch_screen_fight(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'screen2'

    def switch_screen_inventar(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'screen3'

    def switch_screen_city(self, instance):
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'screen4'

    def switch_screen_attribute(self, instance):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'screen5'

class Fight(Gui, Screen):
    def __init__(self, **kwargs):
        super(Fight, self).__init__(**kwargs)

        self.top_left_button.text = 'Attack'
        self.top_right_button.text = 'Heal'
        self.char_label.text = self.saved_char_text = f'You are fighting against a {enemy.name}!'
        self.enemy_label.text = self.saved_enemy_text = f'The {enemy.name} is attacking you!'


        self.top_left_button.bind(on_release=self.attack)
        self.top_right_button.bind(on_release=self.heal)

        self.enemy_name_label.text = enemy.name
        self.enemy_lifebar.max = enemy.max_hp
        self.enemy_lifebar.value = enemy.hp
        self.enemy_lifebar_label.text = f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}"

    def add_text_char(self, new_text) -> str:
        self.saved_char_text += "\n" + new_text
        self.char_label.text = self.saved_char_text

    def add_text_enemy(self, new_text) -> str:
        self.saved_enemy_text += "\n" + new_text
        self.enemy_label.text = self.saved_enemy_text

    def attack(self, instance):
        hero.attack(enemy)
        enemy.attack(hero)

        self.add_text_char(f'You attacked {enemy.name} for {hero.damage} damage')
        self.add_text_enemy(f'{enemy.name} attacked you for {enemy.damage} damage')

        if hero.damage == 0:
            self.add_text_char(f'{enemy.name} blocked the attack!')

        if enemy.hp == 0:
            hero.experience(enemy.exp)
            print(f'{enemy.name} has died')
            self.switch_screen_start(instance)


        elif hero.hp == 0:
            print(f'{hero.name} has died, game over!')
            self.switch_screen_start(instance)

        else:
            self.char_lifebar.value = hero.hp
            self.enemy_lifebar.value = enemy.hp
            self.char_lifebar_label.text = f"{self.char_lifebar.value} / {self.char_lifebar.max}"
            self.enemy_lifebar_label.text = f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}"

    def heal(self, instance):
        hero.heal()
        enemy.attack(hero)

        self.add_text_char(f'You healed yourself for {hero.heal} hp')
        self.add_text_enemy(f'{enemy.name} attacked you for {enemy.damage} damage')

        self.char_lifebar.value = hero.hp
        self.enemy_lifebar.value = enemy.hp
        self.char_lifebar_label.text = f"{self.char_lifebar.value} / {self.char_lifebar.max}"
        self.enemy_lifebar_label.text = f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}"

    def switch_screen_start(self, instance):
        if Hero.level_up == 1:
            print('You have leveled up!')

        else:
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'screen1'


class Inventar(Screen):
    pass

class City(Screen):
    pass

class Attributes(Screen):
    pass

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(StartScreen(name='screen1'))
        screen_manager.add_widget(Fight(name='screen2'))
        screen_manager.add_widget(Inventar(name='screen3'))
        screen_manager.add_widget(City(name='screen4'))
        screen_manager.add_widget(Attributes(name='screen5'))

        return screen_manager

if __name__ == '__main__':
    MyApp().run()