#!/usr/bin/env python3
"""
Test script for pilgrimage journey mechanics.
This tests the core Python classes for the journey game independent of Ren'Py.
"""

import random
import sys


class JourneyCard:
    """Cards for the pilgrimage journey game"""
    def __init__(self, name, description, card_type, effect=None, power=0):
        self.name = name
        self.description = description
        self.card_type = card_type
        self.effect = effect
        self.power = power
        self.is_permanent = (card_type == "relic")
        
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
        self.sustenance = 100
        self.health = 100
        self.spirit = 100
        self.packweight_current = 0
        self.packweight_max = 20
        self.progress = 0
        self.progress_goal = 1000
        
        # Additional attributes
        self.corruption = 0
        self.companions = []
        self.relics = []
        self.blessings = []
        
        # Journey state
        self.current_province = None
        self.current_season = None
        self.days_traveled = 0
        self.deck = JourneyDeck()
        
    def drain_daily(self):
        """Daily resource drain based on travel"""
        sustenance_drain = 5
        
        if self.current_season == "winter":
            sustenance_drain += 2
        elif self.current_season == "summer":
            sustenance_drain += 3
            
        self.sustenance = max(0, self.sustenance - sustenance_drain)
        
        if self.sustenance < 20:
            self.health = max(0, self.health - 3)
        
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
        return False
        
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
        self.permanent_relics = []
        
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


class Province:
    """Represents a region with specific terrain and difficulty"""
    def __init__(self, name, terrain_type, difficulty, travel_speed):
        self.name = name
        self.terrain_type = terrain_type
        self.difficulty = difficulty
        self.travel_speed = travel_speed
        self.encounter_types = []
        
    def get_modified_speed(self, season):
        """Get travel speed modified by season"""
        speed = self.travel_speed
        if season == "winter":
            speed *= 0.7
        elif season == "summer":
            if self.terrain_type == "salt_plains":
                speed *= 0.8
            else:
                speed *= 1.1
        elif season == "spring":
            speed *= 1.0
        elif season == "autumn":
            speed *= 0.9
        return speed


def create_starter_journey_deck(deck_type="balanced"):
    """Create starting deck for pilgrimage"""
    deck = JourneyDeck()
    
    if deck_type == "hunter":
        deck.add_card(JourneyCard("Hunt", "Search for food", "action", power=15))
        deck.add_card(JourneyCard("Hunt", "Search for food", "action", power=15))
        deck.add_card(JourneyCard("Navigate", "Find path", "action", power=10))
        deck.add_card(JourneyCard("Rest", "Recover", "action", power=8))
    elif deck_type == "trader":
        deck.add_card(JourneyCard("Bargain", "Trade goods", "action", power=12))
        deck.add_card(JourneyCard("Bargain", "Trade goods", "action", power=12))
        deck.add_card(JourneyCard("Navigate", "Find path", "action", power=10))
        deck.add_card(JourneyCard("Rest", "Recover", "action", power=8))
    elif deck_type == "faithful":
        deck.add_card(JourneyCard("Pray", "Resist corruption", "action", power=12))
        deck.add_card(JourneyCard("Pray", "Resist corruption", "action", power=12))
        deck.add_card(JourneyCard("Navigate", "Find path", "action", power=10))
        deck.add_card(JourneyCard("Rest", "Recover", "action", power=8))
    else:
        deck.add_card(JourneyCard("Hunt", "Search for food", "action", power=10))
        deck.add_card(JourneyCard("Navigate", "Find path", "action", power=10))
        deck.add_card(JourneyCard("Bargain", "Trade goods", "action", power=10))
        deck.add_card(JourneyCard("Pray", "Resist corruption", "action", power=10))
        deck.add_card(JourneyCard("Rest", "Recover", "action", power=8))
        
    return deck


# ===== TEST FUNCTIONS =====

def test_journey_card_creation():
    """Test creating journey cards"""
    print("Testing journey card creation...")
    
    action_card = JourneyCard("Hunt", "Search for food", "action", power=10)
    assert action_card.name == "Hunt"
    assert action_card.card_type == "action"
    assert not action_card.is_permanent
    
    relic_card = JourneyCard("Amber Reliquary", "Remove condition", "relic", power=3)
    assert relic_card.card_type == "relic"
    assert relic_card.is_permanent
    
    condition_card = JourneyCard("Fatigue", "Reduces effectiveness", "condition", power=-5)
    assert condition_card.card_type == "condition"
    assert not condition_card.is_permanent
    
    print("✓ Journey card creation works")


