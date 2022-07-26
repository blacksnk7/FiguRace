import pandas as pd
import json
import os
import csv
import uuid
from time import time

#Path for all the files
figurace_path = os.path.dirname(os.path.dirname(__file__))
files_json_path = os.path.join(figurace_path, "data", 'files_json')
files_csv_path = os.path.join(figurace_path, "data", 'files_csv')

config_file_path = os.path.join(files_json_path, 'config.json')
users_file_path = os.path.join(files_json_path, 'users.json')
scores_file_path = os.path.join(files_json_path, 'scores.json')

spotify_file_path = os.path.join(files_csv_path, 'updated_spotify.csv')
volcanoes_file_path = os.path.join(files_csv_path, 'updated_volcanoes.csv')
movies_file_path = os.path.join(files_csv_path, 'updated_mymoviedb.csv')
analisis_file_path = os.path.join(files_csv_path, 'round_analisis.csv')
#Base state for the game
state = {
    "config": {
        "time": 3000,
        "rounds": 5,
        "added_score": 10,
        "subs_score": 10,
        "levels": {
            "facil": 3,
            "medio": 2,
            "dificil": 1,
        },
        "volume": 1,
    },
    "game": {
        "volcanes" : [],
        "musica": [],
        "peliculas": [],
    },

    "current":{
        "start_time": 0,
        "rounds": 0,
        "right_choice": "",
        "score": 0,
        "analisis_list": [],
        "page": "-HOME-",
        "level": "facil",
        "csv": "volcanes",
        "user": ""
    },
    
    "users": {},
    "scores": [],
}


def load_files_data():
    """loads data from config, users, scores and csv files and stores it in the state"""
    load_config_data()
    load_users_data()
    load_scores_data()
    load_csv_data()

# -------CONFIG
def get_config_time():
    """gets the configurated time"""
    return int(state["config"]["time"])

def get_config_level():
    """gets the configurated level"""
    return state["config"]["levels"][state["current"]['level']]

def get_config_rounds():
    """gets the configurated rounds"""
    return int(state["config"]["rounds"])

def load_config_data():
    """tries to load the config data from the config json file and update the state"""
    try:
        with open(config_file_path) as config_file:
            state["config"].update(json.load(config_file))
    except:
        print('error loading config data')


def update_config_data(new_config):
    """updates the state config data with a new configuration"""
    state["config"]["time"] = new_config["-CONFIG_TIME-"]
    state["config"]["rounds"] = new_config["-CONFIG_ROUNDS-"]
    state["config"]["added_score"] = new_config["-CONFIG_ADDED_SCORE-"]
    state["config"]["subs_score"] = new_config["-CONFIG_SUBS_SCORE-"]
    state["config"]["levels"][new_config["-CONFIG_LEVEL_KEY-"]] = new_config["-CONFIG_LEVEL_VALUE-"]
    state["config"]["volume"] = float(new_config["-CONFIG_VOLUME-"]) / 100
    save_config_data()


def save_config_data():
    """saves the actual config state in a json file to last over time"""
    try:
        with open(config_file_path, 'w') as config_file:
            config_file.write(json.dumps(state["config"]))
    except:
        pass


# -------USERS
def load_users_data():
    """tries to load the users data from the users json file and update the state"""
    try:
        with open(users_file_path) as users_file:
            state["users"].update(json.load(users_file))
            if (len(state["users"]) > 0):
                state["current"]["user"] = list(state["users"].keys())[0]
    except:
        print('error loading users data')


def update_users_data(user_key, user_data):
    """updates the users config data with a new configuration"""
    state["users"][user_key] = user_data
    save_users_data()


def save_users_data():
    """saves the actual user state in a user file to last over time"""
    try:
        with open(users_file_path, 'w') as users_file:
            users_file.write(json.dumps(state["users"]))
    except:
        pass


# --------SCORES
def load_scores_data():
    """tries to load the scores data from the scores json file and update the state"""
    try:
        with open(scores_file_path) as scores_file:
            state["scores"].extend(json.load(scores_file))
    except:
        print("error loading scores data")

def update_scores():
    """updates the score data with a new score"""
    state["scores"].append({
        "user": get_cur_user(),
        "score": str(get_cur_score()),
        "level": get_cur_level()
    })
    save_scores()


def save_scores():
    """saves the actual scores state in a scores file to last over time"""
    try:
        with open(scores_file_path, 'w') as scores_file:
            scores_file.write(json.dumps(state["scores"]))
    except:
        pass

# --------------CSV
def load_csv_data():
    """tries to load the data from the csv files and update the state"""
    try:
        with open(spotify_file_path, 'r', encoding = 'utf-8') as spotify_file, open(volcanoes_file_path,'r', encoding = 'utf-8') as volcanoes_file, open(movies_file_path, 'r', encoding = 'utf-8') as movies_file:
            spotify_data = csv.reader(spotify_file, delimiter=',') 
            volcanoes_data = csv.reader(volcanoes_file, delimiter=',')
            movies_data = csv.reader(movies_file, delimiter=',')
            state["game"]["musica"] = list(spotify_data)
            state["game"]["volcanes"] = list(volcanoes_data)
            state["game"]["peliculas"] = list(movies_data)
    except Exception as e:
        print(str(e) + "error loading csv data")

