## Pilgrimage Journey to Magi
## This file contains the journey gameplay flow

# Define journey-specific backgrounds
image bg salt_plains = "images/bg_salt_plains.png"
image bg fallen_forests = "images/bg_fallen_forests.png"
image bg clay_wastes = "images/bg_clay_wastes.png"
image bg high_road = "images/bg_high_road.png"
image bg storm_frontier = "images/bg_storm_frontier.png"
image bg magi_city = "images/bg_magi_city.png"
image bg shrine = "images/bg_shrine.png"
image bg settlement = "images/bg_settlement.png"
image bg ruins = "images/bg_ruins.png"

label start_journey:
    """Main entry point for the pilgrimage journey game"""
    
    scene bg black
    with dissolve
    
    "You are one soul among many, heading toward the Magi."
    "A holy living city that wanders the world's rim."
    "The city doesn't wait. It doesn't slow down."
    "You'd better keep pace."
    
    # Province selection
    menu:
        "Choose your starting province:"
        
        "Salt Plains - Fast travel, scarce water":
            $ pilgrim = Pilgrim("Traveler")
            $ pilgrim.current_province = PROVINCES["salt_plains"]
            
        "Fallen Forests - Slow travel, many encounters":
            $ pilgrim = Pilgrim("Traveler")
            $ pilgrim.current_province = PROVINCES["fallen_forests"]
            
        "Clay Wastes - Hazardous terrain, disease risk":
            $ pilgrim = Pilgrim("Traveler")
            $ pilgrim.current_province = PROVINCES["clay_wastes"]
            
        "High Pilgrim Road - Safe but long and tolls":
            $ pilgrim = Pilgrim("Traveler")
            $ pilgrim.current_province = PROVINCES["high_road"]
            
        "Storm Frontier - High risk, high reward":
            $ pilgrim = Pilgrim("Traveler")
            $ pilgrim.current_province = PROVINCES["storm_frontier"]
    
    "You have chosen the [pilgrim.current_province.name]."
    
    # Season selection
    menu:
        "Choose your starting season:"
        
        "Spring - Beasts awaken, moderate travel":
            $ pilgrim.current_season = "spring"
            
        "Summer - Hot and dry, water scarce":
            $ pilgrim.current_season = "summer"
            
        "Autumn - Bandits roam, harvest time":
            $ pilgrim.current_season = "autumn"
            
        "Winter - Slow and harsh, supplies critical":
            $ pilgrim.current_season = "winter"
    
    "You begin your journey in [pilgrim.current_season]."
    
    # Background selection
    menu:
        "Choose your background:"
        
        "Merchant - Extra supplies and carrying capacity":
            $ pilgrim.background = "merchant"
            $ pilgrim.sustenance = 120
            $ pilgrim.packweight_max = 25
            
        "Warrior - Strong and resilient":
            $ pilgrim.background = "warrior"
            $ pilgrim.health = 120
            $ pilgrim.spirit = 90
            
        "Priest - Deep faith and spiritual strength":
            $ pilgrim.background = "priest"
            $ pilgrim.spirit = 120
            $ pilgrim.health = 90
            
        "Scholar - Knowledgeable but frail":
            $ pilgrim.background = "scholar"
            $ pilgrim.spirit = 110
            $ pilgrim.packweight_max = 15
    
    "As a [pilgrim.background], you are prepared for the journey ahead."
    
    # Blessing selection
    menu:
        "Choose your starting blessing:"
        
        "Traveler's Grace - Move faster across the land":
            $ pilgrim.blessings.append("travelers_grace")
            
        "Iron Constitution - Resist illness and fatigue":
            $ pilgrim.blessings.append("iron_constitution")
            
        "Divine Protection - Preserve your spirit":
            $ pilgrim.blessings.append("divine_protection")
            
        "Light Burden - Carry more without strain":
            $ pilgrim.blessings.append("light_burden")
            $ pilgrim.packweight_max += 5
    
    # Deck selection
    menu:
        "Choose your starting deck focus:"
        
        "Hunter's Deck - Survive off the land":
            $ pilgrim.deck = create_starter_journey_deck("hunter")
            
        "Trader's Deck - Negotiate and barter":
            $ pilgrim.deck = create_starter_journey_deck("trader")
            
        "Faithful's Deck - Resist corruption through prayer":
            $ pilgrim.deck = create_starter_journey_deck("faithful")
            
        "Balanced Deck - Adapt to any situation":
            $ pilgrim.deck = create_starter_journey_deck("balanced")
    
    "Your deck is prepared. The journey begins."
    
    $ journey_active = True
    
    jump journey_loop

