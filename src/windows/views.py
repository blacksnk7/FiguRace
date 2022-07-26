from turtle import color
import PySimpleGUI as sg

from src.windows.config_window import create_config_page
from src.windows.scores_window import create_scores_page
from src.windows.profile_window import create_profile_page
from src.windows.new_profile_window import create_new_profile_page
from src.windows.play_window import create_play_page
from src.windows.home_window import create_home_page
import src.data.icons as icons

def create_window(state):
    '''We create the base window, with all the pages loaded, but only the active one is visible to the user'''
    
    #Theme Manager
    sg.LOOK_AND_FEEL_TABLE['Figurace'] = {
        'BACKGROUND': '#355070',
        'TEXT': '#EAAC8B',
        'INPUT': '#EAAC8B',
        'SCROLL': '#EAAC8B',
        'TEXT_INPUT': '#355070',
        'BUTTON': ('#355070', '#EAAC8B'),
        'PROGRESS': ('#FFFFFF', '#FFFFFF'),
        'BORDER': 0, 'SLIDER_DEPTH': 0, 
        'PROGRESS_DEPTH': 0,
    }
    sg.theme('Figurace')
    
    game_data = state["game"]
    config_data = state["config"]
    users_data = state["users"]
    scores_data = state["scores"]

    user_names = list(users_data.keys()) if list(users_data.keys()) else ['NO USERS']
    users_is_zero = user_names == ['NO USERS']

    pages = {
        "-HOME-": create_home_page(game_data, config_data, user_names),
        "-PLAY-": create_play_page(user_names, config_data, game_data),
        "-CONFIG-": create_config_page(config_data),
        "-SCORE-": create_scores_page(scores_data, config_data),
        "-PROFILE-": create_profile_page(users_data, user_names),
        "-NEW_PROFILE-": create_new_profile_page(users_is_zero)
    }
    
    #We need to check if we have users in the json, so we can use the new_profile page as the first page, if not use the home page
    pagesLayout = [sg.Column(page, 
    visible = (page_key == "-HOME-" and not users_is_zero) or (page_key == '-NEW_PROFILE-' and users_is_zero), key=page_key) 
    for page_key, page in pages.items()]
    
    #All pages have the INICIO and EXIT button
    #Inicio button NOT visible if we have no users, we obligate the user to create atleast one user
    navbar=[
        sg.pin(sg.Button(image_data=icons.home, key="-GO_TO--HOME-", visible= not users_is_zero)),
        sg.pin(sg.Button(image_data=icons.mute,key="-MUTE-")),
        sg.pin(sg.Button(image_data=icons.unmute,key="-UN_MUTE-")),
        sg.pin(sg.Button(image_data=icons.exit ,key="Exit")),
        ]
    
    music_titles = [sg.pin(sg.Text("Inicio", key="-ICON_HOME-", visible= not users_is_zero)), sg.pin(sg.Text("Mutear")), sg.pin(sg.Text("Desmutear")), sg.pin(sg.Text("Salir"))]
    
    layout = [
        navbar,
        music_titles,
        [sg.VPush()],
        pagesLayout,
        [sg.VPush()]
    ]

    return sg.Window("Figurace", layout, element_justification='c', resizable=True)

def window_controller(model, window, event, values):
    """Controller for general issues on all windows"""
    if '-GO_TO-' in event:
        window[model.state["current"]["page"]].update(visible=False)
        model.update_cur_page(event[7:])  #We update the new page
        window[model.state["current"]["page"]].update(visible=True)