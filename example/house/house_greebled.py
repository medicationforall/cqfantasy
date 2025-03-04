import cadquery as cq
from cqfantasy.house import House, TudorSplitBody

bp_house = House()
bp_house.length = 100
bp_house.width = 130
bp_house.height = 75
bp_house.roof_height = 50
bp_house.roof_overhang = (15,10)

bp_house.render_roof = True
bp_house.render_doors = True

#bp_house.bp_body = TudorBody()
#bp_house.bp_body = TudorBody()
#bp_house.bp_body = StuccoBrickBody()
bp_house.bp_body = TudorSplitBody()


bp_body = bp_house.bp_body
bp_body.wall_width = 4
bp_body.split_divide_height = 30
bp_body.x_styles = ["left",None,None,'right']
bp_body.y_styles = ["cross",None,'cross',None,'cross']

bp_door = bp_house.bp_door
bp_door.height = 50
bp_door.width = 2.5
bp_house.door_cut_width_padding = 10

bp_roof = bp_house.bp_roof

bp_house.window_x_style = [None,None,None]
bp_house.window_y_style = [None,'window',None,'window',None,'window',None]

bp_house.make()
ex_house = bp_house.build()

#show_object(ex_house)
cq.exporters.export(ex_house, "stl/house_greebled.stl")