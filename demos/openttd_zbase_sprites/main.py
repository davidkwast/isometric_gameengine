from enum import Enum
from collections import namedtuple
import itertools

import pyglet
from pyglet.window import mouse


XY = namedtuple('XY',['x','y'])


class EngineTerrainObject:
    NEXT_ID = 1
    
    def __init__(self):
        self.unit_id = self.NEXT_ID
        self.NEXT_ID += 1


class EngineUnitObject:
    NEXT_ID = 1
    
    def __init__(self):
        self.unit_id = self.NEXT_ID
        self.NEXT_ID += 1


class Direction(Enum):
    NORTH = ( 0, -1)
    EAST =  ( 1,  0)
    SOUTH = ( 0,  1)
    WEST  = (-1,  0)


class CoalTruck(EngineUnitObject):
    
    
    def __init__(self, position: XY):
        
        super().__init__()
        self.position = position
        self.go_to = position#6*128, 720-8*64
        self.direction = Direction.EAST
        self.moving_flag = False
        self.moving_direction = Direction.EAST
        self.image = pyglet.resource.image('assets/truck_coal/256_0563.png')
        self.sprite = pyglet.sprite.Sprite(img=self.image)
        self.sprite.x, self.sprite.y = self.position
    
    
    def move_to(self, go_to: XY):
        self.go_to = go_to
    
    
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


class RoadTile(TerrainTile):
    def __init__(self, img_id: int):
        super().__init__(pyglet.resource.image(f'assets/land_road/256_00{img_id}.png'))


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
            (3,0): (128*1, 64*5), (2,1): (128*3, 64*5), (1,2): (128*5, 64*5), (0,3): (128*7, 64*5),
                        (3,1): (128*2, 64*4), (2,2): (128*4, 64*4), (1,3): (128*6, 64*4), (0,4): (128*8, 64*4),
                                  (3,2): (128*3, 64*3), (2,3): (128*5, 64*3), (1,4): (128*7, 64*3),
                                              (3,3): (128*4, 64*2), (2,4): (128*6, 64*2),
                                                        (3,4): (128*5, 64*1)
        }
        for (x, y), (pos_x, pos_y) in tile_index_map.items():
            self.map_tiles[x][y].update_sprite_position(XY(pos_x, pos_y))



map_tiles = [
    [GrassTile(), GrassTile(), GrassTile(), GrassTile(), GrassTile(), ],
    [GrassTile(), GrassTile(), GrassTile(), GrassTile(), GrassTile(), ],
    [GrassTile(), GrassTile(), GrassTile(), GrassTile(), GrassTile(), ],
    [GrassTile(), GrassTile(), GrassTile(), GrassTile(), GrassTile(), ],
]


world = World(
    map_size = XY(4,3),
    map_tiles = map_tiles,
)


road_tiles = [RoadTile(25), RoadTile(25), RoadTile(25), RoadTile(35)]
road_tiles[0].update_sprite_position(XY(128*2,64*5))
road_tiles[1].update_sprite_position(XY(128*3,64*4))
road_tiles[2].update_sprite_position(XY(128*4,64*3))
road_tiles[3].update_sprite_position(XY(128*5,64*2))


window = pyglet.window.Window(resizable=True)
#window.maximize()
window.set_location(0, 0)
window.set_size(1280, 720)


coal_truck_01 = CoalTruck(XY(128*1.85, 64*5.85))
coal_truck_01.move_to(XY(128*5.85, 64*1.85))

moving_units = [
    coal_truck_01,
]


# goods industry building
g19 = pyglet.sprite.Sprite(img=pyglet.resource.image('assets/ind_goods/256_0019.png'))
g17 = pyglet.sprite.Sprite(img=pyglet.resource.image('assets/ind_goods/256_0017.png'))
g20 = pyglet.sprite.Sprite(img=pyglet.resource.image('assets/ind_goods/256_0020.png'))

gst04 = pyglet.sprite.Sprite(img=pyglet.resource.image('assets/road_station_cargo/256_0004.png'))

g19.x, g19.y = 128*6, 64*5
g17.x, g17.y = 128*5, 64*4
g20.x, g20.y = 128*7, 64*4

gst04.x, gst04.y = 128*6, 64*3

ind_goods_01 = [g19, g17, g20, gst04]



fps_display = pyglet.window.FPSDisplay(window)


@window.event
def on_draw():
    
    window.clear()
    
    for tile in world.get_tiles_for_drawing():
        tile.draw()
    
    for tile in ind_goods_01:
        tile.draw()
    
    for tile in road_tiles:
        tile.draw()
    
    for unit in moving_units:
        unit.draw()
    
    fps_display.draw()


def update(dt):
    
    for unit in moving_units:
        unit.update(dt)


pyglet.clock.schedule_interval(update, 1/60)



@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.RIGHT:
        print(f'drag event, mouse right: x:{x}, y:{y}, dx:{dx}, dy:{dy}')



pyglet.app.run()
