from collections import namedtuple

import pyglet
from pyglet.window import mouse



XY = namedtuple('XY',['x','y'])


window = pyglet.window.Window(resizable=True)


class Engine:
    
    
    def __init__(self, loop_func, world_obj):
        
        self.loop = loop_func
        self.world = world_obj
    
    
    def run(self):
        
        
        @window.event
        def on_draw():
            
            window.clear()
            
            for tile in self.world.get_tiles_for_drawing():
                # print(tile.sprite.x, tile.sprite.y)
                tile.draw()
        
        
        pyglet.clock.schedule_interval(self.loop, 1/60)
        
        pyglet.app.run()