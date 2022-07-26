import PySimpleGUI as sg
import copy
from src.common.components import Title, Text
def prom(dict):
    """Returns the average score of a dictionary"""
    dict["score"] = int(int(dict["score"])/int(dict["cant"]))
    return dict

def make_score_best(scores):
    """Returns a list sorted (higher to lower) by score"""
    return sorted(scores, key=lambda i: int(i['score']), reverse=True)

def make_score_prom(scores):
    """Return a list sorted (higher to lower) by average score"""
    #We need to add at least one score to scores_data_prom so the for can run one time
    if scores:
        scores[0]["cant"] = 1
        scores_data_prom = [scores[0]]
        scores.pop(0)
    else:
        scores_data_prom = []
    #For every element in scores we search on scores_data_prom if it exist. If we found it we add the score and one to cant, if not, we add the dictionary instead
    for elem in scores:
        found = False
        for elem2 in scores_data_prom:
            if elem2["user"] == elem["user"] and elem2["level"] == elem["level"]:
                elem2["score"] = int(elem2["score"]) + int(elem["score"])
                elem2["cant"] += 1
                found = True
        if not found:
            elem["cant"] = 1
            scores_data_prom.append(elem)
    return make_score_best(list(map(prom, scores_data_prom)))

def create_scores_page(scores_data, config_data):
    """Creates the Layout for the score page"""
    levels = list(config_data["levels"].keys())
    #We have to do deepcopys of score_data so the state of model doesn't get changed
    scores_best = make_score_best(copy.deepcopy(scores_data))
    scores_prom = make_score_prom(copy.deepcopy(scores_data))
    primera_columna = sg.Column([
        [sg.Push(), sg.Text("Los mejores 20 puntajes", 
            font="Arial 20 underline", pad=((0, 0), (0, 20))), sg.Push()],
        [sg.Table(values=[[elem['user'], elem['score']] for elem in list(filter(lambda x: x['level'] == 'facil', scores_best))[:20]], headings=['Usuario', 'Puntaje'],
            col_widths=[33, 33], auto_size_columns=False,
            justification='left', num_rows=20, key='-TABLE-', hide_vertical_scroll=True, 
            background_color='#767575')]
    ])

    segunda_columna = sg.Column([
        [sg.Push(), sg.Text("Los mejores 20 usuarios (promedio)", 
            font="Arial 20 underline", pad=((0, 0), (0, 20))), sg.Push()],
        [sg.Table(values=[[elem['user'], elem['score']] for elem in list(filter(lambda x: x['level'] == 'facil', scores_prom))[:20]], headings=['Usuario', 'Puntaje Promedio'],
            col_widths=[33, 33], auto_size_columns=False,
            justification='left', num_rows=20, key='-TABLE2-', hide_vertical_scroll=True, 
            background_color='#767575')]
    ])

    return [
        Title("Puntajes"),
        [sg.Push(), Text("Elegir dificultad:", "lg"), sg.Column([
            [sg.Button(button_text=button.title(), key=f'-SHOW_{button.upper()}-', button_color='#06172e') if button == 'facil' else sg.Button(
            button_text=button.title(), key=f'-SHOW_{button.upper()}-') for button in levels]], pad = ((0,0),(5,10))),  sg.Push()],
        [primera_columna, segunda_columna]
    ]


def scores_controller(model, window, event, values):
    """Controller for the score page"""
    match event:
        case "-GO_TO--SCORE-":
            global scores_best
            global scores_prom
            scores_best = make_score_best(copy.deepcopy(model.state["scores"]))
            scores_prom = make_score_prom(copy.deepcopy(model.state["scores"]))
            window["-GO_TO--HOME-"].update(visible=True)
            window["-ICON_HOME-"].update(visible=True)
            #Facil score list will always be first when we enter the page
            window.write_event_value('-SHOW_FACIL-', '-SHOW_FACIL-')

        case _ if "-SHOW_" in event:
            #We store only the scores that are from the level indicated on the event (Key button)
            scores_best_show = list(filter(lambda x: x['level'] == f'{event.replace("-SHOW_", "").replace("-", "").lower()}', scores_best))
            scores_prom_show = list(filter(lambda x: x['level'] == f'{event.replace("-SHOW_", "").replace("-", "").lower()}', scores_prom)) 
            #Event cases for all the buttons
            cases = ["-SHOW_FACIL-", "-SHOW_MEDIO-", "-SHOW_DIFICIL-"]
            #We remove on cases the key from the button that called the event
            cases.remove(event)
            #We update the button that called the event
            window[event].update(button_color=('#FFFFFF', '#06172e'))
            #We update the others buttons using cases
            for elem in cases:
                window[elem].update(button_color=('#FFFFFF', '#283b5b'))
            #We update the tables
            window['-TABLE-'].update(values=[[elem['user'], elem['score']] for elem in scores_best_show[:20]])
            window['-TABLE2-'].update(values=[[elem['user'], elem['score']] for elem in scores_prom_show[:20]])
