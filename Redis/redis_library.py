import redis
import pandas as pd
import os
from Docker.docker_library import auto_start_container
# import Database.database
import json
import pickle


def create_redis():
    cwd = os.getcwd()
    pokemon_csv = os.path.join(cwd, "..", 'CSV', "Pokemon.csv")
    base_stats_csv = os.path.join(cwd, "..", 'CSV', "Base_Stats.csv")
    routes_csv = os.path.join(cwd, "..", 'CSV', "Routes.csv")

    # explanation of csv reader
    # https://www.delftstack.com/howto/python/python-csv-to-dictionary/
    pokedex_items = pd.read_csv(pokemon_csv, index_col=0, sep=",", encoding='cp1252')
    base_stats_items = pd.read_csv(base_stats_csv, index_col=0, sep=",", encoding='cp1252')
    route_item = pd.read_csv(routes_csv, index_col=0, sep=",", encoding='cp1252')
    # items = pd.read_csv(pokemon_csv, index_col=0, sep=",")

    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html?highlight=transpose#pandas.DataFrame.transpose
    # transpose flips the keys to be row 0 instead of column 0
    pokemon_csv_dict = pokedex_items.transpose().to_dict(orient='series')
    base_stats_dict = base_stats_items.transpose().to_dict(orient='series')

    auto_start_container("redis", "pokemon-redis")

    r = redis.Redis()
    for i in range(1, 152):
        # json_object = json.dumps(dictionary, indent=4)
        r.set(str(i), pickle.dumps(pokemon_csv_dict[i]))

    print("redis started")


def get_pokemon(dexnum: int):
    r = redis.Redis()
    value = r.get(str(dexnum))
    if not value:
        return None
    else:
        return pickle.loads(value)

def remove_pokemon(dexnum: int):
    r = redis.Redis()
    r.delete(str(dexnum))


if __name__ == "__main__":
    create_redis()
    print(get_pokemon(1))
    remove_pokemon(1)

