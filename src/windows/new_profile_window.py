import PySimpleGUI as sg
from src.common.helpers import check_positive_value
from src.common.components import Button
from src.windows.profile_window import updateLayout

def create_new_profile_page(users_is_zero):
    """Creates the Layout for the new profile page"""
    layout = [
        [sg.Text("Crear nuevo Usuario", font="Arial 20 underline", pad=((0, 0), (0, 20)))],
        [sg.Text("Nombre", size=(30, 1), font="Young 15"), sg.Input(
            size=(30, 1), key='-USER_KEY_NEW-', default_text="")],
        [sg.Text("Edad", size=(30, 1), font="Young 15"), sg.Input(
            size=(30, 1), key='-USER_AGE_NEW-', default_text=0)],
        [sg.Text("Genero autopercibido", size=(30, 1), font="Young 15"), sg.Combo(['Masculino', 'Femenino', 'No Binario'], default_value='No Binario', enable_events=True, key='-USER_GENDER_NEW-', size=(30, 1))],
        [Button("Aceptar", '-SAVE-', "sm"),
            sg.Push(),
            Button("Cancelar",'-EXIT-', "sm", visible = not users_is_zero)],
        [sg.pin(sg.Text('Error', font="Young 15", visible=False, key='-ERROR-'))]
    ]
    return layout


def new_profile_controller(model, window, event, values):
    """Controller for the new_profile page"""
    match event:
        case '-GO_TO--NEW_PROFILE-':
            if len(model.state['users'].keys()) == 0:
                window['-EXIT-'].update(visible = False)
            else:
                window['-EXIT-'].update(visible = True)
        case '-EXIT-':
            window.write_event_value('-GO_TO--PROFILE-', '-GO_TO--PROFILE-')
        case "-SAVE-":
            #We have to check if there is an input and if the input is not already on the json
            #With the .isspace() method we check that if there are only whitespace characters in the string and pop up the '-ERROR-'
            if (values['-USER_KEY_NEW-'] and not values['-USER_KEY_NEW-'].isspace()): 
                if (values['-USER_KEY_NEW-'] not in model.state["users"]):
                    user_data = {}
                    user_data['age'] = check_positive_value(values['-USER_AGE_NEW-'])
                    #We check if the age is an integer
                    if (user_data['age'] == 'error'):
                        window['-ERROR-'].update(visible=True, value='No pusiste un numero entero positivo en edad')
                    else:
                        user_data['gender'] = values['-USER_GENDER_NEW-']
                        model.update_users_data(values['-USER_KEY_NEW-'], user_data)
                        window['-USER_KEY-'].update(values=list(model.state['users'].keys()))
                        user_key = values['-USER_KEY_NEW-']
                        updateLayout(model, window, user_key)
                        #We go to the profile page if we come from that page, if not go to home (case of no users on launch)
                        if (model.state["current"]["page"] == '-HOME-'):
                            window.write_event_value('-GO_TO--HOME-', '-GO_TO--HOME-')
                        else:
                            window.write_event_value('-GO_TO--PROFILE-', '-GO_TO--PROFILE-')
                        #We update the current page to new_profile on the case we have this page on launch (-HOME- is the base state)
                        model.update_cur_page('-NEW_PROFILE-')
                        window['-ERROR-'].update(visible=True, value='')
                        window['-GO_TO--HOME-'].update(visible=True)
                        window.write_event_value('-USER_CREATE-', '-USER_CREATE-')
                else:
                    window['-ERROR-'].update(visible=True, value='El usuario Ya existe')
            else:
                window['-ERROR-'].update(visible=True, value='Debe colocarse al menos un caracter')
            model.load_users_data()