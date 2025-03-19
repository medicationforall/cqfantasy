import cadquery as cq
from cqfantasy.house import House

bp_house = House()
bp_house.length = 100
bp_house.width = 150
bp_house.height = 75
bp_house.roof_height = 50
bp_house.roof_overhang = (15,10,4)

bp_body = bp_house.bp_body
bp_body.wall_width = 4

bp_door = bp_house.bp_door
bp_door.height = 50
bp_door.width = 2.5

bp_roof = bp_house.bp_roof

bp_house.window_x_style = ['None',None,None,'window']
bp_house.window_y_style = [None,'window','window','window','window',None]

bp_house.make()
ex_house_plate = bp_house.build_plate()

#show_object(ex_house_plate)
cq.exporters.export(ex_house_plate, "stl/house_plate.stl")