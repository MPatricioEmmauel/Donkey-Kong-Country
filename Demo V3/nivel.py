from __future__ import annotations
from abc import ABC, abstractmethod
from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
import copy

# ///////////////////////////////////////// #

#Bridge
class Cases(ABC):
    '''Interfaz para funciones repetidas'''
    def makesDupes(self, n:int, position:float):
        for i in range(n):
            duplicate(self, x = position * (i + 1)),  
            duplicate(self, x = -position * (i + 1))

    #strategy
    @abstractmethod
    def fondos():
        pass


# ///////////////////////////////////////// #

class Enemy(Entity):
    '''Clase para la creacion de enemigos'''
    def __init__(self, x, y, texture:str):
        super().__init__()
        self.model = 'cube'
        self.texture = texture
        self.color = color.green
        self.x = x
        self.y = y

# ///////////////////////////////////////// #
class Plattforms(Entity, Cases):
    '''Clase creadora de Plataformas'''
    def __init__(self, x = 1, y = 1, z = 1, scaleX = 1, scaleY = 1, color = color.yellow, texture = ''):
        super().__init__()
        self.model = 'quad'
        self.collider = 'box'
        self.scale_x:float = scaleX
        self.scale_y:float = scaleY
        self.x:float = x
        self.y:float = y
        self.z:float = z
        self.color:color = color
        self.texture = texture

class Background(Entity, Cases):
    '''Clase creadora de Fondos'''
    def __init__(self, x = 1, y = 1, z = 1, scale:tuple = (1, 1), texture = ''):
        super().__init__()
        self.model = 'quad'
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.texture = texture
        self.z = z

    def fondos( n, z, texture = ""):
        _cache = []
        _x = 16
        _mx = -16

        for i in range(n):
            x = (i * _x)
            m = (i * _mx)
            _cache.append(Background(x, 0, z, (16, 11), texture))
            
            if m != 0:
                _cache.append(Background(m, 0, z, (16, 11), texture))


class Wall(Entity, Cases):
    '''Clase creadora de Wall'''
    def __init__(self, scale:tuple = (1, 1), color = color.azure, x = 1 , y = 1):
        super().__init__()
        self.model = 'quad'
        self.collider = 'box'
        self.color = color
        self.scale = scale
        self.x = x
        self.y = y

class Level(Entity, Cases):
    '''Clase creadora de Level'''
    def __init__(self, scale:tuple = (1, 1), color = color.red, x = 1):
        super().__init__()
        self.model = 'quad'
        self.collider = 'box'
        self.color = color
        self.scale = scale
        self.x = x

class Ceiling(Entity, Cases):
    '''Clase creadora de Ceiling'''
    def __init__(self, scale:tuple = (1, 1), color = color.red, x = 1, y = 1):
        super().__init__()
        self.model = 'quad'
        self.collider = 'box'
        self.color = color
        self.scale = scale
        self.x = x
        self.y = y

# ///////////////////////////////////////// #
#Singleton
class Update():
    '''Singleton'''
    __instance = None
    
    def __init__(self) -> None:
        self.speed = 1
        self.dx = 0
        self.switch = 1

    def __new__(cls):
        if Update.__instance is None:
                Update.__instance = object.__new__(cls)
        return Update.__instance
        
  
# ///////////////////////////////////////// #

e = Update()
app = Ursina()


def update():
        '''Funcion Para movimiento y colisiones'''
        if not soundtrack.playing:
            soundtrack.play()

        if e.switch == 1:
            e.dx += e.speed * time.dt
            if abs(e.dx) > 2:
                e.speed *= -1
                e.dx = 0
            enemy.x += e.speed * time.dt

            #for enemy in enemies:
            #   enemy.x += speed * time.dt

                #Colision con enemies
                #if abs(player.x - enemy.x) < 1 and abs(player.y - enemy.y)< 1:
                # do something   
                #for death player.rotation_z = 90
                #          switch = 0
        
        #flag 
        if ( abs(player.x - flag.x) <= 1) and (abs(player.y - ground.y) <= 2 and abs(player.y - ground.y) >= -4):
            app.closeWindow()
            
        #Colision con barril
        if abs(player.x - cannon.x) <= 1 and abs(player.y - ground.y) <= 7 and  abs(player.y - ground.y) >= 4:    #abs(dis - SIZE_X)%SIZE_X <= 1 / abs(dis - SIZE_X)%SIZE_X >= SIZE_X - 1 / abs(player.y - ground.y) <= 1
            player.color = color.red
        else:
            player.color = color.white




# /////////////////////////////////////// #

app.ventana = 60

SIZE_X = 16.0
SIZE_Y = 11.0


# ///// #

'''Instacias''' 
 #Enemigos
enemy = Enemy(1, 1, 'assets/enemigo.png')

# Platforms // x, y, z, scaleX, scaleY, texture, color = color.yellow
ground = Plattforms( 0, -7, 0, 16, 3.4, color.yellow, 'grass')
ground.makesDupes(2, SIZE_X)

# BackGroud // numero, z, Texture
Background.fondos(3, 1, "fondos/jungle-trees")
Background.fondos(3, 2, "fondos/far")

# Prefab Para el cielo
Sky(texture = "assets/cloud-BG")

# Walls // scale = (1, 1), color, x , y 
initWall = Wall((1, 11), color.clear, -39.5, 0.2)
wall = Wall((1, 5), color.azure, 6, 0.2)
finalWall = Wall((1, 11), color.clear, 39.5, 0.2)

# Level Plattform // scale:tuple, color, x 
level = Level((3, 1), color.red, 2)

#Ceiling scale, x, y
ceiling = Ceiling((3, 1), color.cyan, -2.5, 1)
cel2 = Ceiling((3, 1), color.cyan, -8, -1)
cel3 = Ceiling((3, 1), color.cyan, -14, -2.5)

#objects
cannon = Entity(model = 'quad', scale = (2, 1), x = 15, y = -1, texture = "assets/barril.png")
flag = Entity(model = 'quad', scale = (2, 2), x = 35, y = -4.3, texture = "assets/flag.png")

# /////////////////////////////////////// #

# sound
soundtrack = Audio(
    "music/Jungle_beat.ogg",
    loop = True,
    autoplay = True
)

# Player entity
player = PlatformerController2d(y = 0.3, x = -3 , z = 0.1, scale_y = 1, color = color.white, texture = "/player_Assets/dk")

#camera settings               target = ##    offset = [x , y,   z]    ##
camera.add_script(SmoothFollow(target = player, offset = [0 , 3, -30], speed = 4))

# /////////////////////////////////////// #

app.run()