## The script of the game goes in this file.

## Define background images
image bg black = "images/bg_black.png"
image bg forest = "images/bg_forest.png"
image bg cave = "images/bg_cave.png"
image bg boss_room = "images/bg_boss_room.png"
image bg victory = "images/bg_victory.png"

## The game starts here.

label start:
    
    # Initialize the player
    $ player = Player("Hero")
    $ player.deck = create_starter_deck()
    
    scene bg black
    with dissolve
    
    "Welcome to Magi: Deck Builder!"
    "You are a young mage embarking on a journey to master the mystical arts."
    "Build your deck, make wise choices, and overcome the challenges ahead!"
    
    menu:
        "Choose your specialization:"
        
        "Offensive Mage":
            "You focus on dealing damage to your enemies."
            $ player.deck.add_card(Card("Fireball", "Deal 9 damage.", "attack", cost=2, power=9))
            
        "Defensive Mage":
            "You focus on protecting yourself."
            $ player.deck.add_card(Card("Shield Barrier", "Gain 8 block.", "defense", cost=2, power=8))
            
        "Balanced Mage":
            "You maintain balance between offense and defense."
            $ player.deck.add_card(Card("Quick Strike", "Deal 4 damage. Draw 1 card.", "attack", cost=1, power=4))
    
    "Your journey begins!"
    
    jump first_encounter

label first_encounter:
    
    scene bg forest
    with dissolve
    
    "As you travel through the mystical forest, you encounter a goblin blocking your path!"
    
    $ current_enemy = Enemy("Goblin Scout", 30, 6)
    
    call combat_encounter from _call_combat_encounter_1
    
    if player.hp <= 0:
        jump game_over
    
    "Victory! You defeated the Goblin Scout!"
    
    # Offer a card reward
    $ reward_cards = [
        Card("Heavy Strike", "Deal 12 damage.", "attack", cost=2, power=12),
        Card("Iron Defense", "Gain 10 block.", "defense", cost=2, power=10),
        Card("Swift Strike", "Deal 4 damage. Costs 0 energy.", "attack", cost=0, power=4)
    ]
    
    call screen reward_screen(reward_cards)
    
    if _return != -1:
        $ chosen_card = reward_cards[_return]
        $ player.deck.add_card(chosen_card)
        "You added [chosen_card.name] to your deck!"
    else:
        "You chose not to add a card to your deck."
    
    $ player.heal(10)
    "You rest and recover 10 HP."
    
    jump second_encounter

label second_encounter:
    
    scene bg cave
    with dissolve
    
    "You venture deeper into the wilderness and discover a dark cave."
    
    menu:
        "What do you do?"
        
        "Enter the cave":
            "You cautiously enter the cave..."
            "A pack of wolves emerges from the shadows!"
            $ current_enemy = Enemy("Wolf Pack", 45, 8)
            
        "Rest outside the cave":
            "You decide to rest and regain your strength."
            $ player.heal(15)
            "You recovered 15 HP."
            "But as you rest, a wandering troll discovers you!"
            $ current_enemy = Enemy("Hill Troll", 50, 10)
    
    call combat_encounter from _call_combat_encounter_2
    
    if player.hp <= 0:
        jump game_over
    
    "Victory! You survived the encounter!"
    
    # Offer another card reward
    $ reward_cards = [
        Card("Power Strike", "Deal 15 damage. Costs 3 energy.", "attack", cost=3, power=15),
        Card("Dodge", "Gain 6 block. Draw 1 card.", "defense", cost=1, power=6),
        Card("Meditation", "Gain 2 energy next turn.", "skill", cost=1)
    ]
    
    call screen reward_screen(reward_cards)
    
    if _return != -1:
        $ chosen_card = reward_cards[_return]
        $ player.deck.add_card(chosen_card)
        "You added [chosen_card.name] to your deck!"
    
    $ player.gold += 50
    "You found 50 gold!"
    
    jump final_boss

label final_boss:
    
    scene bg boss_room
    with dissolve
    
    "You reach the heart of the dungeon."
    "Before you stands the Dark Sorcerer, the source of all evil in these lands!"
    
    "Dark Sorcerer" "Foolish mortal! You dare challenge me?"
    
    menu:
        "This is your final test. Are you ready?"
        
        "Face the Dark Sorcerer!":
            "You steel yourself for the ultimate battle!"
            
        "Check your deck first":
            call screen deck_view
            "Your deck is ready. It's time to fight!"
    
    $ current_enemy = Enemy("Dark Sorcerer", 80, 12)
    
    call combat_encounter from _call_combat_encounter_3
    
    if player.hp <= 0:
        jump game_over
    
    jump victory

label victory:
    
    scene bg victory
    with dissolve
    
    "The Dark Sorcerer falls, his power dissipating into the ether."
    "You have saved the realm from darkness!"
    
    "Congratulations, [player.name]!"
    "You have completed your journey and mastered the art of deck building."
    "Your final stats:"
    "HP: [player.hp]/[player.max_hp]"
    "Deck size: [player.deck.get_deck_size()] cards"
    "Gold: [player.gold]"
    
    "Thank you for playing Magi: Deck Builder CYOA!"
    
    return

label game_over:
    
    scene bg black
    with dissolve
    
    "You have been defeated..."
    "Your journey ends here."
    
    menu:
        "What would you like to do?"
        
        "Try Again":
            jump start
            
        "Return to Main Menu":
            return

label combat_encounter:
    
    # Prepare for combat
    $ combat_active = True
    $ turn_number = 1
    $ player.deck.prepare_for_combat()
    
    # Draw initial hand
    $ player.deck.draw_card(5)
    $ player.start_turn()
    
    # Combat loop
    label combat_loop:
        
        # Use call screen for proper Ren'Py interaction
        call screen combat_ui
        
        $ player_action = _return
        
        if player_action == "end_turn":
            # Player ends turn
            
            # Enemy turn
            "The [current_enemy.name] attacks!"
            $ current_enemy.execute_intent(player)
            
            if player.hp <= 0:
                $ combat_active = False
                return
            
            # New turn setup
            $ turn_number += 1
            $ player.deck.discard_hand()
            $ player.start_turn()
            $ player.deck.draw_card(5)
            
            jump combat_loop
            
        elif player_action[0] == "play_card":
            # Player plays a card
            $ card_index = player_action[1]
            $ card = player.deck.hand[card_index]
            
            if player.spend_energy(card.cost):
                # Execute card effect
                $ result = card.play(player, current_enemy)
                
                if "damage" in result:
                    $ damage_dealt = current_enemy.take_damage(result["damage"])
                    "[card.name] deals [damage_dealt] damage to [current_enemy.name]!"
                
                if "block" in result:
                    $ player.gain_block(result["block"])
                    "[card.name] grants [result['block']] block!"
                
                # Remove card from hand
                $ player.deck.discard_card(card)
                
                # Check if enemy is defeated
                if current_enemy.hp <= 0:
                    $ combat_active = False
                    return
            else:
                "Not enough energy!"
            
            jump combat_loop
    
    return
