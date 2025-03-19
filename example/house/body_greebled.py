import cadquery as cq
from cqfantasy.house import BodyGreebled 
from cqfantasy.house_wall import WallStuccoBrick, WallTudorPaneling, WallTudor

bp_body = BodyGreebled()
bp_body.length = 100
outside_wall = WallStuccoBrick()
outside_wall.length_padding = 0
outside_wall.block_length = 8
outside_wall.width = 5
outside_wall.block_height = 3
outside_wall.block_spacing = 2
outside_wall.center=True

internal_wall = WallTudorPaneling()
internal_wall.render_outline = False
external_wall_tudor = WallTudor()
external_wall_tudor.panel_sections = 6

bp_body.bp_outside_walls = [external_wall_tudor]

internal_wall_tudor = WallTudor()
internal_wall_tudor.panel_sections = 4

internal_wall_tudor2 = WallTudor()
internal_wall_tudor2.panel_sections = 6
bp_body.bp_inside_walls = [internal_wall_tudor,internal_wall_tudor2,internal_wall_tudor,internal_wall_tudor2]

bp_body.make()

ex_body = bp_body.build()

#show_object(ex_body)
cq.exporters.export(ex_body, "stl/house_body_greebled.stl")