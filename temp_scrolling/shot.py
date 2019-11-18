import pygame

from player import *

def RelRect(x,y,w,h,camera):
    return pygame.Rect(x-camera.rect.x, y-camera.rect.y, w, h)

class shot(pygame.sprite.Sprite):
    def __init__(self,game):
        #setting
        super().__init__()

        self.game=game

        #image load
        self.shot_image=pygame.image.load("bullet.png").convert_alpha()
        self.shot_image=pygame.transform.scale(self.shot_image,(30,30))

        #ready : 준비됨
        #fire : 불 쏘고 있는 상태(준비 안됨)
        self.bullet_state="ready"

        #충돌검사 위해
        self.rect=self.shot_image.get_rect()
        self.mask=pygame.mask.from_surface(self.shot_image)

    #총 좌표 초기화
    def shooting_setting(self,x,y):
        if self.game.ex_left==True:
            self.shot_image=pygame.image.load("bullet.png").convert_alpha()
            self.shot_image=pygame.transform.scale(self.shot_image,(30,30))
            self.shot_image=pygame.transform.flip(self.shot_image,True,False)
            self.rect.x=x
            self.rect.y=y
            self.speed=-8
            self.mask=pygame.mask.from_surface(self.shot_image)
        else:
            self.shot_image=pygame.image.load("bullet.png").convert_alpha()
            self.shot_image=pygame.transform.scale(self.shot_image,(30,30))
            self.rect.x=x
            self.rect.y=y
            self.speed=8
            self.mask=pygame.mask.from_surface(self.shot_image)

        self.bullet_state="fire"
        if self.game.ex_left:
            self.rect.x=x-50
            self.rect.y=y
        else:
            self.rect.x=x
            self.rect.y=y

    #총알 날라감
    def shooting(self):
        hits=pygame.sprite.spritecollide(self,self.game.world,False)

        #총알 벽에 부딪히면 없어짐
        if hits:
            self.bullet_state="ready"
        else:
            #총알 창 밖으로 나가면 초기화
            if self.rect.x>=3000 or self.rect.x<0:
                self.bullet_state="ready"
            #총알 날림
            if self.bullet_state is "fire":
                self.game.screen.blit(self.shot_image,RelRect(self.rect.x,self.rect.y,30,30,self.game.camera))
                self.rect.x+=self.speed

"""  
    def shoot_dino(self,game):
        hit_dino=pygame.sprite.spritecollide(self,self.game.dino_group,False,pygame.sprite.collide_mask)

        if hit_dino:
            self.bullet_state="ready"
            game.DINO_alive=False
"""