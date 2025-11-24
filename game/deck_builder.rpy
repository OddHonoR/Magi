## Deck Builder System
## This file contains the core deck building mechanics

init python:
    import random
    
    class Card:
        """Base class for cards in the deck builder"""
        def __init__(self, name, description, card_type, cost=0, power=0, effect=None):
            self.name = name
            self.description = description
            self.card_type = card_type  # "attack", "defense", "skill", "power"
            self.cost = cost  # Energy cost to play
            self.power = power  # Damage or block value
            self.effect = effect  # Special effect function
            
        def play(self, player, enemy):
            """Execute the card's effect"""
            if self.card_type == "attack":
                return {"damage": self.power}
            elif self.card_type == "defense":
                return {"block": self.power}
            elif self.card_type == "skill":
                if self.effect:
                    return self.effect(player, enemy)
                return {}
            return {}
            
        def __str__(self):
            return f"{self.name} ({self.card_type})"
    
    
    class Deck:
        """Manages a collection of cards"""
        def __init__(self):
            self.cards = []
            self.draw_pile = []
            self.discard_pile = []
            self.hand = []
            
        def add_card(self, card):
            """Add a card to the deck"""
            self.cards.append(card)
            
        def remove_card(self, card):
            """Remove a card from the deck"""
            if card in self.cards:
                self.cards.remove(card)
                
        def shuffle(self):
            """Shuffle the draw pile"""
            random.shuffle(self.draw_pile)
            
        def prepare_for_combat(self):
            """Set up the deck for a new combat"""
            self.draw_pile = self.cards.copy()
            self.discard_pile = []
            self.hand = []
            self.shuffle()
            
        def draw_card(self, num=1):
            """Draw cards from the draw pile to hand"""
            drawn = []
            for _ in range(num):
                if not self.draw_pile:
                    # If draw pile is empty, shuffle discard pile into draw pile
                    if self.discard_pile:
                        self.draw_pile = self.discard_pile.copy()
                        self.discard_pile = []
                        self.shuffle()
                    else:
                        break  # No cards left to draw
                        
                if self.draw_pile:
                    card = self.draw_pile.pop(0)
                    self.hand.append(card)
                    drawn.append(card)
            return drawn
            
        def discard_hand(self):
            """Discard all cards in hand"""
            self.discard_pile.extend(self.hand)
            self.hand = []
            
        def discard_card(self, card):
            """Discard a specific card from hand"""
            if card in self.hand:
                self.hand.remove(card)
                self.discard_pile.append(card)
                
        def get_deck_size(self):
            """Get total number of cards in deck"""
            return len(self.cards)
    
    
    class Player:
        """Represents the player character"""
        def __init__(self, name="Player", max_hp=80, max_energy=3):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.max_energy = max_energy
            self.energy = max_energy
            self.block = 0
            self.deck = Deck()
            self.gold = 100
            
        def take_damage(self, amount):
            """Take damage, reduced by block"""
            if self.block >= amount:
                self.block -= amount
                return 0
            else:
                damage_taken = amount - self.block
                self.block = 0
                self.hp -= damage_taken
                if self.hp < 0:
                    self.hp = 0
                return damage_taken
                
        def gain_block(self, amount):
            """Gain block (defense)"""
            self.block += amount
            
        def heal(self, amount):
            """Heal HP"""
            self.hp += amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                
        def reset_energy(self):
            """Reset energy to maximum"""
            self.energy = self.max_energy
            
        def spend_energy(self, amount):
            """Spend energy, returns True if successful"""
            if self.energy >= amount:
                self.energy -= amount
                return True
            return False
            
        def start_turn(self):
            """Reset for a new turn"""
            self.block = 0
            self.reset_energy()
    
    
    class Enemy:
        """Represents an enemy"""
        def __init__(self, name, hp, attack_power):
            self.name = name
            self.max_hp = hp
            self.hp = hp
            self.attack_power = attack_power
            self.block = 0
            self.intent = "attack"  # What the enemy plans to do
            
        def take_damage(self, amount):
            """Take damage, reduced by block"""
            if self.block >= amount:
                self.block -= amount
                return 0
            else:
                damage_taken = amount - self.block
                self.block = 0
                self.hp -= damage_taken
                if self.hp < 0:
                    self.hp = 0
                return damage_taken
                
        def gain_block(self, amount):
            """Gain block (defense)"""
            self.block += amount
            
        def execute_intent(self, player):
            """Execute the enemy's planned action"""
            if self.intent == "attack":
                player.take_damage(self.attack_power)
            self.block = 0  # Enemy block resets each turn
    
    
    def create_starter_deck():
        """Create the starting deck"""
        deck = Deck()
        
        # Add 5 Strike cards
        for _ in range(5):
            deck.add_card(Card("Strike", "Deal 6 damage.", "attack", cost=1, power=6))
        
        # Add 5 Defend cards
        for _ in range(5):
            deck.add_card(Card("Defend", "Gain 5 block.", "defense", cost=1, power=5))
        
        return deck


# Initialize game state
default player = None
default current_enemy = None
default combat_active = False
default turn_number = 0
