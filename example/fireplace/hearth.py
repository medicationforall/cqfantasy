import cadquery as cq
from cqfantasy.fireplace import Hearth

bp_hearth = Hearth()
bp_hearth.length = 35
bp_hearth.width = 35
bp_hearth.height = 3

bp_hearth.make()
result = bp_hearth.build()

#show_object(result)
cq.exporters.export(result, "stl/fireplace_hearth.stl")