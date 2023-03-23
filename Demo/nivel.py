from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

speed = 1
dx = 0
switch = 1

def update():
    global speed, dx, switch

    if switch == 1:
        dx += speed * time.dt
        if abs(dx) > 2:
            speed *= -1
            dx = 0
        enemy.x += speed * time.dt

        #for enemy in enemies:
        #   enemy.x += speed * time.dt

            #Colision con enemies
            #if abs(player.x - enemy.x) < 1 and abs(player.y - enemy.y)< 1:
            # do something   
            #for death player.rotation_z = 90
            #          switch = 0

        #Colision con barril
        dis = abs(player.x - cannon.x)  
        if dis <= 1 and abs(player.y - ground.y) <= 3:         #abs(dis - SIZE_X)%SIZE_X <= 1 / abs(dis - SIZE_X)%SIZE_X >= SIZE_X - 1 / abs(player.y - ground.y) <= 1
            player.color = color.red
        else:
            player.color = color.white


class Enemy(Entity):
    '''Clase para la creacion de enemigos'''
    def __init__(self, x, y, texture:str):
        super().__init__()
        self.model = 'cube'
        self.texture = texture
        self.color = color.green
        self.x = x
        self.y = y


app = Ursina()

SIZE_X = 16
SIZE_Y = 11

#Enemigo
enemy = Enemy(1, 1, 'assets/enemigo.png')

# BackGroud
#Sigue siendo un objeto por lo que se podria caer#
bg = Entity(model ='quad', scale =(SIZE_X, SIZE_Y), texture = "assets/jungle-trees", z = 1)

dupes = 2
for i in range(dupes): 
    duplicate(bg, x = SIZE_X * (i + 1)) #Extend bg
    duplicate(bg, x = -SIZE_X * (i + 1))

# Player entity
player = PlatformerController2d( y = -1, x = -3 , z = 0.1, scale_y = 1, color = color.white, texture = "/player_Assets/dk")

# Platforms
ground = Entity(model ='quad', y = -3.8, x = 0, scale_x = 15, collider = 'box', color = color.yellow)
duplicate(ground, x = SIZE_X)
duplicate(ground, x = -SIZE_X)

wall = Entity(model = 'quad', color = color.azure, scale = (1, 5), x = 6, y = 0.2, collider='box')

level = Entity(model = 'quad', color = color.red, scale = (3, 1), x = 2, collider='box')

ceiling = Entity(model = 'quad', color = color.cyan, scale = (3, 1), x = -2.5, y = 1, collider='box')

#objects
cannon = Entity(model = 'quad', scale = (2, 1), x = -6, y = -2, texture = "assets/barril.png", collider = 'box')


#camera settings#
                            #  target = ##    offset = [x , y, z]    ##
camera.add_script(SmoothFollow(target=player, offset = [0 , 1, -40], speed= 4))



app.run()