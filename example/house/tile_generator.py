import cadquery as cq
from cqfantasy.house import TileGenerator

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

bp_tile = TileGenerator()

bp_tile.length= 100
bp_tile.width = 100
bp_tile.tile_length = 10
bp_tile.tile_width = 10
bp_tile.tile_height = 3
bp_tile.tile_padding = 1
bp_tile.overflow = 12
bp_tile.make_tile_method = make_basic_tile
bp_tile.render_intersect = True

bp_tile.make()

ex_tiles = bp_tile.build()

#show_object(ex_tiles)

cq.exporters.export(ex_tiles, 'stl/house_tile_generator.stl')

