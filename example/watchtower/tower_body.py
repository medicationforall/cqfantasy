import cadquery as cq
from cqfantasy.watchtower import TowerBody

bp_body = TowerBody()
bp_body.length = 75
bp_body.width = 75
bp_body.height = 125
bp_body.make()

ex_body = bp_body.build()

#show_object(ex_body)

cq.exporters.export(ex_body, "stl/watch_tower_body.stl")