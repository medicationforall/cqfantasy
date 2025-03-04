import cadquery as cq
from cqfantasy.house import Body, TudorBody, StuccoBrickBody, TudorSplitBody

scene = cq.Workplane()

bp_body = TudorSplitBody()

bp_body.seed = 'test2'

bp_body.height = 75
bp_body.length = 200
bp_body.width = 150

bp_body.split_divide_height = 35
bp_body.split_width = 3
bp_body.split_height = 3

bp_body.x_styles = "right"#["cross",None,None,"cross",]
bp_body.y_styles = "left"#["cross",None,None,"cross",]

bp_body.block_length = 8
bp_body.block_width = 5
bp_body.block_height = 3
bp_body.make()

ex_body = bp_body.build()

scene = scene.union(ex_body)
#show_object(ex_body)

#-------------------

bp_body = TudorBody()
bp_body.length = 150
bp_body.width = 100

bp_body.x_styles = [None,"right","left","right","left"]
bp_body.y_styles = ["cross","left","right","cross"]

bp_body.split_divide_height = 0
bp_body.panel_length = 25
bp_body.panel_width = 2.5
bp_body.panel_space = 2

bp_body.make()
ex_tudor_body = bp_body.build()

scene = scene.union(ex_tudor_body.translate((250,0,0)))
#show_object(ex_tudor_body.translate((250,0,0)))

#---------------------


bp_body_stucco = StuccoBrickBody()

bp_body_stucco.seed = 'test2'
bp_body_stucco.length = 100
bp_body_stucco.make()

ex_body_stucco = bp_body_stucco.build()

scene = scene.union(ex_body_stucco.translate((-250,0,0)))
#show_object(ex_body_stucco.translate((-250,0,0)))

cq.exporters.export(scene,'stl/house_body_type.stl')

