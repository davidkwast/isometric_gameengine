from enum import Enum

import pyglet


class EngineObject:
    
    NEXT_ID = 1

    def __init__(self):
        self.unit_id = NEXT_ID
        NEXT_ID += 1

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

class CoalTruck(EngineObject):
    def __init__(self, batch):
        self.position = 0*128, 720-2*64
        self.go_to = 6*128, 720-8*64
        self.direction = Direction.EAST
        self.moving_flag = False
        self.moving_direction = Direction.EAST
        self.image = pyglet.resource.image('assets/truck_coal/256_0563.png')
        self.sprite = pyglet.sprite.Sprite(img=self.image, batch=batch)
        self.sprite.x, self.sprite.y = self.position
    
    def update(self, dt):
        pos = self.position
        gt = self.go_to
        
        if pos == gt: return False

        s = self.sprite
        s.x += int(128 * dt)
        s.y += int(-64 * dt)
        
        if s.x > gt[0]:
            s.x = gt[0]
        if s.y < gt[1]:
            s.y = gt[1]
        
        self.position = s.x, s.y

        return True



window = pyglet.window.Window(resizable=True)
#window.maximize()
window.set_location(0, 0)
window.set_size(1280, 720)

image_grass = pyglet.resource.image('assets/land_grass/256_0001.png')

batch = pyglet.graphics.Batch()

sprite_grass = pyglet.sprite.Sprite(img=image_grass, batch=batch)
sprite_grass.x, sprite_grass.y = 0, 720-128


moving_units = [
    CoalTruck(batch),
]



fps_display = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()

def update(dt):

    for unit in moving_units:
        unit.update(dt)


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()