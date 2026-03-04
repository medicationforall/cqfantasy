import cadquery as cq
from cqfantasy.watchtower import TowerTopGreebled

bp_top = TowerTopGreebled()
bp_top.length:float = 115
bp_top.width:float = 115
bp_top.height:float = 75
bp_top.render_doors = True
bp_top.render_windows = True
bp_top.render_outside_walls = True
bp_top.render_inside_walls = True
bp_top.render_floor_tiles = True
bp_top.make()

ex_top = bp_top.build()

#show_object(ex_top)

cq.exporters.export(ex_top, "stl/watch_tower_top_greebled.stl")