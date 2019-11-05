from enum import Enum
from collections import namedtuple
import itertools

import pyglet

XY = namedtuple('XY',['x','y'])

class EngineTerrainObject:
    NEXT_ID = 1

    def __init__(self):
        self.unit_id =  self.NEXT_ID
        self.NEXT_ID += 1

class EngineUnitObject:
    NEXT_ID = 1

    def __init__(self):
        self.unit_id =  self.NEXT_ID
        self.NEXT_ID += 1

# class GraphicUnit(EngineObject):
#     def __init__(self, pyglet_batch: pyglet.graphics.Batch):
#         self.pyglet_batch = pyglet_batch

# class TerrainTile(GraphicUnit):
#     def __init__(self, )


class Direction(Enum):
    NORTH = ( 0, -1)
    EAST =  ( 1,  0)
    SOUTH = ( 0,  1)
    WEST  = (-1,  0)

# class DirectionalGraphicUnit:
#     def __init__(self, directional_sprite_dict):
#         self.directional_sprite_dict = directional_sprite_dict

class CoalTruck(EngineUnitObject):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.go_to = 6*128, 720-8*64
        self.direction = Direction.EAST
        self.moving_flag = False
        self.moving_direction = Direction.EAST
        self.image = pyglet.resource.image('assets/truck_coal/256_0563.png')
        self.sprite = pyglet.sprite.Sprite(img=self.image)
        self.sprite.x, self.sprite.y = self.position
    
    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        pos = self.position
        gt = self.go_to
        
        if pos == gt: return False

        s = self.sprite
        s.x += 128 * dt / 2
        s.y += -64 * dt / 2
        
        if int(s.x) > gt[0]:
            s.x = gt[0]
        if int(s.y) < gt[1]:
            s.y = gt[1]
        
        self.position = s.x, s.y

        return True


class TerrainTile(EngineTerrainObject):
    def __init__(self, image: pyglet.resource.image):
        super().__init__()
        self.image = image
        self.sprite = pyglet.sprite.Sprite(img=image)
    
    def update_sprite_position(self, position: XY):
        self.sprite.x, self.sprite.y = position


    def draw(self):
        self.sprite.draw()

class GrassTile(TerrainTile):
    def __init__(self):
        super().__init__(pyglet.resource.image('assets/land_grass/256_0001.png'))


class World:

    def __init__(self, map_size: XY, map_tiles):
        self.map_size = map_size
        self.map_tiles = map_tiles
        self._update_sprites_absolute_screen_position()
    
    def get_tiles_for_drawing(self):
        return itertools.chain(*self.map_tiles)
    
    def _update_sprites_absolute_screen_position(self):
        tile_index_map = {
            (0,0): (128*4, 64*8),
            (1,0): (128*3, 64*7), (0,1): (128*5, 64*7),
            (2,0): (128*2, 64*6), (1,1): (128*4, 64*6), (0,2): (128*6, 64*6),
        }
        for (x, y), (pos_x, pos_y) in tile_index_map.items():
            self.map_tiles[x][y].update_sprite_position(XY(pos_x, pos_y))


map_tiles = [[GrassTile() for x in range(4)],[GrassTile() for x in range(4)],[GrassTile() for x in range(4)]]

world = World(
    map_size = XY(4,3),
    map_tiles = map_tiles,
)


window = pyglet.window.Window(resizable=True)
#window.maximize()
window.set_location(0, 0)
window.set_size(1280, 720)


moving_units = [
    CoalTruck((0*128, 720-2*64)),
]

fps_display = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():
    window.clear()

    for tile in world.get_tiles_for_drawing():
        tile.draw()

    for unit in moving_units:
        unit.draw()

    fps_display.draw()

def update(dt):

    for unit in moving_units:
        unit.update(dt)


pyglet.clock.schedule_interval(update, 1/100)
pyglet.app.run()