import cadquery as cq
from cqfantasy.tower import TileGenerator

def make_basic_tile(
    length:float, 
    width:float, 
    height:float
) -> cq.Workplane:
    tile = cq.Workplane("XY").box(
        length, 
        width, 
        height
    )
    return tile

bp_tiles = TileGenerator()

bp_tiles.diameter = 100
bp_tiles.tile_length = 10
bp_tiles.tile_width = 10
bp_tiles.tile_height = 3
bp_tiles.tile_padding = 1
bp_tiles.overflow = 12
bp_tiles.make_tile_method = make_basic_tile

bp_tiles.make()

tiles = bp_tiles.build()

#show_object(tiles)

cq.exporters.export(tiles,'stl/tower_tile_generator.stl')