def save_analisis_data():
    """
    This function adds new rows to our 'rounds.csv' file. If the file does not exist, then the function creates it with the information given. The data_list variable
    is a list containing the information for each new row, so the lenght of the list equals the ammount of new rows to add into the .csv file.
    """
    data_list = state["current"]["analisis_list"]
    try:
        data_set = pd.read_csv(analisis_file_path, sep=",", encoding='utf-8', on_bad_lines='skip')
        #series_temp = pd.Series(dicc.values())
        #data_set = pd.concat([data_set, data_set_temp], ignore_index=True)
    except FileNotFoundError:
        headers = ["timestamp", "id", "evento", "usuario", "genero", "estado", "texto ingresado", "respuesta", "nivel"]
        dict_temp = {}
        list_temp = [""]
        data_list_element = data_list.pop(0)
        counter = 0
        for key in headers:
            list_temp[0] = data_list_element[counter]
            dict_temp[key] = list_temp.copy()
            counter += 1
        data_set = pd.DataFrame.from_dict(dict_temp)
    for elem in data_list:
        data_set.loc[len(data_set.index)] = elem
    data_set.to_csv(analisis_file_path, index=False, encoding='utf-8')
# ----------CURRENT
# ANALISIS DATA
def add_analisis_row(type, texto=""):
    """adds a row to a temporary state and later that will be consumed to finally be stored in a csv file"""
    data_row = []
    
    data_row.append(time())                                #0 timestamp 
    data_row.append(uuid.uuid1().int)                      #1 id 
    data_row.append('')                                    #2 evento 
    data_row.append(get_cur_user())                        #3 usuario 
    data_row.append(get_cur_user_gender(data_row[3]))      #4 genero 
    data_row.append('')                                    #5 estado 
    data_row.append(texto )                                #6 texto 
    data_row.append('')                                    #7 respuesta 
    data_row.append(get_cur_level())                       #8 nivel 
    
    match type:
        case "start":
            data_row[2] = 'inicio_partida'
            data_row[5] = 'nueva'

        case "end":
            data_row[2] = 'fin'
            data_row[5] = 'finalizado'
        
        case "error":
            data_row[2] = 'intento'
            data_row[5] = 'error'
            data_row[7] = get_right_choice()
        
        case "ok":
            data_row[2] = 'intento'
            data_row[5] = 'ok'
            data_row[6] = get_right_choice()
            data_row[7] = get_right_choice()
        
        case "timeout":
            data_row[2] = 'intento'
            data_row[5] = 'timeout'
            data_row[7] = get_right_choice()
            
        case "cancel":
            data_row[2] = 'fin'
            data_row[5] = 'cancelada'
            
    state["current"]["analisis_list"].append(data_row)
            
def clear_analisis():
    state["current"]["analisis_list"] = []
    
# CSV
def get_cur_csv_data():
    """gets the data on current csv"""
    return state["game"][state["current"]["csv"]]

def get_cur_csv():
    """gets the current csv"""
    return state["current"]["csv"]

def set_current_csv(newcsv):
    """sets the dataset passed"""
    state["current"]["csv"] = newcsv

# USER
def get_cur_user():
    """gets the current user"""
    return state["current"]["user"]

def set_current_user(new_user):
    """sets the user passed"""
    state["current"]["user"] = new_user
    
def get_cur_user_gender(cur_user):
    """gets the current user's gender"""
    return state["users"][cur_user]["gender"]

# LEVEL
def get_cur_level():
    """gets the current level"""
    return state["current"]["level"]

def set_current_level(new_level):
    """sets the level passed"""
    state["current"]["level"] = new_level

# TIME
def get_current_time():
    """gets the current time"""
    return state["current"]["start_time"]
    
def set_current_time(new_time):
    """sets the time passed"""
    state["current"]["start_time"] = new_time
    
# RIGHT CHOICE
def get_right_choice():
    """gets the current choice in game"""
    return state["current"]["right_choice"]
    
def set_right_choice(new_right_choice):
    """sets the choice passed"""
    state["current"]["right_choice"] = new_right_choice

# ROUND
def get_cur_round():
    """gets the current rounds"""
    return int(state["current"]["rounds"])

def set_cur_round(rounds):
    """sets the rounds state to a new integer passed as parameter"""
    state["current"]["rounds"] = rounds

# SCORE
def get_cur_score():
    """gets the current score"""
    return int(state["current"]["score"])

def set_cur_score(score):
    """sets the scores state to a new integer passed as parameter"""
    state["current"]["score"] = str(score)

def calculate_score(choice):
    """Score calculation, multiplier applied depending on time passed and difficulty"""
    score = int(state["config"]["added_score"]) if choice == get_right_choice() else -1*int(state["config"]["subs_score"])
    #Calculo de score: (((Max tiempo + 2 - Tiempo actual)*Score max)/Max tiempo)*Mult dificultad
    #Se le suma 2 a max tiempo asi es realista conseguir el maximo de puntos
    #Ejemplo -> Max tiempo: 50seg, Tiempo actual: 2seg, Score max: 30, Dificultad: Fácil
    #El calculo seria: (((50seg - 2seg)*30)/50seg)*1 = 28 puntos
    score = round(get_config_time() + 2 - (time() - get_current_time()),1)*score/get_config_time()
    match get_cur_level():
        case "medio":
            score *= 1.5
        case "dificil":
            score *= 2
    return int(score)
# PAGES
def update_cur_page(new_page):
    """sets the current page state to a new page passed as parameter"""
    state["current"]["page"] = new_page


