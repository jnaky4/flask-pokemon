import pandas as pd
from typing import Dict
from Models.PokemonModel import Pokemon
import os


def get_csv_route(filename):
    cwd = os.path.abspath(os.path.dirname(__file__))
    print(cwd)
    csv = os.path.join(cwd, '..', 'static', 'CSV', filename)
    return csv


types = ["Fire", "Water", "Grass", "Electric", "Ice", "Normal", "Bug", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Rock", "Ghost", "Dragon"]

pokemon_csv = get_csv_route('Pokemon.csv')
typing_csv = get_csv_route('Type.csv')

# explanation of csv reader
# https://www.delftstack.com/howto/python/python-csv-to-dictionary/
items = pd.read_csv(pokemon_csv, index_col=0, sep=",", encoding='cp1252')
types = pd.read_csv(typing_csv, index_col=0, sep=",", encoding='cp1252')
# items = pd.read_csv(pokemon_csv, index_col=0, sep=",")

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html?highlight=transpose#pandas.DataFrame.transpose
# transpose flips the keys to be row 0 instead of column 0
pokemon_csv_dict = items.transpose().to_dict(orient='series')
typing_csv_dict = types.transpose().to_dict(orient='series')
# print(typing_csv_dict)


def createPokemon(dexnum: int, pokemon_csv_dict: Dict) -> Pokemon:
    return Pokemon(
        dexnum=dexnum,
        name=pokemon_csv_dict[dexnum]['Pokemon_Name'],
        type1=pokemon_csv_dict[dexnum]['Type1'],
        type2=pokemon_csv_dict[dexnum]['Type2'] if pokemon_csv_dict[dexnum]['Type2'] != "-" else "None",
        stage=pokemon_csv_dict[dexnum]['Stage'],
        evolve_level=int(pokemon_csv_dict[dexnum]['Evolve_Level']),
        gender_ratio=pokemon_csv_dict[dexnum]['Gender_Ratio'],
        height=float(pokemon_csv_dict[dexnum]['Height']),
        weight=float(pokemon_csv_dict[dexnum]['Weight']),
        description=pokemon_csv_dict[dexnum]['Description'],
        category=pokemon_csv_dict[dexnum]['Category'],
        lvl_speed=float(pokemon_csv_dict[dexnum]['Leveling_Speed']),
        base_exp=int(pokemon_csv_dict[dexnum]['Base_Exp']),
        catch_rate=int(pokemon_csv_dict[dexnum]['Catch_Rate']),
    )


def get_all_pokemon_weakness_resistance(type1: str, type2: str) -> Dict:
    defending_type_dict = {
        0.0: [],
        0.25: [],
        0.5: [],
        1.0: [],
        2.0: [],
        4.0: []
    }

    for type in types:
        score1 = typing_csv_dict[type][type1]
        if type2 != "None":
            score2 = typing_csv_dict[type][type2]
            score1 = score1 * score2

        defending_type_dict[score1].append(type)

    # print(defending_type_dict)
    return defending_type_dict




