import pygame
import os

# loading animation while sorting
# import the picture from animation folder

path = "images/animation/"

pic_name = []

# animate_loading will be the item with 24 pictures use for the sort.py
animate_loading = []

for i in range(24):
    pic_name.append(str(i) + ".gif")

    temp = pygame.image.load(os.path.join(path, pic_name[i]))
    w = temp.get_width()
    h = temp.get_height()
    scale = 0.5
    temp = pygame.transform.scale(temp, (int(w * scale), int(h * scale)))
    animate_loading.append(temp)
