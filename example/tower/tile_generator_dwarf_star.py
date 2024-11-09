import cadquery as cq
from cqfantasy.tower import TileGenerator
from cqterrain.tile import dwarf_star

def make_dwarf_star(
    length:float, 
    width:float, 
    height:float
) -> cq.Workplane:
    tile = dwarf_star(
        length, 
        width, 
        height
        #set hardcoded overrides here
    )
    return tile

bp_tiles = TileGenerator()

bp_tiles.diameter = 100
bp_tiles.tile_length = 15
bp_tiles.tile_width = 15
bp_tiles.tile_height = 3
bp_tiles.tile_padding = .5
bp_tiles.overflow = 12
bp_tiles.make_tile_method = make_dwarf_star

bp_tiles.make()

tiles = bp_tiles.build()

#show_object(tiles)

cq.exporters.export(tiles,'stl/tower_tile_generator_dwarf_star.stl')