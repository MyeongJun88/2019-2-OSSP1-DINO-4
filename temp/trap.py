import pygame
import random

from const import *

class trap(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        #창의 넓이,높이
        self.game=game
        self.width=WIDTH
        self.height=HEIGHT

        #fire image 불러옴
        self.image=pygame.image.load("tile/flame_frames.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(60,60))
        self.rect = self.image.get_rect()

        self.trap=pygame.image.load("tile/platform_tile_062.png")
        self.trap=pygame.transform.scale(self.trap,(100,30))
        self.saw_tooth=pygame.image.load("tile/platform_tile_072.png")
        self.saw_tooth=pygame.transform.scale(self.saw_tooth,(40,40))
        

    def trap_draw(self,screen,fire):
        self.rect.x=fire[0]
        self.rect.y=fire[1]
        fire[1]+=1.5
        
        hits=pygame.sprite.spritecollide(self,self.game.platforms,False)
 
        if hits:
            fire[0]=random.randrange(0,900)
            fire[1]=40
            screen.blit(self.image,(fire[0],fire[1]))
            
 
        else:
            if fire[1]>600:
                fire[0]=random.randrange(0,900)
                fire[1]=random.randrange(0,600)
                screen.blit(self.image,(fire[0],fire[1]))
    
            else:
                screen.blit(self.image,(fire[0],fire[1]))
            

        #screen.blit(self.saw_tooth,(700,260))