import PySimpleGUI as sg
from src.common.components import  Button, Text, Combo
import os

def create_home_page(game_data, config_data, user_names):
	"""Creates the Layout for the new profile page"""
	levels = list(config_data["levels"].keys())
	datasets = list(game_data.keys())

	first_column = sg.Column([
        [Button("Jugar", "-GO_TO--PLAY-", "lg") ],
        [Button("Configuracion", "-GO_TO--CONFIG-", "lg")],
        [Button("Puntaje", "-GO_TO--SCORE-", "lg")],
        [Button("Perfil", "-GO_TO--PROFILE-", "lg")]
        ],  p=(64, 0))
  
	second_column = sg.Column([
     	[
      		Text('Elegir dificultad: ', size="lg"),
   			Combo(levels, key="-SELECT_LEVEL-"),
		],
		[
      		Text('Elegir usuario:   ', size="lg"),
   			Combo(user_names, key="-SELECT_USER-"),
		],
         [
             Text("Elegir dataset:   ", size="lg"),
             Combo(datasets, key="-SELECT_CSV-"),
		 ]
        ])
	return [
     [sg.Push(), sg.Image(filename=os.path.join(os.getcwd(), 'src', 'data', 'img', 'Figurace.png'), pad=(0, 20)), sg.Push()],
      [first_column, second_column],
    ]

def home_page_controller(model, window, event, values):
	"""Controller for the home page"""
	users = list(model.state['users'].keys())
	match event:
		#Update users name combo when event on click INICIO button
		case "-GO_TO--HOME-":
			window["-SELECT_USER-"].update(value= model.get_cur_user(), values = users)
			window["-SELECT_CSV-"].update(value= model.get_cur_csv(), values = list(model.state["game"].keys()))
			window["-SELECT_LEVEL-"].update(value= model.get_cur_level(), values = list(model.state["config"]["levels"].keys()))

		case "-SELECT_LEVEL-":
			model.set_current_level(values['-SELECT_LEVEL-'])

		case "-SELECT_CSV-":
			model.set_current_csv(values['-SELECT_CSV-'])
   
		case "-SELECT_USER-":
			model.set_current_user(values['-SELECT_USER-'])
