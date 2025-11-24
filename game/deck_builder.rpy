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
    
    
    # ===== PILGRIMAGE JOURNEY GAME SYSTEM =====
    
    class JourneyCard:
        """Cards for the pilgrimage journey game"""
        def __init__(self, name, description, card_type, effect=None, power=0):
            self.name = name
            self.description = description
            self.card_type = card_type  # "action", "condition", "relic"
            self.effect = effect  # Function to execute when played
            self.power = power  # Effectiveness value
            self.is_permanent = (card_type == "relic")  # Relics stay unless destroyed
            
        def play(self, pilgrim, event_context):
            """Execute the card's effect during an event"""
            if self.effect:
                return self.effect(pilgrim, event_context)
            return {}
            
        def __str__(self):
            return f"{self.name} ({self.card_type})"
    
    
    class Pilgrim:
        """The player character on their pilgrimage to Magi"""
        def __init__(self, name="Pilgrim", background=None):
            self.name = name
            self.background = background
            
            # Core stats
            self.sustenance = 100  # Food and water (0-100)
            self.health = 100  # Physical wellbeing (0-100)
            self.spirit = 100  # Faith and resolve (0-100)
            self.packweight_current = 0  # Current carried weight
            self.packweight_max = 20  # Maximum carry capacity
            self.progress = 0  # Distance traveled (0-1000)
            self.progress_goal = 1000  # Distance to reach Magi
            
            # Additional attributes
            self.corruption = 0  # Accumulates from dark choices
            self.companions = []  # Fellow pilgrims traveling with you
            self.relics = []  # Permanent powerful items
            self.blessings = []  # Active divine blessings
            
            # Journey state
            self.current_province = None
            self.current_season = None
            self.days_traveled = 0
            self.deck = JourneyDeck()
            
        def drain_daily(self):
            """Daily resource drain based on travel"""
            # Base daily drain
            sustenance_drain = 5
            
            # Season modifiers
            if self.current_season == "winter":
                sustenance_drain += 2
            elif self.current_season == "summer":
                sustenance_drain += 3
                
            # Apply drain
            self.sustenance = max(0, self.sustenance - sustenance_drain)
            
            # Low sustenance affects health
            if self.sustenance < 20:
                self.health = max(0, self.health - 3)
            
            # Low health affects spirit
            if self.health < 30:
                self.spirit = max(0, self.spirit - 2)
                
        def get_hand_size(self):
            """Hand size depends on Spirit"""
            if self.spirit >= 80:
                return 5
            elif self.spirit >= 60:
                return 4
            elif self.spirit >= 40:
                return 3
            elif self.spirit >= 20:
                return 2
            else:
                return 1
                
        def add_condition(self, condition_card):
            """Add a condition card that clogs the deck"""
            self.deck.add_card(condition_card)
            
        def add_relic(self, relic_card):
            """Add a relic to inventory"""
            if self.packweight_current + relic_card.power <= self.packweight_max:
                self.relics.append(relic_card)
                self.packweight_current += relic_card.power
                return True
            return False  # Too heavy
            
        def is_alive(self):
            """Check if pilgrim can continue"""
            return self.health > 0 and self.spirit > 0
            
        def has_reached_magi(self):
            """Check if pilgrim has reached the destination"""
            return self.progress >= self.progress_goal
    
    
    class JourneyDeck:
        """Manages cards for the pilgrimage journey"""
        def __init__(self):
            self.cards = []
            self.draw_pile = []
            self.discard_pile = []
            self.hand = []
            self.permanent_relics = []  # Relics that stay out of deck
            
        def add_card(self, card):
            """Add a card to the deck"""
            if card.is_permanent:
                self.permanent_relics.append(card)
            else:
                self.cards.append(card)
                
        def remove_card(self, card):
            """Remove a card from the deck"""
            if card in self.cards:
                self.cards.remove(card)
            if card in self.permanent_relics:
                self.permanent_relics.remove(card)
                
        def shuffle(self):
            """Shuffle the draw pile"""
            random.shuffle(self.draw_pile)
            
        def prepare_for_node(self):
            """Set up the deck for a new node encounter"""
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
    
    
    class Province:
        """Represents a region with specific terrain and difficulty"""
        def __init__(self, name, terrain_type, difficulty, travel_speed):
            self.name = name
            self.terrain_type = terrain_type
            self.difficulty = difficulty  # 1-5 scale
            self.travel_speed = travel_speed  # Base progress per day
            self.encounter_types = []
            
        def get_modified_speed(self, season):
            """Get travel speed modified by season"""
            speed = self.travel_speed
            if season == "winter":
                speed *= 0.7
            elif season == "summer":
                if self.terrain_type == "salt_plains":
                    speed *= 0.8  # Heat exhaustion
                else:
                    speed *= 1.1
            elif season == "spring":
                speed *= 1.0
            elif season == "autumn":
                speed *= 0.9
            return speed
    
    
    class Node:
        """A stop on the journey"""
        def __init__(self, node_type, event_pool):
            self.node_type = node_type  # camp, crossroads, shrine, settlement, wilderness, ruins
            self.event_pool = event_pool
            self.visited = False
            
        def get_event(self):
            """Randomly select an event from the pool"""
            if self.event_pool:
                return random.choice(self.event_pool)
            return None
    
    
    class Encounter:
        """An encounter at a node"""
        def __init__(self, name, description, choices):
            self.name = name
            self.description = description
            self.choices = choices  # List of (choice_text, outcome_function) tuples
    
    
    # Province definitions
    PROVINCES = {
        "salt_plains": Province("Salt Plains", "salt_plains", 2, 15),
        "fallen_forests": Province("Fallen Forests", "fallen_forests", 3, 8),
        "clay_wastes": Province("Clay Wastes", "clay_wastes", 4, 10),
        "high_road": Province("High Pilgrim Road", "high_road", 1, 12),
        "storm_frontier": Province("Storm Frontier", "storm_frontier", 5, 13)
    }
    
    # Pilgrim backgrounds
    BACKGROUNDS = {
        "merchant": {"name": "Merchant", "sustenance": 120, "packweight": 25},
        "warrior": {"name": "Warrior", "health": 120, "spirit": 90},
        "priest": {"name": "Priest", "spirit": 120, "health": 90},
        "scholar": {"name": "Scholar", "spirit": 110, "packweight": 15}
    }
    
    # Starting blessings
    BLESSINGS = {
        "travelers_grace": {"name": "Traveler's Grace", "effect": "travel_speed_bonus"},
        "iron_constitution": {"name": "Iron Constitution", "effect": "health_drain_reduction"},
        "divine_protection": {"name": "Divine Protection", "effect": "spirit_loss_reduction"},
        "light_burden": {"name": "Light Burden", "effect": "packweight_bonus"}
    }
    
    
    def create_starter_journey_deck(deck_type="balanced"):
        """Create starting deck for pilgrimage"""
        deck = JourneyDeck()
        
        # Action cards - tools for survival
        if deck_type == "hunter":
            deck.add_card(JourneyCard("Hunt", "Search for food in the wilderness", "action", power=15))
            deck.add_card(JourneyCard("Hunt", "Search for food in the wilderness", "action", power=15))
            deck.add_card(JourneyCard("Navigate", "Find the best path forward", "action", power=10))
            deck.add_card(JourneyCard("Rest", "Recover health and spirit", "action", power=8))
        elif deck_type == "trader":
            deck.add_card(JourneyCard("Bargain", "Trade goods and negotiate", "action", power=12))
            deck.add_card(JourneyCard("Bargain", "Trade goods and negotiate", "action", power=12))
            deck.add_card(JourneyCard("Navigate", "Find the best path forward", "action", power=10))
            deck.add_card(JourneyCard("Rest", "Recover health and spirit", "action", power=8))
        elif deck_type == "faithful":
            deck.add_card(JourneyCard("Pray", "Resist corruption and restore spirit", "action", power=12))
            deck.add_card(JourneyCard("Pray", "Resist corruption and restore spirit", "action", power=12))
            deck.add_card(JourneyCard("Navigate", "Find the best path forward", "action", power=10))
            deck.add_card(JourneyCard("Rest", "Recover health and spirit", "action", power=8))
        else:  # balanced
            deck.add_card(JourneyCard("Hunt", "Search for food in the wilderness", "action", power=10))
            deck.add_card(JourneyCard("Navigate", "Find the best path forward", "action", power=10))
            deck.add_card(JourneyCard("Bargain", "Trade goods and negotiate", "action", power=10))
            deck.add_card(JourneyCard("Pray", "Resist corruption and restore spirit", "action", power=10))
            deck.add_card(JourneyCard("Rest", "Recover health and spirit", "action", power=8))
            
        return deck


# Initialize game state
default player = None
default current_enemy = None
default combat_active = False
default turn_number = 0

# Initialize pilgrimage game state
default pilgrim = None
default current_node = None
default journey_active = False
