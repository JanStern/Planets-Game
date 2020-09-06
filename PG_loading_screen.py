import time, os, pygame
from numpy.random import randint as rnd


# Graphics #########################################################################
_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\',os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path]=image
    return image 


# main #######################################################################
def main(l,h):
    l = int(9*l/10)
    h = int(9*h/10)
    screen = pygame.display.set_mode((l,h))

    screen.fill((200,200,200))
    font = pygame.font.SysFont('papyrus', l//7)
    text = font.render("PLANET", True, (0, 0, 0))
    screen.blit(text, (l//5-40,h//5))

    font = pygame.font.SysFont('papyrus', l//20)
    text = font.render("by J. Sternagel", True, (0, 0, 0))
    screen.blit(text, (l//3,h//2))

    pygame.display.flip()

    steps = 20
    for i in range(steps+1):
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,int(h-8), int(i*l/steps),8))
        pygame.display.flip()
        time.sleep(rnd(0,100)/500) #350

    pygame.display.flip()
    time.sleep(0.01)        
