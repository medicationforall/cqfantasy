import cadquery as cq
from cqfantasy.house import TudorBody

bp_body = TudorBody()
bp_body.length = 150
bp_body.width = 100

bp_body.x_styles = [None,"right","left","right","left"]
bp_body.y_styles = ["cross","left","right","cross"]

bp_body.split_divide_height = 25
bp_body.panel_length = 25
bp_body.panel_width = 2.5
bp_body.panel_space = 2

bp_body.make()
ex_body = bp_body.build()

#show_object(ex_body)

cq.exporters.export(ex_body,'stl/house_body_tudor.stl')