## Screens for the Deck Builder CYOA

## Main Menu Screen ############################################################

screen main_menu():
    tag menu
    
    style_prefix "main_menu"
    
    add "gui/main_menu.png"
    
    frame:
        style_prefix "main_menu"
        
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10
            
            text "Magi: Deck Builder" size 50 xalign 0.5
            
            textbutton "New Game" action Start()
            textbutton "Continue" action ShowMenu("load")
            textbutton "Options" action ShowMenu("preferences")
            textbutton "About" action ShowMenu("about")
            textbutton "Quit" action Quit(confirm=True)


## Combat Screen ###############################################################

screen combat_ui():
    zorder 100
    
    # Top bar - Enemy info
    frame:
        xalign 0.5
        ypos 20
        xsize 600
        
        vbox:
            spacing 5
            text "[current_enemy.name]" size 30 xalign 0.5
            hbox:
                spacing 20
                xalign 0.5
                text "HP: [current_enemy.hp]/[current_enemy.max_hp]"
                if current_enemy.block > 0:
                    text "Block: [current_enemy.block]"
            text "Intent: [current_enemy.intent] ([current_enemy.attack_power] damage)" size 20 xalign 0.5
    
    # Player info
    frame:
        xpos 20
        ypos 20
        
        vbox:
            spacing 5
            text "[player.name]" size 25
            text "HP: [player.hp]/[player.max_hp]"
            if player.block > 0:
                text "Block: [player.block]"
            text "Energy: [player.energy]/[player.max_energy]"
            text "Draw: [len(player.deck.draw_pile)] | Discard: [len(player.deck.discard_pile)]"
    
    # End Turn button
    frame:
        xalign 1.0
        yalign 1.0
        xpos -20
        ypos -20
        
        textbutton "End Turn" action Return("end_turn")
    
    # Hand display
    frame:
        xalign 0.5
        yalign 0.95
        xsize 900
        
        hbox:
            spacing 10
            xalign 0.5
            
            for i, card in enumerate(player.deck.hand):
                button:
                    action Return(("play_card", i))
                    
                    frame:
                        xsize 150
                        ysize 200
                        
                        vbox:
                            spacing 5
                            text "[card.name]" size 18 xalign 0.5
                            text "Cost: [card.cost]" size 14
                            text "[card.card_type]" size 14
                            if card.power > 0:
                                text "Power: [card.power]" size 14
                            text "[card.description]" size 12


## Deck View Screen ############################################################

screen deck_view():
    tag menu
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        
        vbox:
            spacing 10
            
            text "Your Deck" size 40 xalign 0.5
            text "Total Cards: [player.deck.get_deck_size()]" xalign 0.5
            
            viewport:
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 5
                    
                    for card in player.deck.cards:
                        hbox:
                            spacing 20
                            text "[card.name]" size 20 min_width 150
                            text "[card.card_type]" size 16 min_width 100
                            text "Cost: [card.cost]" size 16 min_width 80
                            if card.power > 0:
                                text "Power: [card.power]" size 16
            
            textbutton "Close" action Return() xalign 0.5


## Reward Screen ###############################################################

screen reward_screen(cards_offered):
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 500
        
        vbox:
            spacing 20
            
            text "Choose a card to add to your deck" size 30 xalign 0.5
            
            hbox:
                spacing 30
                xalign 0.5
                
                for i, card in enumerate(cards_offered):
                    button:
                        action Return(i)
                        
                        frame:
                            xsize 200
                            ysize 280
                            
                            vbox:
                                spacing 8
                                text "[card.name]" size 22 xalign 0.5
                                text "Cost: [card.cost]" size 16
                                text "[card.card_type]" size 16
                                if card.power > 0:
                                    text "Power: [card.power]" size 16
                                text "[card.description]" size 14
            
            textbutton "Skip" action Return(-1) xalign 0.5


## Choice Screen ###############################################################

screen choice_screen(prompt, choices):
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 400
        
        vbox:
            spacing 20
            
            text "[prompt]" size 24 xalign 0.5
            
            vbox:
                spacing 15
                xalign 0.5
                
                for i, choice in enumerate(choices):
                    textbutton "[choice]" action Return(i) xsize 500


## Say Screen ##################################################################

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## GUI Variables ###############################################################

define gui.textbox_height = 185
define gui.textbox_yalign = 1.0

define gui.name_xpos = 240
define gui.name_ypos = 0
define gui.name_xalign = 0.0

define gui.namebox_width = None
define gui.namebox_height = None

define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False

define gui.dialogue_xpos = 268
define gui.dialogue_ypos = 50
define gui.dialogue_width = 744

define gui.dialogue_text_xalign = 0.0

init python:
    gui.text_properties = lambda x, accent=False: {}


## About screen ################################################################

screen about():
    tag menu

    frame:
        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################

screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))

screen file_slots(title):
    
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))
    
    frame:
        style_prefix "file_slots"
        
        vbox:
            
            hbox:
                textbutton _("Previous") action FilePagePrevious()
                textbutton _("Next") action FilePageNext()
            
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    
                    $ slot = i + 1
                    
                    button:
                        action FileAction(slot)
                        
                        has vbox
                        
                        text FileTime(slot, empty=_("Empty Slot")):
                            style "slot_time_text"
                        
                        text FileSaveName(slot):
                            style "slot_name_text"

define gui.file_slot_cols = 2
define gui.file_slot_rows = 4

style file_slots_frame is default
style slot_button is default
style slot_time_text is default
style slot_name_text is default


## Preferences screen ##########################################################

screen preferences():
    tag menu
    
    frame:
        style_prefix "preferences"
        
        vbox:
            
            label _("Preferences")
            
            hbox:
                box_wrap True
                
                vbox:
                    style_prefix "radio"
                    label _("Display")
                    textbutton _("Window") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")
                
                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                
                vbox:
                    style_prefix "slider"
                    
                    label _("Text Speed")
                    bar value Preference("text speed")
                    
                    label _("Auto-Forward Time")
                    bar value Preference("auto-forward time")
            
            textbutton _("Return") action Return()

style preferences_frame is default
style radio_label is default
style radio_button is default
style check_label is default
style check_button is default
style slider_label is default
style slider_slider is default


## GUI Styles ##################################################################

style default:
    font "DejaVuSans.ttf"
    size 22
    color "#fff"

style button:
    padding (5, 5, 5, 5)

style button_text:
    idle_color "#888"
    hover_color "#fff"
    selected_color "#fa0"

style frame:
    background Frame("gui/frame.png", 10, 10)
    padding (10, 10, 10, 10)

style main_menu_frame:
    background Frame("gui/overlay/main_menu.png", 10, 10)
    padding (20, 20, 20, 20)

style gui_label:
    size 30

style gui_label_text:
    size 30
    color "#fff"
