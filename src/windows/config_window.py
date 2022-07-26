import PySimpleGUI as sg

from src.data.music_player import M_Player
from src.common.helpers import check_positive_value
from src.common.components import Title, Text, Input, Combo, Button, Column, Slider
from threading import Timer

def create_config_page(config_data):
    """Creates the Layout for the config page"""
    levels = list(config_data["levels"].keys())

    col1 = Column([
        Text("Tiempo por ronda:", p=((0, 0), (20, 0))),
        Text("Puntaje sumado: "),
        Text("Puntaje restado: "),
        Text("Máxima cantidad de rondas: ", p=(4, 8)),
        Text("Volumen de Musica: ", p=(4, 14)),
        Text("Cantidad de características por nivel: "),
        Button("Guardar cambios", '-CONFIG_SAVE-'),
    ])
    
    col2 = Column([
        Slider((5, 200), '-CONFIG_TIME-', int(config_data["time"])),
        Input(config_data["added_score"], '-CONFIG_ADDED_SCORE-'),
        Input(config_data["subs_score"], key='-CONFIG_SUBS_SCORE-'),
        Slider(10, "-CONFIG_ROUNDS-", int(config_data["rounds"])),
        Slider(100, "-CONFIG_VOLUME-", int(config_data["volume"]*100), p=(4, 10)),
        Slider(5, '-CONFIG_LEVEL_VALUE-',  int(config_data["levels"]["facil"])),
        Combo(levels, '-CONFIG_LEVEL_KEY-', "sm"), 
    ])

    col3 = Column([sg.Column([[sg.Text('', font="Young 15", visible=True, key='-TEXT_INFO2-')]])])
    
    return [
        Title("Configuracion"),
        [col1, col2],
        [col3],
    ]


def config_controller(model, window, event, values, mp):
    """Controller for the config page"""

    def hide_text():
        """Sets to false the visibility of the information text"""
        window['-TEXT_INFO2-'].update(visible=False, value="")

    match event:
        #If there is a change on the key level, it updates the correspondant value
        case "-CONFIG_LEVEL_KEY-":
            level_key = values["-CONFIG_LEVEL_KEY-"]
            window["-CONFIG_LEVEL_VALUE-"].update(model.state["config"]["levels"][level_key])
        #It saves the config information
        case "-CONFIG_SAVE-":
            config_level_key = values["-CONFIG_LEVEL_KEY-"]

            #We assing on a dict, the key and the value of that key
            config = {key: check_positive_value(value) for key, value in values.items() 
                if "CONFIG" in key and "-CONFIG_LEVEL_KEY-" != key}
            mp.update_volume(float(values['-CONFIG_VOLUME-']) / 100)

            #We check if there are errors on the inputs so we don't update the json
            error_keys = [key for key, value in config.items() if 'error' == value]
            if (error_keys):
                for key in error_keys:
                    window[key].update('No se introdujo un numero positivo')
            else:
                window['-TEXT_INFO2-'].update(visible=True, value='Los cambios han sido guardado con exito')
                t = Timer(3, hide_text)
                t.start()
                config['-CONFIG_LEVEL_KEY-'] = config_level_key
                model.update_config_data(config)