def test_pilgrim_initialization():
    """Test pilgrim creation"""
    print("Testing pilgrim initialization...")
    
    pilgrim = Pilgrim("Traveler")
    assert pilgrim.name == "Traveler"
    assert pilgrim.sustenance == 100
    assert pilgrim.health == 100
    assert pilgrim.spirit == 100
    assert pilgrim.progress == 0
    assert pilgrim.progress_goal == 1000
    assert pilgrim.packweight_max == 20
    assert pilgrim.packweight_current == 0
    assert pilgrim.corruption == 0
    assert len(pilgrim.companions) == 0
    assert len(pilgrim.relics) == 0
    
    print("✓ Pilgrim initialization works")


def test_daily_drain():
    """Test daily resource drain"""
    print("Testing daily resource drain...")
    
    pilgrim = Pilgrim("Traveler")
    pilgrim.current_season = "spring"
    
    initial_sustenance = pilgrim.sustenance
    pilgrim.drain_daily()
    assert pilgrim.sustenance < initial_sustenance
    
    # Test winter increases drain
    pilgrim2 = Pilgrim("Traveler")
    pilgrim2.current_season = "winter"
    pilgrim2.drain_daily()
    assert pilgrim2.sustenance < pilgrim.sustenance
    
    # Test low sustenance affects health
    pilgrim3 = Pilgrim("Traveler")
    pilgrim3.sustenance = 15
    initial_health = pilgrim3.health
    pilgrim3.drain_daily()
    assert pilgrim3.health < initial_health
    
    print("✓ Daily drain works")


def test_hand_size_scaling():
    """Test hand size based on spirit"""
    print("Testing hand size scaling...")
    
    pilgrim = Pilgrim("Traveler")
    
    pilgrim.spirit = 100
    assert pilgrim.get_hand_size() == 5
    
    pilgrim.spirit = 70
    assert pilgrim.get_hand_size() == 4
    
    pilgrim.spirit = 50
    assert pilgrim.get_hand_size() == 3
    
    pilgrim.spirit = 30
    assert pilgrim.get_hand_size() == 2
    
    pilgrim.spirit = 10
    assert pilgrim.get_hand_size() == 1
    
    print("✓ Hand size scaling works")


def test_relic_management():
    """Test adding and managing relics"""
    print("Testing relic management...")
    
    pilgrim = Pilgrim("Traveler")
    relic1 = JourneyCard("Light Relic", "A small trinket", "relic", power=5)
    relic2 = JourneyCard("Heavy Relic", "A massive artifact", "relic", power=25)
    
    # Should be able to add light relic
    assert pilgrim.add_relic(relic1)
    assert len(pilgrim.relics) == 1
    assert pilgrim.packweight_current == 5
    
    # Should not be able to add heavy relic (too heavy)
    assert not pilgrim.add_relic(relic2)
    assert len(pilgrim.relics) == 1
    
    print("✓ Relic management works")


def test_pilgrim_alive_check():
    """Test alive status checking"""
    print("Testing alive status...")
    
    pilgrim = Pilgrim("Traveler")
    assert pilgrim.is_alive()
    
    pilgrim.health = 0
    assert not pilgrim.is_alive()
    
    pilgrim.health = 50
    pilgrim.spirit = 0
    assert not pilgrim.is_alive()
    
    print("✓ Alive status checking works")


def test_progress_tracking():
    """Test journey progress tracking"""
    print("Testing progress tracking...")
    
    pilgrim = Pilgrim("Traveler")
    assert not pilgrim.has_reached_magi()
    
    pilgrim.progress = 500
    assert not pilgrim.has_reached_magi()
    
    pilgrim.progress = 1000
    assert pilgrim.has_reached_magi()
    
    pilgrim.progress = 1500
    assert pilgrim.has_reached_magi()
    
    print("✓ Progress tracking works")


