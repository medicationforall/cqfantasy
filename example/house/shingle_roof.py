import cadquery as cq
from cqfantasy.house import ShingleRoof

bp_roof = ShingleRoof()
bp_roof.height = 25
bp_roof.length = 50
bp_roof.width = 50
bp_roof.make()
ex_roof = bp_roof.build()

#show_object(ex_roof.translate((0,0,0)))
cq.exporters.export(ex_roof,'stl/house_roof_shingle.stl')