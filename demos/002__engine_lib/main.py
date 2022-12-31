import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

import isometric
import isometric.tiles
import isometric.world



def main_loop(dt):
    
    pass



def main():
    
    
    grass_image = isometric.tiles.Image('assets/land_grass/256_0001.png')
    
    def grass_sprite_factory():
        return isometric.tiles.Simple_Sprite(grass_image)
    
    
    world_size = isometric.XY(5,4)
    world_obj = isometric.world.World(size=world_size, base_tile_sprite_factory=grass_sprite_factory)
    
    
    engine = isometric.Engine(main_loop, world_obj)
    
    engine.run()


if __name__ == '__main__':
    main()