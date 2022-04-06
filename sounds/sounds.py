import requests
from playsound import playsound
import os
from multiprocessing.pool import Pool


def play_pokemon_sound(i):
    sound_path = os.path.join(os.getcwd(), "sound_files", f"{i}.mp3")
    playsound(sound_path)


def get_pokemon_sounds():

    sound_folder = os.path.join(os.getcwd(), "sound_files")
    if not os.path.isdir(sound_folder):
        os.mkdir(sound_folder)

    for i in range(1, 152):
        url = f"https://pokemoncries.com/cries-old/{i}.mp3"

        # print(f"getting pokemon {i}")
        response = requests.get(url)

        # writing sound to file current_directory/sound_files/{i}.mp3
        sound_path = os.path.join(sound_folder, f"{i}.mp3")

        open(sound_path, 'wb').write(response.content)


def get_a_pokemon_sound(url: str):
    """
    Goes to https://pokemoncries.com/cries-old/ [1-151].mp3
    and downloads to cwd/sound_files
    """

    # check if folder exists
    sound_folder = os.path.join(os.getcwd(), "sound_files")
    if not os.path.isdir(sound_folder):
        os.mkdir(sound_folder)

    # writing sound to file current_directory/sound_files/{i}.mp3

    # split url to get the mp3 file name
    split_url = url.split("/")
    sound_path = os.path.join(sound_folder, f"{split_url[-1]}")
    # print(sound_path)

    # if file exists, don't download it
    if not os.path.exists(sound_path):
        response = requests.get(url)
        open(sound_path, 'wb').write(response.content)


if __name__ == '__main__':

    # single threaded network - io bound process
    # get_pokemon_sounds()

    # for j in range(1, 152):
    #     play_pokemon_sound(j)

    # multiple threaded network - io bound process
    cpus = os.cpu_count()

    urls = []
    for j in range(1, 152):
        urls.append(f"https://pokemoncries.com/cries-old/{j}.mp3")

    with Pool(cpus) as pool:

        res = pool.map(get_a_pokemon_sound, urls)