label journey_loop:
    """Main journey gameplay loop"""
    
    # Check win/lose conditions
    if not pilgrim.is_alive():
        jump journey_death
    
    if pilgrim.has_reached_magi():
        jump reach_magi
    
    # Display status
    call screen journey_status_screen
    
    # Daily progression
    $ pilgrim.days_traveled += 1
    $ pilgrim.drain_daily()
    
    # Calculate progress based on province and season
    $ travel_speed = pilgrim.current_province.get_modified_speed(pilgrim.current_season)
    
    # Apply traveler's grace blessing
    if "travelers_grace" in pilgrim.blessings:
        $ travel_speed *= 1.2
    
    $ pilgrim.progress += travel_speed
    
    "Day [pilgrim.days_traveled]: You travel [travel_speed:.0f] leagues."
    
    # Check if reached destination
    if pilgrim.has_reached_magi():
        jump reach_magi
    
    # Random node encounter
    $ node_roll = renpy.random.randint(1, 6)
    
    if node_roll == 1:
        jump node_camp
    elif node_roll == 2:
        jump node_crossroads
    elif node_roll == 3:
        jump node_shrine
    elif node_roll == 4:
        jump node_settlement
    elif node_roll == 5:
        jump node_wilderness
    else:
        jump node_ruins
    
    jump journey_loop

label node_camp:
    """Rest and recover at a camp"""
    scene bg forest
    
    "You come upon a sheltered spot suitable for camp."
    
    menu:
        "What will you do?"
        
        "Rest and recover (costs 10 sustenance)":
            if pilgrim.sustenance >= 10:
                $ pilgrim.sustenance -= 10
                $ pilgrim.health = min(100, pilgrim.health + 15)
                $ pilgrim.spirit = min(100, pilgrim.spirit + 10)
                "You rest and feel renewed."
            else:
                "You don't have enough supplies to rest properly."
                $ pilgrim.health = min(100, pilgrim.health + 5)
                
        "Craft and prepare (costs 5 sustenance)":
            if pilgrim.sustenance >= 5:
                $ pilgrim.sustenance -= 5
                "You spend time preparing for the road ahead."
                # Add a random action card
                $ new_card = JourneyCard("Navigate", "Find the best path", "action", power=10)
                $ pilgrim.deck.add_card(new_card)
            else:
                "You don't have enough supplies."
        
        "Push on without rest":
            "You decide to keep moving."
    
    jump journey_loop

label node_crossroads:
    """Choose a new direction"""
    scene bg high_road
    
    "You reach a crossroads. Multiple paths stretch before you."
    
    menu:
        "Which path do you take?"
        
        "The well-worn path (safer, slower)":
            $ pilgrim.progress += 5
            "You take the safer route."
            
        "The overgrown trail (faster, riskier)":
            $ pilgrim.progress += 15
            $ danger_roll = renpy.random.randint(1, 4)
            if danger_roll == 1:
                $ pilgrim.health -= 10
                "You stumble and injure yourself!"
                $ injury_card = JourneyCard("Sprained Ankle", "Slows your travel", "condition", power=-5)
                $ pilgrim.add_condition(injury_card)
            else:
                "You navigate successfully!"
    
    jump journey_loop

