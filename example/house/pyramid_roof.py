import cadquery as cq
from cqfantasy.house import PyramidRoof

bp_roof = PyramidRoof()

bp_roof.length = 140
bp_roof.width = 140
bp_roof.height = 75

bp_roof.overhang = (5,5)
bp_roof.wall_width= (4,4,4)

bp_roof.render_magnets = True
bp_roof.magnet_diameter = 3.4
bp_roof.magnet_height = 2.2

bp_roof.make()
ex_roof = bp_roof.build()

#show_object(ex_roof)
cq.exporters.export(ex_roof, "stl/house_pyramid_roof.stl")