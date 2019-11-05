import pygame

from const import *

#버튼이 눌렸는지 확인
class button_detect(pygame.sprite.Sprite):
    def __init__(self):
        #setting
        super().__init__()

        #image load
        self.image=pygame.image.load("background_image.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(3,3))

        #to detect collide
        self.rect = self.image.get_rect()
        self.rect.x=30
        self.rect.y=345

    def detect(self,screen,game):
        screen.blit(self.image,(self.rect.x,self.rect.y))

        hit=pygame.sprite.spritecollide(self,game.player_group,False)
        if hit:
            game.BUTTON_ON1=True

#버튼이 눌렸을 때 버튼 이미지를 바꿔줌
class button_image(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game=game

        #image load
        self.image=pygame.image.load("tile/platform_tile_038.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(30,30))

        self.rect=self.image.get_rect()

    def button_draw(self,screen):
       #버튼이 눌리지 않았다면, 눌리지 않은 버튼 이미지
        if self.game.BUTTON_ON1==False:
            self.image=pygame.image.load("tile/platform_tile_038.png").convert_alpha()
            self.image=pygame.transform.scale(self.image,(30,30))
        #버튼이 눌렸다면,눌린 버튼 이미지
        else:
            self.image=pygame.image.load("tile/platform_tile_038.png").convert_alpha()
            self.image=pygame.transform.scale(self.image,(30,10))
        
        self.rect=self.image.get_rect()

        if self.game.BUTTON_ON1==False:
            self.rect.x=10
            self.rect.y=350
            screen.blit(self.image,(self.rect.x,self.rect.y))
        else:
            self.rect.x=10
            self.rect.y=370
            screen.blit(self.image,(self.rect.x,self.rect.y))