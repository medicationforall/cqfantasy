import cadquery as cq
from cqfantasy.house import TileGenerator

bp_tile = TileGenerator()
bp_tile.make()

ex_tiles = bp_tile.build()

#show_object(ex_tiles)

cq.exporters.export(ex_tiles, 'stl/house_tile_generator.stl')

