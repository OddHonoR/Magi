## UI Screens for Pilgrimage Journey

screen journey_status_screen():
    """Display current journey status"""
    
    frame:
        xalign 0.5
        yalign 0.1
        padding (20, 20)
        
        vbox:
            spacing 10
            
            text "[pilgrim.name] - Day [pilgrim.days_traveled]" size 24 bold True
            
            text "Province: [pilgrim.current_province.name]" size 18
            text "Season: [pilgrim.current_season.capitalize()]" size 18
            
            null height 10
            
            # Stats display
            hbox:
                spacing 30
                
                vbox:
                    text "Sustenance" size 16
                    bar value pilgrim.sustenance range 100 xsize 150
                    text "[pilgrim.sustenance]/100" size 14
                
                vbox:
                    text "Health" size 16
                    bar value pilgrim.health range 100 xsize 150
                    text "[pilgrim.health]/100" size 14
                
                vbox:
                    text "Spirit" size 16
                    bar value pilgrim.spirit range 100 xsize 150
                    text "[pilgrim.spirit]/100" size 14
            
            null height 10
            
            text "Progress: [pilgrim.progress:.0f] / [pilgrim.progress_goal]" size 16
            bar value pilgrim.progress range pilgrim.progress_goal xsize 450
            
            null height 10
            
            text "Pack: [pilgrim.packweight_current] / [pilgrim.packweight_max]" size 14
            text "Corruption: [pilgrim.corruption]" size 14
            text "Companions: [len(pilgrim.companions)]" size 14
            text "Relics: [len(pilgrim.relics)]" size 14
            
            null height 20
            
            textbutton "Continue Journey" action Return()


screen journey_hand_display():
    """Display cards in hand during a node encounter"""
    
    frame:
        xalign 0.5
        yalign 0.8
        padding (20, 20)
        
        vbox:
            spacing 10
            
            text "Your Hand" size 20 bold True
            
            hbox:
                spacing 10
                
                for i, card in enumerate(pilgrim.deck.hand):
                    button:
                        xsize 150
                        ysize 200
                        
                        vbox:
                            text "[card.name]" size 16 bold True
                            null height 5
                            text "[card.description]" size 12 color "#ccc"
                            null height 10
                            text "Type: [card.card_type]" size 10
                            text "Power: [card.power]" size 10
                        
                        action Return(i)


screen journey_deck_view():
    """View entire deck"""
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        xsize 800
        ysize 600
        
        vbox:
            spacing 15
            
            text "Your Deck" size 24 bold True
            
            null height 10
            
            text "Total Cards: [len(pilgrim.deck.cards)]" size 16
            
            null height 10
            
            viewport:
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 8
                    
                    # Action cards
                    text "Action Cards:" size 18 bold True color "#6f6"
                    for card in pilgrim.deck.cards:
                        if card.card_type == "action":
                            hbox:
                                spacing 10
                                text "• [card.name]" size 14
                                text "- [card.description]" size 12 color "#ccc"
                    
                    null height 10
                    
                    # Condition cards
                    text "Condition Cards:" size 18 bold True color "#f66"
                    for card in pilgrim.deck.cards:
                        if card.card_type == "condition":
                            hbox:
                                spacing 10
                                text "• [card.name]" size 14
                                text "- [card.description]" size 12 color "#ccc"
                    
                    null height 10
                    
                    # Relics (in deck, not permanent)
                    text "Relic Cards:" size 18 bold True color "#fc6"
                    for card in pilgrim.deck.cards:
                        if card.card_type == "relic":
                            hbox:
                                spacing 10
                                text "• [card.name]" size 14
                                text "- [card.description]" size 12 color "#ccc"
                    
                    null height 10
                    
                    # Permanent relics
                    if len(pilgrim.relics) > 0:
                        text "Permanent Relics:" size 18 bold True color "#fa0"
                        for relic in pilgrim.relics:
                            hbox:
                                spacing 10
                                text "• [relic.name]" size 14
                                text "- [relic.description]" size 12 color "#ccc"
            
            null height 20
            
            textbutton "Close" action Return()