label node_shrine:
    """A holy place offering blessings or tests"""
    scene bg shrine
    
    "You discover an ancient shrine dedicated to the Magi."
    
    menu:
        "What do you do?"
        
        "Pray at the shrine (costs 10 spirit)":
            if pilgrim.spirit >= 10:
                $ pilgrim.spirit -= 10
                $ blessing_roll = renpy.random.randint(1, 3)
                if blessing_roll == 1:
                    $ pilgrim.spirit = min(100, pilgrim.spirit + 30)
                    $ pilgrim.corruption = max(0, pilgrim.corruption - 10)
                    "Your prayers are answered! You feel purified."
                else:
                    $ pilgrim.spirit = min(100, pilgrim.spirit + 15)
                    "You feel spiritually refreshed."
            else:
                "Your spirit is too weak to properly pray."
                
        "Search for relics":
            $ search_roll = renpy.random.randint(1, 4)
            if search_roll == 1:
                "You find a sacred relic!"
                $ relic = JourneyCard("Shrine Token", "Protects from corruption", "relic", power=2)
                if pilgrim.add_relic(relic):
                    "You add the Shrine Token to your pack."
                else:
                    "Your pack is too full to carry it."
            else:
                "You find nothing of value."
        
        "Move on respectfully":
            "You continue your journey."
    
    jump journey_loop

label node_settlement:
    """Trade and rest in a settlement"""
    scene bg settlement
    
    "You arrive at a small settlement of fellow pilgrims and traders."
    
    menu:
        "What do you do?"
        
        "Trade for supplies (costs 20 progress)":
            if pilgrim.progress >= 20:
                $ pilgrim.progress -= 20
                $ pilgrim.sustenance = min(100, pilgrim.sustenance + 40)
                "You trade some goods for food and water."
            else:
                "You have nothing of value to trade."
                
        "Hire protection (costs 30 progress)":
            if pilgrim.progress >= 30:
                $ pilgrim.progress -= 30
                $ pilgrim.companions.append("Guard")
                "A guard agrees to travel with you for a while."
            else:
                "You can't afford to hire help."
        
        "Listen to gossip":
            "You hear tales of other pilgrims and the road ahead."
            $ pilgrim.spirit = min(100, pilgrim.spirit + 5)
        
        "Move on quickly":
            "You don't linger in the settlement."
    
    jump journey_loop

label node_wilderness:
    """Dangerous encounters in the wild"""
    scene bg fallen_forests
    
    $ encounter_roll = renpy.random.randint(1, 5)
    
    if encounter_roll == 1:
        "A pack of wolves surrounds you!"
        $ pilgrim.health -= 20
        $ pilgrim.sustenance -= 10
        "You fight them off but suffer wounds and lose supplies."
        
    elif encounter_roll == 2:
        "You encounter a hermit living in the wilderness."
        menu:
            "Share your supplies with them? (costs 15 sustenance)":
                $ pilgrim.sustenance -= 15
                "The hermit blesses you for your kindness."
                $ pilgrim.spirit = min(100, pilgrim.spirit + 15)
                
            "Politely decline":
                "You continue on your way."
                
    elif encounter_roll == 3:
        "A lost caravan needs help!"
        menu:
            "Help them (costs time and health)":
                $ pilgrim.progress -= 10
                $ pilgrim.health -= 5
                "You help them back to the path. They share supplies with you."
                $ pilgrim.sustenance = min(100, pilgrim.sustenance + 20)
                
            "Leave them to their fate":
                "You press on alone."
                $ pilgrim.corruption += 5
                
    elif encounter_roll == 4:
        "A corrupted pilgrim blocks your path!"
        "They demand you turn back or join them in darkness."
        menu:
            "Resist with faith (costs 20 spirit)":
                if pilgrim.spirit >= 20:
                    $ pilgrim.spirit -= 20
                    "Your faith drives them away!"
                    $ pilgrim.spirit = min(100, pilgrim.spirit + 10)
                else:
                    "Your spirit is too weak. You flee!"
                    $ pilgrim.progress -= 15
                    
            "Fight them (costs 15 health)":
                $ pilgrim.health -= 15
                "You defeat them but are wounded."
                
            "Flee":
                $ pilgrim.progress -= 20
                "You escape but lose ground."
    else:
        "The wilderness is quiet today."
        "You find some edible plants."
        $ pilgrim.sustenance = min(100, pilgrim.sustenance + 10)
    
    jump journey_loop

