import json
import os

original_puzzle_info = {
    "moves" : 0,
    "seed" : 0,
    "matrix" : []
}

original_data = {
    "in_puzzle" : False,
    "level" : -1,
    "slide" : 999,
    "total_moves" : 0,
    "puzzle_info" : original_puzzle_info,
}

def load_pass():
    with open('./gamedata.json' , 'r') as jfile:
        jdata = json.load(jfile)
    return jdata["pass_tutorial"]

def load_prog():
    with open('./gamedata.json' , 'r') as jfile:
        jdata = json.load(jfile)
    return jdata["level"], jdata["slide"]

def load_info():
    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)
    return jdata["puzzle_info"]

def load_n_save(in_puzzle=None, level=None, slide=None, total_moves=None, moves=None, seed=None, matrix=None) -> None:
    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)
    if in_puzzle is not None:
        jdata["in_puzzle"] = in_puzzle
    if level is not None:
        jdata["level"] = level
    if slide is not None:
        jdata["slide"] = slide
    if total_moves is not None:
        jdata["total_moves"] += total_moves
    if moves is not None:
        jdata["puzzle_info"]["moves"] = moves
    if seed is not None:
        jdata["puzzle_info"]["seed"] = seed
    if matrix is not None:
        jdata["puzzle_info"]["matrix"] = matrix
    with open('./gamedata.json', 'w') as jfile:
        json.dump(jdata, jfile, indent=4)

def check_in_puzzle() -> None:
    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)
    return jdata["in_puzzle"]

def restart_game() -> None:
    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)
    temp = jdata["pass_tutorial"]
    jdata = original_data
    jdata["pass_tutorial"] = temp
    with open('./gamedata.json', 'w') as jfile:
        json.dump(jdata, jfile, indent=4)

def pass_tutorial() -> None:
    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)
    jdata["pass_tutorial"] = True
    with open('./gamedata.json', 'w') as jfile:
        json.dump(jdata, jfile, indent=4)

def create_game() -> None:
    jdata = original_data
    jdata["pass_tutorial"] = False
    with open('./gamedata.json', 'w') as jfile:
        json.dump(jdata, jfile, indent=4) 

def check_error() -> None:
    with open('./gamedata.json', 'r') as jfile:
        jdata = json.load(jfile)
    if (jdata["level"] == -1) and (jdata["puzzle_info"] != original_puzzle_info):
        restart_game()

if __name__ == '__main__':
    restart_game()
