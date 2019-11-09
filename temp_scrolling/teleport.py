import pygame

from camera import *

class teleport(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        #초기화
        self.game=game
        self.ready=False
        self.player_state=0
    
    #텔레포트 확인
    #한 class당 본인 sprite 하나라서 사용자 좌표 받아서 sprite 정함
    def sprite_def(self,game,player):
        #아래 빨간색
        if player.rect.x>=2500 and player.rect.x<=3000 and player.rect.y>=1100 and player.rect.y<=1500:
            self.image=pygame.image.load("tile/red_up.png").convert_alpha()
            self.image=pygame.transform.scale(self.image,(40,80))

            self.rect=self.image.get_rect()
            self.mask=pygame.mask.from_surface(self.image)

            self.rect.x=3000
            self.rect.y=1160

            self.ready=True
            self.player_state=1

        #위 빨간색
        if player.rect.x>=1390 and player.rect.x<=1700 and player.rect.y>=550 and player.rect.y<=600:
            self.image=pygame.image.load("tile/red_up.png").convert_alpha()
            self.image=pygame.transform.scale(self.image,(40,80))

            self.rect=self.image.get_rect()
            self.mask=pygame.mask.from_surface(self.image)

            self.rect.x=1560
            self.rect.y=560

            self.ready=True
            self.player_state=2


    def collide_detect(self,game):
        hits=pygame.sprite.spritecollide(self,game.player_sprite,False,pygame.sprite.collide_mask)

        if hits:
            #아래 빨간색으로 들어가면 위 빨간색으로 나옴
            if self.player_state is 1 and game.player.direction is "right":
                game.player.rect.x=1585
                game.player.rect.y=590
                game.player.direction="left"
            #위쪽 빨간색으로 들어가면 아래 빨간색으로 나옴
            if self.player_state is 2 and game.player.direction is "left":
                game.player.rect.x=2995
                game.player.rect.y=1190
                game.player.direction="right"
            
            
