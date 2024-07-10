class Item:
    def __init__(self, name, type, effect):
        self.name = name
        self.type = type
        self.effect = effect

    def use(self, target):
        print(f"Using {self.name} on {target.name}!")
        self.effect(target)


class Move:
    def __init__(self, name, type, power, accuracy, category, effect=None):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.category = category
        self.effect = effect

    def apply_effect(self, target):
        if self.effect:
            print(f"{self.name} had an additional effect on {target.name}!")
            self.effect(target)


import random

class Pokemon:
    def __init__(self, name, type, health, attack, defense, special_attack, special_defense, speed, level, experience, moves, is_wild):
        self.name = name
        self.type = type
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.level = level
        self.experience = experience
        self.moves = moves
        self.is_wild = is_wild

    def attack_opponent(self, move, opponent):
        print(f"{self.name} used {move.name}!")
        if random.random() <= move.accuracy:
            damage = self.calculate_damage(move, opponent)
            opponent.take_damage(damage)
            move.apply_effect(opponent)
        else:
            print(f"{self.name}'s attack missed!")

    def calculate_damage(self, move, opponent):
        if move.category == 'physical':
            damage = ((2 * self.level / 5 + 2) * move.power * self.attack / opponent.defense) / 50 + 2
        else:
            damage = ((2 * self.level / 5 + 2) * move.power * self.special_attack / opponent.special_defense) / 50 + 2

        return int(damage)

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
        print(f"{self.name} took {damage} damage! Current health: {self.current_health}")

    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level ** 3:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.attack += 2
        self.defense += 2
        self.special_attack += 2
        self.special_defense += 2
        self.speed += 2
        self.current_health = self.max_health
        print(f"{self.name} leveled up to level {self.level}!")

    def learn_move(self, move):
        if len(self.moves) < 4:
            self.moves.append(move)
        else:
            print(f"{self.name} can't learn more than 4 moves!")

    def get_stat(self, stat):
        return getattr(self, stat)
    

from random import choice

class Trainer:
    def __init__(self, name, team, inventory):
        self.name = name
        self.team = team
        self.inventory = inventory

    def catch_pokemon(self, wild_pokemon):
        if wild_pokemon.is_wild and len(self.team) < 6:
            self.team.append(wild_pokemon)
            wild_pokemon.is_wild = False
            print(f"{self.name} caught {wild_pokemon.name}!")
        else:
            print("Can't catch this Pokémon!")

    def use_item(self, item, target):
        item.use(target)

    def battle(self, opponent):
        print(f"{self.name} is battling {opponent.name}!")
        my_pokemon = self.team[0]
        opponent_pokemon = opponent.team[0]

        while my_pokemon.current_health > 0 and opponent_pokemon.current_health > 0:
            print(f"\n{my_pokemon.name} (HP: {my_pokemon.current_health}) vs {opponent_pokemon.name} (HP: {opponent_pokemon.current_health})")

            move = self.choose_move(my_pokemon)
            my_pokemon.attack_opponent(move, opponent_pokemon)

            if opponent_pokemon.current_health > 0:
                move = choice(opponent_pokemon.moves)
                opponent_pokemon.attack_opponent(move, my_pokemon)

        if my_pokemon.current_health > 0:
            print(f"{my_pokemon.name} won the battle!")
            self.gain_experience(100)
        else:
            print(f"{my_pokemon.name} fainted!")

    def choose_move(self, pokemon):
        print(f"Choose a move for {pokemon.name}:")
        for idx, move in enumerate(pokemon.moves):
            print(f"{idx + 1}. {move.name} ({move.type} type, {move.power} power, {move.accuracy * 100}% accuracy)")
        choice = int(input("Enter the number of the move you want to use: ")) - 1
        return pokemon.moves[choice]

    def gain_experience(self, exp):
        for pokemon in self.team:
            pokemon.gain_experience(exp)

# Defining moves
thunderbolt = Move("Thunderbolt", "Electric", 90, 1.0, "special")
tackle = Move("Tackle", "Normal", 40, 1.0, "physical")

# Defining characters
pikachu = Pokemon("Pikachu", "Electric", 100, 55, 40, 50, 50, 90, 5, 0, [thunderbolt, tackle], False)
bulbasaur = Pokemon("Bulbasaur", "Grass", 100, 49, 49, 65, 65, 45, 5, 0, [tackle], True)
ash = Trainer("Ash", [pikachu], [])

# Catching random pokemon //if any 
ash.catch_pokemon(bulbasaur)
# Fighting
misty = Trainer("Misty", [bulbasaur], [])
ash.battle(misty)