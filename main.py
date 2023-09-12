import os
import random
import math
import pygame
from os import listdir
from os.path import isfile , join

pygame.init()
pygame.display.set_caption("platformer game")

#global variables
WIDTH , HIGHT = 1000 , 600
FBS= 60
player_vel= 5

#game window

window= pygame.display.set_mode((WIDTH,HIGHT))


#adding & loading spritesheets

def flipSprites(sprites):
    return [pygame.transform.flip(sprite,True,False)for sprite in sprites]

def loadSpritesheets(dir1 , dir2 , width , hight , direction=False):
    path =join("assets" ,dir1,dir2)
    images=[f for f in listdir(path) if isfile(join(path,f))]
    
    all_sprites={}
    
    for image in images:
        spriteSheet = pygame.image.load(join(path,image)).convert_alpha()
        
        sprites=[]
        for i in range(spriteSheet.get_width()//width):
            surface = pygame.Surface((width,hight),pygame.SRCALPHA,32)
            rect = pygame.Rect(i*width,0,width,hight)                  #this block of code to make the spritesheet moving frame by frame
            surface.blit(spriteSheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace(".png","")+"_right"]=sprites    
            all_sprites[image.replace(".png","")+"_left"]=flipSprites(sprites)
        else:
            all_sprites[image.replace(".png","")]=sprites
            
    return all_sprites 

def getBlock(size):
    path=join("assets","terrain","terrain.png")
    image=pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect=pygame.Rect(96,0,size,size)
    surface.blit(image,(0,0),rect)
    
    return pygame.transform.scale2x(surface)   

class enemy(pygame.sprite.Sprite):
    enmySprite=loadSpritesheets("enemies","Bee",32,32,True)
    gravity=2
    
    def __init__(self, x, y, width,hight,player):
        super().__init__()
        self.player=player
        self.rect =pygame.Rect(x,y,width,hight)
        self.speed=3
        self.mask=None
        self.direction="right"
        self.animation_count=0
        self.fall_count=0
        
        self.rect.x = 400
        self.rect.y = 40
  
        self.change_x = 0
        self.change_y = 0
        
    def draw(self,win):
        self.sprite=self.enmySprite["Idle_"+ self.direction][0]
        win.blit(self.sprite,(self.rect.x,self.rect.y))
        
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y
        
    # def updateSprite(self):

            
    #     sprite_sheet_name=sprite_sheet+"_"+self.direction
    #     sprite=self.SPRITES[sprite_sheet_name]
    #     sprite_index=(self.animationCount//self.ANIMARION_DELAY)% len(sprite)
    #     self.sprite=sprite[sprite_index]
    #     self.animationCount +=1
    #     self.update()
  
  #to make the enemy chase the player

  
  
    # def update(self,fps):
    #     if self.player.rect.x > self.rect.x :
    #         self.rect.x += 1
    #     if self.player.rect.x < self.rect.x :
    #         self.rect.x -= 1
    #     if self.player.rect.y > self.rect.y :
    #         self.rect.y += 1
    #     if self.player.rect.y < self.rect.y :
    #         self.rect.y -= 1
    #     # self.updateSprite()
    
def enemy_move_to_player(enemy, Player):
    dirvect = pygame.math.Vector2(Player.rect.x - enemy.rect.x,
    Player.rect.y - enemy.rect.y)
    dirvect.scale_to_length(2) 
    enemy.rect.move_ip(dirvect) 

#creating the player

class player(pygame.sprite.Sprite):
    GRAVITY=10
    SPRITES =loadSpritesheets("MainCharacters","NinjaFrog",32,32,True)
    ANIMARION_DELAY=2
    
    def __init__(self, x , y , width , hight):
        super().__init__()
        self.rect = pygame.Rect(x , y , width , hight)
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        self.direction="left"
        self.animationCount=0
        self.fallCount=0
        self.jumping=0
        
    def jump(self):
        self.y_vel= -self.GRAVITY*2
        self.animationCount=0
        self.jumping +=1
        if self.jumping ==1:
            self.fallCount=0
        
    def move(self,dx,dy):
        self.rect.x +=dx    
        self.rect.y +=dy
        
    def moveToLeft(self,vel):
        self.x_vel= -vel
        if self.direction != "left" :
            self.direction = "left"
            self.animationCount=0      
            
    def moveToRight(self,vel):
        self.x_vel= vel
        if self.direction != "right" :
            self.direction = "right"
            self.animationCount=0   
            
    def landed(self):
        self.fallCount=0
        self.y_vel=0
        self.jumping=0
                    
    def hitHead(self):
        self.Count=0
        self.y_vel *= -1
         
   
    def loop(self, fps):
        self.y_vel += min(1, (self.fallCount / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fallCount +=1
        self.updateSprite()
        
        
    #for animation
    def updateSprite(self):
        sprite_sheet="idle"
        if self.y_vel <0:
            if self.jumping ==1:
                sprite_sheet="jump"
            elif self.jumping ==2:
                sprite_sheet="double_jump"
        elif self.y_vel > self.GRAVITY*1:
            sprite_sheet="fall"
        elif self.x_vel != 0:
            sprite_sheet="run"
            
        sprite_sheet_name=sprite_sheet+"_"+self.direction
        sprite=self.SPRITES[sprite_sheet_name]
        sprite_index=(self.animationCount//self.ANIMARION_DELAY)% len(sprite)
        self.sprite=sprite[sprite_index]
        self.animationCount +=1
        self.Update()
        
    def Update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
           
    def Draw(self,win ,offsetx):
        win.blit(self.sprite,(self.rect.x - offsetx,self.rect.y))
        
        
    
#for blocks
class object(pygame.sprite.Sprite):
    def __init__(self, x , y , width , hight ,name =None):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,hight)
        self.image = pygame.Surface((width,hight),pygame.SRCALPHA)
        self.width=width
        self.hight=hight
        self.name=name
    def draw(self,win,offsetx):
        win.blit(self.image,(self.rect.x - offsetx,self.rect.y))
        
class BlockObject(object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size , size)
        block=getBlock(size)
        self.image.blit(block,(0,0))
        self.mask=pygame.mask.from_surface(self.image)
        

            
            
#generating BG

def got_background(name):
    imge=pygame.image.load(join("assets","Background",name))
    _,_, width ,hight = imge.get_rect()
    tiles=[]
    
    for i in range(WIDTH // width +1):
        for j in range(HIGHT // hight +1):
            pos=(i*width , j*hight)
            tiles.append(pos)
            
    return tiles,imge           

#all this code to draw BG from left to right

def draw_BG(window , background , bg_img , p1 , objects,offsetx,e1):
    for tile in background:
        window.blit(bg_img,tile)
        
    for obj in objects:
        obj.draw(window,offsetx)
       
    e1.draw(window)
    p1.Draw(window,offsetx) 
    pygame.display.update()
    
#for vertical collition
def verCollition(p1,objects,dy):
    collided_objects=[]
    for obj in objects:
        if pygame.sprite.collide_mask(p1,obj):
            if dy >0:
                p1.rect.bottom = obj.rect.top
                p1.landed()
            elif dy < 0:
                p1.rect.top = obj.rect.bottom
                p1.hitHead()
                
        collided_objects.append(obj)
    return collided_objects
    
    
#collider check

def collide(p1,objects,dx):
    p1.move(dx,0)
    p1.update()
    collideObject=None
    for obj in objects:
        if pygame.sprite.collide_mask(p1 , obj):
            collideObject = obj
            break
        
    p1.move(-dx,0)
    p1.update()
    return collideObject    
    
    
#player movment
def Moving(p1,objects):
    keys = pygame.key.get_pressed()
    
    collideLeft = collide(p1 , objects , -player_vel*2)
    collideRight = collide(p1 , objects , player_vel*2)
        
    p1.x_vel=0
    if keys[pygame.K_LEFT] and not collideLeft:
            p1.moveToLeft(player_vel)   
    if keys[pygame.K_RIGHT] and not collideRight:
            p1.moveToRight(player_vel)
            
    verCollition(p1,objects,p1.y_vel)
                


def main(window):
    clock= pygame.time.Clock()
    background ,bg_img =got_background("Yellow.png")
    run = True
    p1= player(50,50,50,50)
    e1=enemy(150,150,100,100,p1)
    blockSize=96
    floor = [BlockObject(i* blockSize,HIGHT-blockSize,blockSize)for i in range(-WIDTH//blockSize,(WIDTH*2)//blockSize)]
    objects =[*floor, BlockObject(0, HIGHT - blockSize * 2, blockSize),
               BlockObject(blockSize * 3, HIGHT - blockSize * 4, blockSize)]
    offsetx=0
    scrollWidth=200
    
    
    while run:
        clock.tick(FBS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                break
            
            if event.type== pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and p1.jumping < 2:
                    p1.jump()
        
        
        enemy_move_to_player(e1,p1)
        p1.loop(FBS)
        draw_BG(window,background,bg_img ,p1, objects ,offsetx,e1 )
        Moving(p1 , objects)    
        
        if ((p1.rect.right- offsetx >= WIDTH-scrollWidth)and p1.x_vel > 0) or ((p1.rect.left- offsetx <= scrollWidth)and p1.x_vel < 0):
            offsetx += p1.x_vel
            
            
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