def test_journey_deck_operations():
    """Test journey deck operations"""
    print("Testing journey deck operations...")
    
    deck = JourneyDeck()
    
    # Add regular cards
    card1 = JourneyCard("Hunt", "Hunt for food", "action", power=10)
    card2 = JourneyCard("Navigate", "Find path", "action", power=10)
    deck.add_card(card1)
    deck.add_card(card2)
    assert len(deck.cards) == 2
    
    # Add relic (should go to permanent relics)
    relic = JourneyCard("Compass", "Navigation aid", "relic", power=3)
    deck.add_card(relic)
    assert len(deck.permanent_relics) == 1
    assert len(deck.cards) == 2
    
    # Prepare for node
    deck.prepare_for_node()
    assert len(deck.draw_pile) == 2
    assert len(deck.hand) == 0
    assert len(deck.discard_pile) == 0
    
    # Draw cards
    drawn = deck.draw_card(2)
    assert len(drawn) == 2
    assert len(deck.hand) == 2
    assert len(deck.draw_pile) == 0
    
    print("✓ Journey deck operations work")


def test_deck_cycling():
    """Test deck cycling when draw pile is empty"""
    print("Testing deck cycling...")
    
    deck = JourneyDeck()
    for i in range(5):
        deck.add_card(JourneyCard(f"Card {i}", "Test", "action", power=5))
    
    deck.prepare_for_node()
    
    # Draw all cards
    deck.draw_card(5)
    assert len(deck.hand) == 5
    assert len(deck.draw_pile) == 0
    
    # Discard all
    deck.discard_hand()
    assert len(deck.discard_pile) == 5
    assert len(deck.hand) == 0
    
    # Draw should shuffle discard into draw
    deck.draw_card(3)
    assert len(deck.hand) == 3
    assert len(deck.discard_pile) == 0
    assert len(deck.draw_pile) == 2
    
    print("✓ Deck cycling works")


def test_province_travel_speed():
    """Test province travel speed with seasons"""
    print("Testing province travel speed...")
    
    province = Province("Test Plains", "plains", 2, 10)
    
    spring_speed = province.get_modified_speed("spring")
    assert spring_speed == 10.0
    
    winter_speed = province.get_modified_speed("winter")
    assert winter_speed == 7.0
    
    summer_speed = province.get_modified_speed("summer")
    assert summer_speed == 11.0
    
    autumn_speed = province.get_modified_speed("autumn")
    assert autumn_speed == 9.0
    
    print("✓ Province travel speed works")


def test_starter_decks():
    """Test starter deck creation"""
    print("Testing starter deck creation...")
    
    hunter_deck = create_starter_journey_deck("hunter")
    assert len(hunter_deck.cards) == 4
    
    trader_deck = create_starter_journey_deck("trader")
    assert len(trader_deck.cards) == 4
    
    faithful_deck = create_starter_journey_deck("faithful")
    assert len(faithful_deck.cards) == 4
    
    balanced_deck = create_starter_journey_deck("balanced")
    assert len(balanced_deck.cards) == 5
    
    print("✓ Starter deck creation works")


def test_condition_cards():
    """Test adding condition cards to deck"""
    print("Testing condition card mechanics...")
    
    pilgrim = Pilgrim("Traveler")
    initial_deck_size = len(pilgrim.deck.cards)
    
    condition = JourneyCard("Fatigue", "Slows travel", "condition", power=-5)
    pilgrim.add_condition(condition)
    
    assert len(pilgrim.deck.cards) == initial_deck_size + 1
    assert condition in pilgrim.deck.cards
    
    print("✓ Condition card mechanics work")


# ===== RUN ALL TESTS =====

def run_all_tests():
    """Run all journey game tests"""
    print("=" * 50)
    print("Running Journey Game Tests")
    print("=" * 50)
    
    try:
        test_journey_card_creation()
        test_pilgrim_initialization()
        test_daily_drain()
        test_hand_size_scaling()
        test_relic_management()
        test_pilgrim_alive_check()
        test_progress_tracking()
        test_journey_deck_operations()
        test_deck_cycling()
        test_province_travel_speed()
        test_starter_decks()
        test_condition_cards()
        
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
