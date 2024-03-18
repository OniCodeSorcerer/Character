from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from Character import hero, Enemy, Weapon, Armor, Character, Hero, enemy_select, hero_select  
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

class PopupWindow():
    def show_popup(self, popup_label, popup_titel):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text= popup_label))
        mybutton = Button(text='OK', size_hint_x=None, width=300, pos_hint={'center_x': 0.5})
        box.add_widget(mybutton)
        popup = Popup(title= popup_titel, content=box, size_hint=(None, None), size=(500, 200))
        popup.open()
        mybutton.bind(on_press=popup.dismiss)


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

class Fight(Gui, Screen, PopupWindow):
    def __init__(self, **kwargs):
        super(Fight, self).__init__(**kwargs)

        self.top_left_button.bind(on_release = self.attack)
        self.top_right_button.bind(on_release = self.heal)
        self.down_left_button.bind(on_release = self.switch_screen_start)
        self.down_right_button.bind(on_release = self.magic)

        self.top_left_button.text = 'Attack'
        self.top_right_button.text = 'Heal'
        self.down_left_button.text = 'Run'
        self.down_right_button.text = 'Magic'

        self.enemy = None
        self.update_char()

    def on_enter(self, *args):
        self.update_char()

    def update_char(self):
        self.enemy = enemy_select(1, 1)
        hero = hero_select(1, 1)
        self.enemy_name_label.text = self.enemy.name
        self.enemy_lifebar.max = self.enemy.max_hp
        self.enemy_lifebar.value = self.enemy.hp
        self.char_lifebar.max = hero.max_hp
        self.char_lifebar.value = hero.hp
        self.char_lifebar_label.text = f"{self.char_lifebar.value} / {self.char_lifebar.max}"
        self.enemy_lifebar_label.text = f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}"
        self.char_label.text = self.saved_char_text = f'You are fighting against a {self.enemy.name}!'
        self.enemy_label.text = self.saved_enemy_text = f'The {self.enemy.name} is attacking you!'
        self.char_label.text = self.saved_char_text = f'You are fighting against a {self.enemy.name}!'
        self.enemy_label.text = self.saved_enemy_text = f'The {self.enemy.name} is attacking you!'

        self.top_right_button.disabled = False

    def add_text_char(self, new_text) -> str:
        self.saved_char_text += "\n" + new_text
        self.char_label.text = self.saved_char_text

    def add_text_enemy(self, new_text) -> str:
        self.saved_enemy_text += "\n" + new_text
        self.enemy_label.text = self.saved_enemy_text

    def attack(self, instance):
        hero.attack(self.enemy)
        self.enemy.attack(hero)

        self.add_text_char(f'You attacked {self.enemy.name} for {hero.damage} damage')
        self.add_text_enemy(f'{self.enemy.name} attacked you for {self.enemy.damage} damage')

        if hero.damage == 0:
            self.add_text_char(f'{self.enemy.name} blocked the attack!')

        if self.enemy.hp == 0 and hero.hp > 0:
            hero.experience(self.enemy.exp)
            print(f'{self.enemy.name} has died')
            self.show_popup(f'You have gained {self.enemy.exp} experience.\n {hero.exp} / {hero.max_exp}.', 'You have won!')
            hero.hp = hero.max_hp
            self.switch_screen_start(instance)

        elif hero.hp == 0:
            print(f'{hero.name} has died, game over!')
            self.switch_screen_start(instance)
            hero.hp = hero.max_hp

        else:
            self.char_lifebar.value = hero.hp
            self.enemy_lifebar.value = self.enemy.hp
            self.char_lifebar_label.text = f"{self.char_lifebar.value} / {self.char_lifebar.max}"
            self.enemy_lifebar_label.text = f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}"

    def heal(self, instance):
        hero.healing()
        self.enemy.attack(hero)

        self.add_text_char(f'You healed yourself for {hero.heal} hp')
        self.add_text_enemy(f'{self.enemy.name} attacked you for {self.enemy.damage} damage')
        self.top_right_button.disabled = True

        self.char_lifebar.value = hero.hp
        self.enemy_lifebar.value = self.enemy.hp
        self.char_lifebar_label.text = f"{self.char_lifebar.value} / {self.char_lifebar.max}"
        self.enemy_lifebar_label.text = f"{self.enemy_lifebar.value} / {self.enemy_lifebar.max}"

    def magic(self, instance):
        self.add_text_char('You used magic!')
        self.add_text_enemy(f'{self.enemy.name} attacked you for {self.enemy.damage} damage')

    def switch_screen_start(self, instance):
        if Hero.level_up == 1:
            print('You have leveled up!')

        else:
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'screen1'


class Inventar(Screen):
    def __init__(self, **kwargs):
        super(Inventar, self).__init__(**kwargs)
        self.show_waepon()
        self.show_armor()
        layout = BoxLayout(orientation = "vertical", spacing=5, padding=50)
        top_layout = GridLayout(cols=6, spacing=5, padding=5)
        weapon_left = Button(text="<",width=50, size_hint_x=None, height=50, size_hint_y=None)
        weapon_stats_label = Label(text=f"Weapon: {self.weapon_name} \n Damage: {self.weapon_damage}")
        weapon_right = Button(text=">",width=50, size_hint_x=None, height=50, size_hint_y=None)
        armor_left = Button(text="<",width=50, size_hint_x=None, height=50, size_hint_y=None)
        armor_stats_label = Label(text="Armor Statics")
        armor_right = Button(text=">",width=50, size_hint_x=None, height=50, size_hint_y=None)
        top_layout.add_widget(weapon_left)
        top_layout.add_widget(weapon_stats_label)
        top_layout.add_widget(weapon_right)
        top_layout.add_widget(armor_left)
        top_layout.add_widget(armor_stats_label)
        top_layout.add_widget(armor_right)

        down_layout = GridLayout(cols=2, spacing=5, padding=5)
        equip_weapon_button = Button(text="Equip Weapon",height=60, size_hint_y=None)
        equip_armor_button = Button(text="Equip Armor",height=60, size_hint_y=None)
        back_button = Button(text="Back",height=60, size_hint_y=None, on_press=self.switch_screen_start)
        list_button = Button(text="List",height=60, size_hint_y=None)
        down_layout.add_widget(equip_weapon_button)
        down_layout.add_widget(equip_armor_button)
        down_layout.add_widget(back_button)
        down_layout.add_widget(list_button)
        
        layout.add_widget(top_layout)
        layout.add_widget(down_layout)
        self.add_widget(layout)

    def show_waepon(self):
        weapon_id = 1
        conn = sqlite3.connect('Charakter Database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Characterweapons WHERE oid = ' + str(weapon_id))
        weapon = c.fetchone()
        for i in weapon:
            self.weapon_name = weapon[0]
            self.weapon_damage = weapon[1]
        
        conn.commit()
        conn.close()

    def show_armor(self):
        armor_id = 1
        conn = sqlite3.connect('Charakter Database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Characterarmores WHERE oid = ' + str(armor_id))
        armor = c.fetchone()
        for i in armor:
            self.armor_name = armor[0]
            self.armor_defense = armor[1]
        
        conn.commit()
        conn.close()

    def switch_screen_start(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'screen1'

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