label node_ruins:
    """Ancient ruins with dangers and treasures"""
    scene bg ruins
    
    "You discover ancient ruins, remnants of an age long past."
    
    menu:
        "What do you do?"
        
        "Explore carefully":
            $ explore_roll = renpy.random.randint(1, 4)
            if explore_roll == 1:
                "You find a powerful relic!"
                $ relic = JourneyCard("Ancient Compass", "Improves navigation", "relic", power=3)
                if pilgrim.add_relic(relic):
                    "You add the Ancient Compass to your pack."
                else:
                    "Your pack is too full."
            elif explore_roll == 2:
                "A trap springs! You're injured."
                $ pilgrim.health -= 15
                $ injury = JourneyCard("Curse Wound", "Slowly drains health", "condition", power=-2)
                $ pilgrim.add_condition(injury)
            else:
                "You find nothing of interest."
                
        "Loot quickly and run":
            $ pilgrim.sustenance = min(100, pilgrim.sustenance + 10)
            "You grab what you can and flee."
            $ curse_roll = renpy.random.randint(1, 3)
            if curse_roll == 1:
                $ pilgrim.corruption += 10
                "You feel a dark presence following you."
        
        "Avoid the ruins":
            "You wisely avoid the dangerous ruins."
    
    jump journey_loop

label reach_magi:
    """The pilgrim reaches the holy city"""
    scene bg magi_city
    with dissolve
    
    "After [pilgrim.days_traveled] days of travel, you finally see it..."
    "The Magi. The holy living city."
    "It towers before you, vast and impossible, wandering the world's rim."
    
    # Calculate final outcome based on multiple factors
    $ corruption_level = pilgrim.corruption
    $ spirit_level = pilgrim.spirit
    $ companion_count = len(pilgrim.companions)
    $ relic_count = len(pilgrim.relics)
    
    # Determine ending
    if corruption_level >= 50:
        jump ending_consumed
    elif spirit_level <= 20:
        jump ending_turned_away
    elif spirit_level >= 70 and corruption_level < 20:
        jump ending_blessed
    else:
        jump ending_wall
    
    return

label ending_blessed:
    """Best ending - receive the blessing"""
    "The gates of Magi open before you."
    "Your spirit burns bright, uncorrupted by the journey."
    "The city welcomes you as one of the faithful."
    
    "You have been BLESSED by the Magi."
    "Your pilgrimage is complete."
    
    $ journey_active = False
    return

label ending_turned_away:
    """Spirit too low - not ready"""
    "You approach the gates, but your spirit is broken."
    "The journey has taken too much from you."
    "The city's guardians shake their heads sadly."
    
    "You are TURNED AWAY."
    "Perhaps you will try again, when your spirit is renewed."
    
    $ journey_active = False
    return

label ending_consumed:
    """Corruption too high - dark ending"""
    "As you approach the city, the corruption within you grows."
    "The darkness you've accumulated on the journey consumes you."
    "You cannot enter the holy city in this state."
    
    "You are CONSUMED by corruption."
    "Your soul becomes another wandering shadow on the pilgrim road."
    
    $ journey_active = False
    return

label ending_wall:
    """Neutral ending - become part of the city"""
    "The Magi receives you, but not as you hoped."
    "Your journey was marked by compromise and survival."
    "Neither fully blessed nor fully corrupted."
    
    "You become part of the OUTER WALL."
    "Your spirit joins the countless others who protect the city."
    "Not the ending you sought, but an ending nonetheless."
    
    $ journey_active = False
    return

label journey_death:
    """Death on the journey"""
    scene bg black
    
    if pilgrim.health <= 0:
        "Your body gives out. The journey was too much."
    elif pilgrim.spirit <= 0:
        "Your spirit breaks. You can no longer continue."
    else:
        "You collapse on the pilgrim road."
    
    "After [pilgrim.days_traveled] days of travel..."
    "Your pilgrimage ends here."
    
    "GAME OVER"
    
    $ journey_active = False
    return
