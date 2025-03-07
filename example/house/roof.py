import cadquery as cq
from cqfantasy.house import Roof

bp_roof = Roof()
bp_roof.length = 100
bp_roof.width = 150
bp_roof.height = 75

bp_roof.overhang = (4,4,4)

bp_roof.render_overhang_inset = True
bp_roof.overhang_inset = (4,2,4)

bp_roof.make()
ex_roof = bp_roof.build()

#show_object(ex_roof)
cq.exporters.export(ex_roof, "stl/house_roof.stl")