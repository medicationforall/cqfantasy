import cadquery as cq
from cqfantasy.house import Roof, WallTudor

bp_roof = Roof()
bp_roof.length = 100
bp_roof.width = 150
bp_roof.height= 50
bp_roof.overhang = (4,8,4)
bp_roof.render_overhang_inset = True
bp_roof.overhang_inset = (8,4,4)

bp_roof.bp_outside_wall = WallTudor()
bp_roof.bp_outside_wall.panel_length = bp_roof.length /4
bp_roof.bp_outside_wall.styles = "cross"


bp_roof.make()

ex_roof = bp_roof.build()

#show_object(ex_roof)
cq.exporters.export(ex_roof,'stl/house_roof_greebled.stl')