import cadquery as cq
from cqfantasy.house import SnowyRoof

bp_roof = SnowyRoof()
bp_roof.overhang = (10,16,10)
bp_roof.height = 50
bp_roof.length = 150
bp_roof.width = 150

bp_roof.tile_length = 10
bp_roof.tile_width = 10
bp_roof.tile_height = 0.8
bp_roof.tile_rotation = 4
bp_roof.tile_push = 2
bp_roof.seed_one = 'test'
bp_roof.seed_two = 'test_four'
bp_roof.snow_height = 7
bp_roof.snow_peak_count = 5
bp_roof.snow_segments = 3
bp_roof.snow_z_translate= 0

bp_roof.make()
ex_roof = bp_roof.build()

#show_object(ex_roof.translate((0,0,0)))

cq.exporters.export(ex_roof,'stl/house_roof_snow.stl')