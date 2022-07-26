import PySimpleGUI as sg
import src.data.model as model

from src.data.music_player import M_Player
from src.windows.views import create_window
from src.windows.views import window_controller
from src.windows.home_window import home_page_controller 
from src.windows.play_window import play_page_controller
from src.windows.config_window import config_controller
from src.windows.scores_window import scores_controller
from src.windows.profile_window import profile_controller
from src.windows.new_profile_window import new_profile_controller


def main_menu():
    ''' 
    When called, this function will create the main menu for the FiguRace game. The file reading is handled by the model.py module, while the UI is created using the modules from
    the windows folder. The music meanwhile is handled by music_player.py. This function mainly calls the other modules in order to create the main menu of the game. 
    '''
    #We get the data from the files
    model.load_files_data()
    #Create window fullscreen
    window = create_window(model.state).Finalize()
    window.maximize()

    #Calls a function to start playin the music
    mp = M_Player(model.state["config"]["volume"])
    mp.play_menu_song()
    
    while True:
        event, values = window.read(timeout = 10)
        
        if event in (None, "Exit"):
            break   
        
        #We call all the controllers of mostly all the pages (play and csvselect not functional... yet)
        mp.music_controller(model, window, event, values)
        window_controller(model, window, event, values)
        home_page_controller(model, window, event, values)
        play_page_controller(model, window, event, values)
        config_controller(model, window, event, values, mp)
        scores_controller(model, window, event, values)
        profile_controller(model, window, event, values)
        new_profile_controller(model, window, event, values)
                
    #Calls a function to stop the music
    mp.end()
    window.close()
