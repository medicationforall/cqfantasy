import cadquery as cq
from cqfantasy.house_wall import LogWall

bp_wall = LogWall()

bp_wall.length = 30
bp_wall.width = 5
bp_wall.height = 60
bp_wall.log_count = 9
bp_wall.diameter_overlap = 5
bp_wall.spread_width = True


bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall, "stl/house_log_wall.stl")