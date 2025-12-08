import cadquery as cq
from cqfantasy.house import SnowyRoof

bp_roof = SnowyRoof()
bp_roof.overhang = (10,16,10)
bp_roof.height = 50
bp_roof.length = 150
bp_roof.width = 150
bp_roof.make()
ex_roof = bp_roof.build()

#show_object(ex_roof.translate((0,0,0)))

cq.exporters.export(ex_roof,'stl/house_roof_snow.stl')