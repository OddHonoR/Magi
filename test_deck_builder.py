#!/usr/bin/env python3
"""
Test script for deck builder mechanics.
This tests the core Python classes independent of Ren'Py.
"""

import random
import sys

class Card:
    """Base class for cards in the deck builder"""
    def __init__(self, name, description, card_type, cost=0, power=0, effect=None):
        self.name = name
        self.description = description
        self.card_type = card_type
        self.cost = cost
        self.power = power
        self.effect = effect
        
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
                if self.discard_pile:
                    self.draw_pile = self.discard_pile.copy()
                    self.discard_pile = []
                    self.shuffle()
                else:
                    break
                    
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
        self.intent = "attack"
        
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


def create_starter_deck():
    """Create the starting deck"""
    deck = Deck()
    
    for _ in range(5):
        deck.add_card(Card("Strike", "Deal 6 damage.", "attack", cost=1, power=6))
    
    for _ in range(5):
        deck.add_card(Card("Defend", "Gain 5 block.", "defense", cost=1, power=5))
    
    return deck


# Test functions
def test_card_creation():
    """Test creating cards"""
    print("Testing card creation...")
    card = Card("Strike", "Deal 6 damage.", "attack", cost=1, power=6)
    assert card.name == "Strike"
    assert card.cost == 1
    assert card.power == 6
    assert card.card_type == "attack"
    print("✓ Card creation works")


def test_deck_operations():
    """Test deck operations"""
    print("\nTesting deck operations...")
    deck = Deck()
    
    # Add cards
    for i in range(10):
        deck.add_card(Card(f"Card {i}", "Test card", "attack", cost=1, power=1))
    
    assert deck.get_deck_size() == 10
    print("✓ Adding cards works")
    
    # Prepare for combat
    deck.prepare_for_combat()
    assert len(deck.draw_pile) == 10
    assert len(deck.hand) == 0
    assert len(deck.discard_pile) == 0
    print("✓ Combat preparation works")
    
    # Draw cards
    drawn = deck.draw_card(5)
    assert len(drawn) == 5
    assert len(deck.hand) == 5
    assert len(deck.draw_pile) == 5
    print("✓ Drawing cards works")
    
    # Discard hand
    deck.discard_hand()
    assert len(deck.hand) == 0
    assert len(deck.discard_pile) == 5
    print("✓ Discarding hand works")
    
    # Draw remaining and test cycling
    deck.draw_card(5)
    deck.discard_hand()
    deck.draw_card(5)  # Should reshuffle
    assert len(deck.hand) == 5
    print("✓ Deck cycling works")


def test_player_mechanics():
    """Test player mechanics"""
    print("\nTesting player mechanics...")
    player = Player("Test Hero", max_hp=100, max_energy=3)
    
    assert player.hp == 100
    assert player.energy == 3
    print("✓ Player initialization works")
    
    # Test damage without block
    damage = player.take_damage(10)
    assert player.hp == 90
    assert damage == 10
    print("✓ Taking damage works")
    
    # Test damage with block
    player.gain_block(15)
    damage = player.take_damage(10)
    assert player.block == 5
    assert player.hp == 90
    assert damage == 0
    print("✓ Block mechanics work")
    
    # Test damage exceeding block
    damage = player.take_damage(10)
    assert player.block == 0
    assert player.hp == 85
    assert damage == 5
    print("✓ Damage exceeding block works")
    
    # Test healing
    player.heal(20)
    assert player.hp == 100
    print("✓ Healing works")
    
    # Test energy
    assert player.spend_energy(2)
    assert player.energy == 1
    assert not player.spend_energy(5)
    print("✓ Energy management works")
    
    # Test turn reset
    player.gain_block(10)
    player.start_turn()
    assert player.block == 0
    assert player.energy == 3
    print("✓ Turn reset works")


def test_enemy_mechanics():
    """Test enemy mechanics"""
    print("\nTesting enemy mechanics...")
    enemy = Enemy("Test Goblin", 30, 6)
    
    assert enemy.hp == 30
    assert enemy.attack_power == 6
    print("✓ Enemy initialization works")
    
    # Test damage
    damage = enemy.take_damage(10)
    assert enemy.hp == 20
    assert damage == 10
    print("✓ Enemy taking damage works")
    
    # Test with block
    enemy.gain_block(5)
    damage = enemy.take_damage(3)
    assert enemy.block == 2
    assert enemy.hp == 20
    print("✓ Enemy block works")


def test_card_effects():
    """Test card effects in combat"""
    print("\nTesting card effects...")
    player = Player("Hero")
    enemy = Enemy("Goblin", 30, 6)
    
    # Test attack card
    strike = Card("Strike", "Deal 6 damage.", "attack", cost=1, power=6)
    result = strike.play(player, enemy)
    assert result["damage"] == 6
    
    damage = enemy.take_damage(result["damage"])
    assert enemy.hp == 24
    print("✓ Attack cards work")
    
    # Test defense card
    defend = Card("Defend", "Gain 5 block.", "defense", cost=1, power=5)
    result = defend.play(player, enemy)
    assert result["block"] == 5
    
    player.gain_block(result["block"])
    assert player.block == 5
    print("✓ Defense cards work")


def test_starter_deck():
    """Test starter deck creation"""
    print("\nTesting starter deck...")
    deck = create_starter_deck()
    
    assert deck.get_deck_size() == 10
    
    # Count card types
    strikes = sum(1 for card in deck.cards if card.name == "Strike")
    defends = sum(1 for card in deck.cards if card.name == "Defend")
    
    assert strikes == 5
    assert defends == 5
    print("✓ Starter deck creation works")


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("Running Deck Builder Tests")
    print("="*50)
    
    try:
        test_card_creation()
        test_deck_operations()
        test_player_mechanics()
        test_enemy_mechanics()
        test_card_effects()
        test_starter_deck()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50)
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
