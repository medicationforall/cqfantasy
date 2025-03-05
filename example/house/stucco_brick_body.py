import cadquery as cq
from cqfantasy.house import StuccoBrickBody

bp_body_stucco = StuccoBrickBody()

bp_body_stucco.seed = 'test2'
bp_body_stucco.length = 100
bp_body_stucco.render_stones= True
bp_body_stucco.cell_types = [
    'block',
    'block', 
    'empty',
    'block'
]

bp_body_stucco.block_length = 8
bp_body_stucco.block_width = 5
bp_body_stucco.block_height = 3
bp_body_stucco.block_spacing = 2
bp_body_stucco.make()

ex_body_stucco = bp_body_stucco.build()

#show_object(ex_body_stucco)

cq.exporters.export(ex_body_stucco,'stl/house_body_stucco_brick.stl')