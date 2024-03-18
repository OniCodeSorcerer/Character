import random
import sqlite3
import math


class Character():
    def __init__(self, name, max_hp, damage, defense, luck, weapon, armor):
        self.name = name
        self.max_hp = max_hp
        self.static_damage = damage
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
        
        self.damage = self.static_damage * damage_random - target.defense + self.weapon.damage
        self.damage = math.ceil(self.damage)
        self.damage = max(1, self.damage)
        target.hp -= self.damage
        target.hp = max(0, target.hp)
        print(f'{self.name} attacked {target.name} for {self.damage} damage')
        if damage_random == 2:
            print('Critical Hit!')
        print(f'{target.name} has {target.hp} hp left')

    def healing(self):
        healing = random.choices([0.2, 0.3, 0.5], weights=[0.6, 0.03 * self.luck, 0.01 * self.luck], k=1)[0]
        self.heal = self.max_hp * healing
        self.hp += self.heal
        self.hp = min(self.max_hp, self.hp)
        print(f'{self.name} has healed for {self.heal} hp')
        print(f'{self.name} has {self.hp} hp')

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

class Hero(Character):
    def __init__(self, name, max_hp, damage, defense, luck, weapon, armor, level, exp):
        super().__init__(name, max_hp, damage, defense, luck, weapon, armor)
        self.hp = max_hp
        self.level = level
        self.exp = exp
        self.exp = max(0, self.exp)
        self.heal = 0
        self.max_exp = level * 100 + level / 0.05

    def experience(self, exp):
        hero.exp += exp
        print(f'{self.name} has {hero.exp} exp from {self.max_exp} exp !')
        if hero.exp >= self.max_exp:
            self.level_up()

        conn = sqlite3.connect("Charakter Database.db")
        c = conn.cursor()
        c.execute("UPDATE Attributes SET exp = " + str(hero.exp) + " WHERE name = '" + hero.name + "'")
        conn.commit()
        conn.close()


    def level_up(self):
        hero.static_damage += 2
        hero.defense += 1
        hero.luck += 1
        hero.level += 1
        hero.max_hp = hero.level * 10 + 100
        print(f'{hero.name} has leveled up, {hero.name} is now level {hero.level}!')
        conn = sqlite3.connect("Charakter Database.db")
        c = conn.cursor()

        # Zurücksetzen des Levels
        #c.execute("UPDATE Attributes SET damage = " + str(10) + " WHERE name = '" + hero.name + "'")
        # c.execute("UPDATE Attributes SET defense = " + str(5) + " WHERE name = '" + hero.name + "'")
        # c.execute("UPDATE Attributes SET luck = " + str(5) + " WHERE name = '" + hero.name + "'")
        # c.execute("UPDATE Attributes SET lvl = " + str(1) + " WHERE name = '" + hero.name + "'")
        # c.execute("UPDATE Attributes SET exp = " + str(0) + " WHERE name = '" + hero.name + "'")
        # c.execute("UPDATE Attributes SET hp = " + str(100) + " WHERE name = '" + hero.name + "'")

        c.execute("UPDATE Attributes SET damage = " + str(hero.static_damage) + " WHERE name = '" + hero.name + "'")
        c.execute("UPDATE Attributes SET defense = " + str(hero.defense) + " WHERE name = '" + hero.name + "'")
        c.execute("UPDATE Attributes SET luck = " + str(hero.luck) + " WHERE name = '" + hero.name + "'")
        c.execute("UPDATE Attributes SET lvl = " + str(hero.level) + " WHERE name = '" + hero.name + "'")
        c.execute("UPDATE Attributes SET hp = " + str(hero.max_hp) + " WHERE name = '" + hero.name + "'")
        conn.commit()
        conn.close()

        return 1

def hero_select(self, hero_select):
    conn = sqlite3.connect("Charakter Database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM Attributes")
    records = c.fetchall()
    for record in records:
        name = record[0]
        max_hp = record[1]
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
    return Hero(name, max_hp, damage, defense, luck, equipt_weapon, equipt_armor, level, exp)

hero = hero_select(1,1)


class Enemy(Character):
    def __init__(self, name, max_hp, damage, defense, luck, weapon, armor, exp):
        super().__init__(name, max_hp, damage, defense, luck, weapon, armor)
        self.hp = max_hp
        self.exp = exp

def enemy_select(self, enemys_select):
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
    
    conn.commit()
    conn.close()

    return Enemy(name, hp, damage, defense, luck, equipt_weapon, equipt_armor, exp)


    



