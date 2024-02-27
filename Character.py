import random
import sqlite3
import math

class Character():
    def __init__(self, name, hp, damage, defense, luck, weapon, armor):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.luck = luck
        self.weapon = weapon
        self.armor = armor

    def attack(self, target):
        damage_random = random.choices([0.8, 1, 2], weights=[0.6, 0.03 * self.luck, 0.01 * self.luck], k=1)[0]
        defense_random = random.choices([0.8, 1, 2], weights=[0.6, 0.03 * target.luck, 0.01 * target.luck], k=1)[0]
        if defense_random == 2 and self.armor is not None:
            print(f'{target.name} blocked the attack!')
            return
        damage = self.damage * damage_random - target.defense + self.weapon.damage
        damage = math.ceil(damage)
        target.hp -= damage
        target.hp = max(0, target.hp)
        print(f'{self.name} attacked {target.name} for {damage} damage')
        print(f'{target.name} has {target.hp} hp left')
        if damage_random == 2:
            print('Critical Hit!')

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

class Hero(Character):
    def __init__(self, name, hp, damage, defense, luck, weapon, armor, level, exp):
        super().__init__(name, hp, damage, defense, luck, weapon, armor)
        self.level = level
        self.exp = exp

    def experience(self, exp):        
        print(f'become {enemy.exp} exp')
        hero.exp += exp
        print(f'{self.name} has {hero.exp} exp')

        if hero.exp >= 100:
            hero.exp -= 100
            self.level_up(hero.level)

        conn = sqlite3.connect("Charakter Database.db")
        c = conn.cursor()

        c.execute("UPDATE Attributes SET exp = " + str(hero.exp) + " WHERE name = '" + hero.name + "'")

        conn.commit()
        conn.close()


    def level_up(self, level):
        self.hp += 10
        self.damage += 2
        self.defense += 1
        self.luck += 1
        print(f'{self.name} has leveled up, {self.name} is now level {self.level + 1}!')

conn = sqlite3.connect("Charakter Database.db")
c = conn.cursor()
c.execute("SELECT * FROM Attributes")
records = c.fetchall()

for record in records:
    name = record[0]
    hp = record[1]
    damage = record[2]
    defense = record[3]
    luck = record[4]
    exp = record[5]    
    level = record[6]

c.execute("SELECT * FROM Characterweapons WHERE equiped = 1")
weapons = c.fetchall()

for weapon in weapons:
    weapon_name = weapon[0]
    weapon_damage = weapon[1]

equipt_weapon = Weapon(weapon_name, weapon_damage)

c.execute("SELECT * FROM Characterarmores WHERE equiped = 1")
armors = c.fetchall()

for armor in armors:
    armor_name = armor[0]
    armor_defense = armor[1]

equipt_armor = Armor(armor_name, armor_defense)

conn.commit()
conn.close()

hero = Hero(name, hp, damage, defense, luck, equipt_weapon, equipt_armor, level, exp)
        


class Enemy(Character):
    def __init__(self, name, hp, damage, defense, luck, weapon, armor, exp):
        super().__init__(name, hp, damage, defense, luck, weapon, armor)
        self.exp = exp


sword = Weapon('Sword', 10)
shield = Armor('Shield', 5)
bite = Weapon('Bite', 5)
fell = Armor('Fell', 2)
panzer = Armor('Panzer', 2)


conn = sqlite3.connect("Enemys Database.db")

c = conn.cursor()
c.execute("SELECT COUNT(*) FROM Enemys")
rows = c.fetchall()[0]
enemys_select = random.randint(1, rows[0])

c.execute("SELECT *, oid FROM Enemys WHERE oid = " + str(enemys_select))
records = c.fetchall()


for record in records:
    name = record[0]
    hp = record[1]
    damage = record[2]
    defense = record[3]
    luck = record[4]
    weapon = record[5]
    armor = record[6]
    exp = record[7]

c.execute("SELECT * FROM Weapons WHERE name = '" + weapon + "'")
weapons = c.fetchall()

for weapon in weapons:
    weapon_name = weapon[0]
    weapon_damage = weapon[1]
    
equipt_weapon = Weapon(weapon_name, weapon_damage)

c.execute("SELECT * FROM Armor WHERE name = '" + armor + "'")
armors = c.fetchall()

for armor in armors:
    armor_name = armor[0]
    armor_defense = armor[1]




equipt_armor = Armor(armor_name, armor_defense)
enemy = Enemy(name, hp, damage, defense, luck, equipt_weapon, equipt_armor, exp)

conn.commit()

conn.close()


while enemy.hp > 0:
    hero.attack(enemy)
    enemy.attack(hero)

    if enemy.hp == 0:
        hero.experience(enemy.exp)
        print(f'{enemy.name} has died')
        break

    elif hero.hp == 0:
        print(f'{hero.name} has died, game over!')
        break



        
