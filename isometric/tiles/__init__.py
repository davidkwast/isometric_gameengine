import pyglet

from .. import XY



class Image:
    
    def __init__(self, file_path):
        
        self.file_path = file_path
        self.obj = pyglet.resource.image(file_path)


class Simple_Sprite:
    
    def __init__(self, image):
        
        self.image = image
        self.obj = pyglet.sprite.Sprite(img=self.image.obj)


class Engine_Terrain_Object:
    NEXT_ID = 1
    
    def __init__(self):
        
        self.unit_id = self.NEXT_ID
        self.NEXT_ID += 1


class Terrain_Tile(Engine_Terrain_Object):
    
    
    def __init__(self, sprite):
        
        super().__init__()
        
        self.sprite = sprite.obj
    
    
    def update_sprite_position(self, position: XY):
        
        self.sprite.x, self.sprite.y = position
    
    
    def draw(self):
        self.sprite.draw()