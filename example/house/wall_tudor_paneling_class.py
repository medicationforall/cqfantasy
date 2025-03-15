import cadquery as cq
from cqfantasy.house import WallTudorPaneling

bp_wall = WallTudorPaneling()

bp_wall.length = 100
bp_wall.width = 2
bp_wall.height = 75

bp_wall.render_outline = False
bp_wall.h_frame_height = 4
bp_wall.v_frame_length = 2
bp_wall.rows = 5
bp_wall.columns = 10
bp_wall.row_height = 2
bp_wall.column_width = 2

bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall, "stl/house_wall_tudor_paneling_class.stl")