screen journey_card_reward(reward_cards):
    """Select a card reward after an event"""
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        
        vbox:
            spacing 15
            
            text "Choose a card to add to your deck:" size 20 bold True
            
            null height 10
            
            hbox:
                spacing 20
                
                for i, card in enumerate(reward_cards):
                    button:
                        xsize 180
                        ysize 250
                        
                        vbox:
                            spacing 8
                            
                            text "[card.name]" size 18 bold True
                            
                            null height 5
                            
                            text "[card.description]" size 12 color "#ccc"
                            
                            null height 10
                            
                            text "Type: [card.card_type]" size 11
                            text "Power: [card.power]" size 11
                            
                            if card.card_type == "relic":
                                text "Weight: [card.power]" size 11 color "#fa0"
                        
                        action Return(i)
            
            null height 20
            
            textbutton "Skip (Keep deck lean)" action Return(-1)


screen journey_event_choice(event):
    """Display an event and its choices"""
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        xsize 700
        
        vbox:
            spacing 15
            
            text "[event.name]" size 22 bold True
            
            null height 10
            
            text "[event.description]" size 14
            
            null height 20
            
            for i, (choice_text, _) in enumerate(event.choices):
                textbutton "[choice_text]" action Return(i)


screen journey_stats_detailed():
    """Detailed stats view"""
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        xsize 600
        ysize 700
        
        vbox:
            spacing 12
            
            text "Pilgrim Status" size 24 bold True
            
            null height 10
            
            text "Name: [pilgrim.name]" size 16
            text "Background: [pilgrim.background.capitalize()]" size 16
            text "Days Traveled: [pilgrim.days_traveled]" size 16
            
            null height 15
            
            text "Current Location" size 20 bold True
            text "Province: [pilgrim.current_province.name]" size 14
            text "Season: [pilgrim.current_season.capitalize()]" size 14
            text "Terrain: [pilgrim.current_province.terrain_type]" size 14
            text "Difficulty: [pilgrim.current_province.difficulty]/5" size 14
            
            null height 15
            
            text "Core Stats" size 20 bold True
            
            hbox:
                spacing 20
                vbox:
                    text "Sustenance: [pilgrim.sustenance]/100" size 14
                    bar value pilgrim.sustenance range 100 xsize 200
                    
                    null height 5
                    
                    text "Health: [pilgrim.health]/100" size 14
                    bar value pilgrim.health range 100 xsize 200
                    
                    null height 5
                    
                    text "Spirit: [pilgrim.spirit]/100" size 14
                    bar value pilgrim.spirit range 100 xsize 200
            
            null height 15
            
            text "Journey Progress" size 20 bold True
            text "Distance: [pilgrim.progress:.0f] / [pilgrim.progress_goal]" size 14
            bar value pilgrim.progress range pilgrim.progress_goal xsize 400
            text "Progress: [pilgrim.progress * 100 / pilgrim.progress_goal:.1f]%" size 14
            
            null height 15
            
            text "Inventory" size 20 bold True
            text "Pack Weight: [pilgrim.packweight_current] / [pilgrim.packweight_max]" size 14
            text "Corruption: [pilgrim.corruption]" size 14
            
            null height 10
            
            if len(pilgrim.companions) > 0:
                text "Companions:" size 16
                for companion in pilgrim.companions:
                    text "  • [companion]" size 13
            else:
                text "No companions" size 14 color "#888"
            
            null height 10
            
            if len(pilgrim.blessings) > 0:
                text "Blessings:" size 16
                for blessing in pilgrim.blessings:
                    text "  • [blessing]" size 13 color "#6f6"
            
            null height 20
            
            textbutton "Close" action Return()
