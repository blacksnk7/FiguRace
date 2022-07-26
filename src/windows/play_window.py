import PySimpleGUI as sg
import random
from threading import Timer
from time import time
from src.common.components import Text, Button, Column

def create_play_page(user_names, config_data, game_data):
    """Creates the Layout for the play page"""
    
    first_column = Column([
        [Text("Dataset: ") , Text(key = '-DATASET-')],
        [Text("Puntaje Actual: "), Text(key='-GAME_SCORE-')], 
        [Text("Usuario actual: "), Text(key = '-USER-')], 
        [sg.Column([
            [Text(f"{i+1}- ", f"-ROUND_{i}-", "sm")] for i in range(0,10)
        ])],
        [Button('Abandonar el Juego', "-GAME_RESIGN-")]
    ])
    
    second_column = Column([
        [Text("Nivel: ") , Text(key='-LEVEL-')], 
        [Text("Tiempo: " ), Text(" 3000", '-GAME_TIME-')], 
        [sg.Column([
             [Text("CARAC0" ,f'-CARAC_{i}-', "sm",  width=(25, None))] for i in range(5)
        ])], 
        [sg.Column([
            [Button("choice", f'-CHOICE_{i}-', "sm")] for i in range(5)
        ])]
    ])

    return [
    	[first_column, second_column]
    ]

def play_page_controller(model, window, event, values):
    """Controller for the play page"""
    
    def handle_choice(choice_key):
        choice_value = window[choice_key].get_text()

        if choice_value == model.get_right_choice():
            model.add_analisis_row("ok")
            window[f"-ROUND_{model.get_cur_round()-1}-"].update(f"{model.get_cur_round()}- Correcto ✓")
            window[choice_key].update(button_color=('white', 'green'))
        else:
            model.add_analisis_row("error", choice_value)
            window[f"-ROUND_{model.get_cur_round()-1}-"].update(f"{model.get_cur_round()}- Incorrecto X")
            window[choice_key].update(button_color=('white', 'red'))
        #Set new score
        model.set_cur_score(model.get_cur_score() + model.calculate_score(choice_value))
        window["-GAME_SCORE-"].update(model.get_cur_score())
    def play_next():
        window.write_event_value('-PLAY_NEXT-', '-PLAY_NEXT-')
    def return_home():
        model.set_current_time(0)
        model.clear_analisis()
    def resign():
        model.add_analisis_row("cancel")
        model.save_analisis_data()
        model.set_current_time(0)
        window.write_event_value('-GO_TO--SCORE-', '-GO_TO--SCORE-')
        
    match event:
        case "-GO_TO--PLAY-":
            window["-GO_TO--HOME-"].update(visible=False)
            window["-ICON_HOME-"].update(visible=False)
            #Initialize round and score
            model.set_cur_round(0)
            model.set_cur_score(0)
            window["-GAME_SCORE-"].update(0)
            #Show rounds depending on config and resets them to " "
            for i in range(10):
                window[f'-ROUND_{i}-'].update(f"{i+1}-", visible=False)
            cant_rondas = int(model.state["config"]["rounds"])
            for i in range(cant_rondas):
                window[f'-ROUND_{i}-'].update(visible=True)
                
            #Update depending on dificulty, user and csv
            window['-DATASET-'].update(model.state["current"]["csv"].title())
            window['-LEVEL-'].update(model.state["current"]["level"].title())
            window['-USER-'].update(model.state["current"]["user"])
            
            model.set_current_time(time())
            model.add_analisis_row("start")
            window.write_event_value('-PLAY_NEXT-', '-PLAY_NEXT-')


        case "-PLAY_NEXT-":
            #We need to check if we completed all the rounds
            rounds = model.get_cur_round()
            if (rounds == model.get_config_rounds()):
                model.add_analisis_row("end")
                model.save_analisis_data()

                #We update the score list in state and dump the info to the json file
                model.update_scores()
                window.write_event_value('-GO_TO--SCORE-', '-GO_TO--SCORE-')
            #Make buttons work
            for i in range(5):
                window[f'-CHOICE_{i}-'].update(disabled = False) 

            csv_data = model.get_cur_csv_data()
            header = csv_data[0]

            ran_choices = []
            right_choice = random.choice(csv_data)
            ran_choices.append(right_choice)
            
            #Random choices to pick from (CHECKING COPIES!)
            model.set_right_choice(right_choice[5])
            right_index = random.randrange(5)
            for i in range(5):
                window[f'-CHOICE_{i}-'].update(button_color=('white', 'RoyalBlue3'))
                if (i == right_index):
                    window[f'-CHOICE_{i}-'].update(model.get_right_choice())
                else:
                    ran_choice = random.choice(csv_data)[5]
                    while (ran_choice in ran_choices):
                        ran_choice = random.choice(csv_data)[5]
                    ran_choices.append(ran_choice)
                    window[f'-CHOICE_{i}-'].update(ran_choice)
                    
            #Show caracteristics depending on config level
            cant_carac = int(model.get_config_level())
            for i in range(4, cant_carac-1, -1):
                window[f'-CARAC_{i}-'].update(visible=False)
            for i in range(cant_carac):
                window[f'-CARAC_{i}-'].update(f"{header[i].title()}: {right_choice[i] if right_choice[i] else False}", visible=True)
            #Add one to rounds
            model.set_current_time(time()) 
            model.set_cur_round(rounds+1)

        #If the game is canceled, we need to clear the values   
        case "-GO_TO--HOME-":
            return_home()

        case "-GAME_RESIGN-":
            current_time = model.get_current_time()
            global_time = time()
            popup = sg.popup_ok_cancel(f'Esta segura/o que desea finalizar la partida?')
            if (popup == 'OK'):
                resign()
            else:
                model.set_current_time(time() - (global_time - current_time))
                print(model.get_current_time())

        case _ if '-CHOICE_' in event:
            handle_choice(event)
            for i in range(5):
                window[f'-CHOICE_{i}-'].update(disabled = True)    
            t = Timer(1, play_next)
            t.start()
            
        case _ if (model.get_current_time() != 0):
            elapsed_time = round(model.get_config_time() - (time() - model.get_current_time()), 1)
            
            if (elapsed_time >= 0):
                window['-GAME_TIME-'].update(f"{elapsed_time}s")
            else:
                window[f"-ROUND_{model.get_cur_round()-1}-"].update(f"{model.get_cur_round()}- Se acabo el Tiempo -")
                model.add_analisis_row("timeout")
                model.set_current_time(0)
                for i in range(5):
                    window[f'-CHOICE_{i}-'].update(disabled = True) 
                t = Timer(1, play_next)
                t.start()
        
            
            
        
            
            