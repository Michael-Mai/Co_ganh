import os
import random


cwd = os.getcwd()

player_file_list = os.listdir(os.path.join(cwd, "static/botfiles"))

load_rand_player = random.choice(player_file_list)