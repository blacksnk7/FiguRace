import PySimpleGUI as sg
from src.common.helpers import check_integer
from src.common.components import Title, Text, Input, Combo, Button, Column
from threading import Timer

def create_profile_page(users_data, user_names):
    """Creates the Layout for the profile page"""
    #Check if users_data has any users, so the profile can use a default, if not use the most added user
    act_user = user_names[0]
    if act_user == 'NO USERS':
        users_data = {'NO USERS': {'age': 'NO DATA', 'gender': 'NO DATA'}}
        
    col1 = Column([Text("Nombre de Usuario: "), Text("Edad: "), Text("Genero autopercibido: ")])
    
    col2 = Column([
        Combo(user_names, "-USER_KEY-"), 
        Input(users_data[act_user]['age'], "-USER_AGE-"), 
        Combo(['Masculino', 'Femenino', 'No Binario'], "-USER_GENDER-", default_value=users_data[act_user]["gender"])], "right", pad=((60, 60),(0, 50)))
    
    col3 = Column([Button("Crear nuevo usuario", '-GO_TO--NEW_PROFILE-'), Button("Borrar usuario", '-USER_DELETE-')])

    col4 = Column([Button("Guardar cambios", '-USER_SAVE-')],"right")

    col5 = Column([sg.Column([[sg.Text('', font="Young 15", visible=True, key='-TEXT_INFO-')]])])
    
    return [
        Title("Usuarios"),
        [col1, col2],
        [col3, col4],
        [col5],
    ]

def updateLayout(model, window, user_key):
    """Updates the inputs and combo so it stays connected to the actual data"""
    window['-USER_KEY-'].update(user_key)
    window['-USER_GENDER-'].update(value=model.state["users"][user_key]['gender'])
    window['-USER_AGE-'].update(model.state["users"][user_key]['age'])


def profile_controller(model, window, event, values):
    """Controller for the profile page"""

    def hide_text():
        """Sets to false the visibility of the information text"""
        window['-TEXT_INFO-'].update(visible=False, value="")
        
    def delete_usr():
        users_data = model.state["users"]
        remove = values['-USER_KEY-']
        #Removes the selected user
        del users_data[remove]
        model.state["users"] = users_data
        model.save_users_data()
        model.load_users_data()
        window['-TEXT_INFO-'].update(visible=True, value='El usuario ha sido eliminado con exito')
        t = Timer(3, hide_text)
        t.start()
        #We update the json and layout to the actual data if we have atleast one user, if not we go to new_profile
        if len(model.state['users'].keys()) > 0: 
            first_user = list(model.state['users'].keys())[0]
            window['-USER_KEY-'].update(first_user,values=list(model.state['users'].keys()))
            updateLayout(model, window, first_user)
        else:
            window['-GO_TO--HOME-'].update(visible=False)
            window['-ICON_HOME-'].update(visible=False)
            window.write_event_value('-GO_TO--NEW_PROFILE-', '-GO_TO--NEW_PROFILE-')
            
    def save_usr():
        #We update the the users json state, and pass it to model
        users_data = model.state["users"]
        user_data = {}
        user_data['age'] = check_integer(values['-USER_AGE-'])
        if (user_data['age'] == 'error'):
            window['-USER_AGE-'].update('No pusiste un numero')
        else:
            window['-TEXT_INFO-'].update(visible=True, value='Los cambios han sido guardado con exito')
            t = Timer(3, hide_text)
            t.start()
            user_data['gender'] = values['-USER_GENDER-']
            model.update_users_data(values['-USER_KEY-'], user_data)
        model.load_users_data()
    
    match event:
        case "-USER_KEY-":
            user_key = values['-USER_KEY-']
            updateLayout(model, window, user_key)

        case "-USER_SAVE-":
            popup = sg.popup_ok_cancel(f'Esta segura/o que desea actualizar los datos del usuario {values["-USER_KEY-"]}?')
            if (popup == 'OK'):
                save_usr()

        case "-USER_DELETE-":
            #{values["-USER_KEY-"]}
            popup = sg.popup_ok_cancel(f'Esta segura/o que desea borrar el usuario {values["-USER_KEY-"]}?')
            if (popup == 'OK'):
                delete_usr()

        case "-USER_CREATE-":
            window['-TEXT_INFO-'].update(visible=True, value='El perfil ha sido creado con exito')
            t = Timer(3, hide_text)
            t.start()