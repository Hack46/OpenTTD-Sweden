#  lakes.py
#
#  Tweak the scale of heights to get some better look and feel, retaining
#  sea edges and fjäll.

import pygame
from random import randint

#screen = pygame.display.set_mode((640,480))
#pygame.display.set_caption('Eric Knut Halvardsson')

img = pygame.image.load('test_auto.png')
export = pygame.Surface((1024,2048), depth=32)
export.fill((0,0,0))

for y in range(0,2048):
  for x in range(0,909):
    pixel = img.get_at((x,y))
    if pixel[0] > 1:
      pixel[0] = int(1+pixel[0]*0.5)
      pixel[1] = int(1+pixel[1]*0.5)
      pixel[2] = int(1+pixel[2]*0.5)
      export.set_at((x,y),pixel)
    else:
      export.set_at((x,y),pixel)
    

pygame.image.save(export,'tweak1.png')
