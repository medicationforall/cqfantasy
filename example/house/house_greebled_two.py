import cadquery as cq
from cqfantasy.house import House, TudorSplitBody, ShingleRoof, BodyGreebled
from cqfantasy.house_wall import WallTudor, WallStuccoBrick, WallTudorPaneling, WallSplit
from cqterrain.tile import dwarf_star

def make_dwarf_star(
    length:float, 
    width:float, 
    height:float
) -> cq.Workplane:
    tile = dwarf_star(
        length, 
        width, 
        height
        #set hardcoded overrides here
    )
    return tile

#-------------------------

bp_house = House()
bp_house.length = 100
bp_house.width = 175
bp_house.height = 75
bp_house.roof_height = 50
bp_house.roof_overhang = (15,10, 4)
#bp_house.roof_gap_spacer = 2

bp_house.render_roof = True
bp_house.render_doors = True

bp_house.bp_body = BodyGreebled()
bp_body = bp_house.bp_body
bp_body.render_outside_walls = True
bp_body.render_inside_walls = True
bp_body.render_floor_tiles = True

#bp_body.bp_tile_generator = TileGenerator()
bp_tiles = bp_body.bp_tile_generator
bp_tiles.tile_length = 25
bp_tiles.tile_width = 25
bp_tiles.tile_height = 2
bp_tiles.tile_padding = .5
bp_tiles.overflow = 17
bp_tiles.make_tile_method = make_dwarf_star

#bp_body.tile_height = 1.5
bp_body.floor_height = 2
outside_wall = WallStuccoBrick()
outside_wall.length_padding = 0
outside_wall.block_length = 8
outside_wall.width = 5
outside_wall.block_height = 3
outside_wall.block_spacing = 2
outside_wall.center=True

split_wall = WallSplit()
split_wall.width = 2.5
split_wall.split_divide_height = 26.5
split_wall.bp_upper_wall = WallTudor()
split_wall.bp_upper_wall.panel_sections = 3
split_wall.bp_upper_wall.styles = ["right",None,'left']

split_wall.bp_lower_wall = WallStuccoBrick()
split_wall.bp_lower_wall.block_length = 5
split_wall.bp_lower_wall.block_spacing = 2
split_wall.bp_lower_wall.spread_width = True

split_wall_width = WallSplit()
split_wall_width.width = 2.5
split_wall_width.split_divide_height = 26.5
split_wall_width.bp_upper_wall = WallTudor()
split_wall_width.bp_upper_wall.styles = ["right",None,'cross',None,'cross',None,'left']

split_wall_width.bp_lower_wall = WallStuccoBrick()
split_wall_width.bp_lower_wall.block_length = 5
split_wall_width.bp_lower_wall.block_spacing = 2
split_wall_width.bp_lower_wall.spread_width = False

bp_body.bp_outside_walls = [split_wall, split_wall_width, split_wall, split_wall_width]


internal_wall_tudor = WallTudorPaneling()
internal_wall_tudor.rows = 3
internal_wall_tudor.columns = 4
#internal_wall_tudor.panel_sections = 4

internal_wall_tudor2 = WallTudorPaneling()
internal_wall_tudor2.rows = 3
internal_wall_tudor2.columns = 5
#internal_wall_tudor2.panel_sections = 6
bp_body.bp_inside_walls = [internal_wall_tudor,internal_wall_tudor2,internal_wall_tudor,internal_wall_tudor2]

bp_door = bp_house.bp_door
bp_door.height = 50
bp_door.width = 2.5
bp_house.door_cut_width_padding = 10

bp_house.bp_roof = ShingleRoof()
bp_roof = bp_house.bp_roof
bp_roof.tile_length = 10
bp_roof.overhang_inset = (12,10,4)

bp_roof.bp_outside_wall = WallTudor()
bp_roof.bp_outside_wall.panel_length = 130/4
bp_roof.bp_outside_wall.panel_space:float = 2
bp_roof.bp_outside_wall.panel_width:float = 2.5 
bp_roof.bp_outside_wall.styles = "cross"

bp_house.window_space = (bp_house.length/3,25)
bp_house.window_x_style = ['window',None,"window"]
bp_house.window_y_style = [None,'window',None,'window',None,'window',None]
bp_house.window_offset = 14
bp_house.window_length = 14
bp_house.window_width = 8

bp_house.make()
#ex_house = bp_house.build()

#show_object(ex_house)
#cq.exporters.export(ex_house, "stl/house_greebled_two_plate.stl")

ex_house_plate = bp_house.build_plate()
#show_object(ex_house_plate)

cq.exporters.export(ex_house_plate, "stl/house_greebled_two_plate.stl")
