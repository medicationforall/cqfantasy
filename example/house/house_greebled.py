import cadquery as cq
from cqfantasy.house import House, TudorSplitBody

bp_house = House()
bp_house.length = 100
bp_house.width = 175
bp_house.height = 75
bp_house.roof_height = 50
bp_house.roof_overhang = (15,10)

bp_house.render_roof = True
bp_house.render_doors = True

#bp_house.bp_body = TudorBody()
#bp_house.bp_body = TudorBody()
#bp_house.bp_body = StuccoBrickBody()
bp_house.bp_body = TudorSplitBody()

bp_house.floor_height = 5
bp_body = bp_house.bp_body

bp_body.wall_width = 4
bp_body.split_divide_height = 25
bp_body.x_styles = ["right",None,None,'left']
bp_body.y_styles = ["right",None,'cross',None,'cross',None,'left']

bp_door = bp_house.bp_door
bp_door.height = 50
bp_door.width = 2.5
bp_house.door_cut_width_padding = 10

bp_house.tile_height = 1.5

bp_roof = bp_house.bp_roof

bp_house.window_x_style = [None,None,None]
bp_house.window_y_style = [None,'window',None,'window',None,'window',None]
bp_house.window_offset = 14
bp_house.window_length = 14

bp_house.make()
ex_house = bp_house.build()

#show_object(ex_house)
cq.exporters.export(ex_house, "stl/house_greebled.stl")

ex_house_plate = bp_house.build_plate()
#show_object(ex_house_plate)
cq.exporters.export(ex_house_plate, "stl/house_greebled_plate.stl")