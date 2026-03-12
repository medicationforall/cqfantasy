import cadquery as cq
from cqfantasy.watchtower import TowerBodyGreebled

bp_body = TowerBodyGreebled()
bp_body.length = 75
bp_body.width = 75
bp_body.height = 125

bp_body.render_doors = True
bp_body.render_windows = True
bp_body.render_outside_walls = True
bp_body.render_inside_walls = True
bp_body.render_floor_tiles = True
bp_body.render_outside_corners = True
bp_body.render_ladder = True
bp_body.make()

ex_body = bp_body.build()

#show_object(ex_body)

cq.exporters.export(ex_body, "stl/watch_tower_body_greebled.stl")