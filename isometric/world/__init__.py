import itertools

from .. import XY
from ..tiles import Terrain_Tile


class World:
    
    def __init__(self, size: XY, base_tile_sprite_factory):
        
        self.map_size = size
        self.base_tile_sprite_factory = base_tile_sprite_factory
        
        Tile = Terrain_Tile
        factory = base_tile_sprite_factory
        self.map_tiles = [
            [Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), ],
            [Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), ],
            [Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), ],
            [Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), Tile(factory()), ],
        ]
        
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
            print(x, y, pos_x, pos_y)
            self.map_tiles[x][y].update_sprite_position(XY(pos_x, pos_y))