import cadquery as cq
from cqfantasy.house import StuccoBrickBody

bp_body_stucco = StuccoBrickBody()

bp_body_stucco.seed = 'test2'
bp_body_stucco.length = 100
bp_body_stucco.make()

ex_body_stucco = bp_body_stucco.build()

#show_object(ex_body_stucco)

cq.exporters.export(ex_body_stucco,'stl/house_body_stucco_brick.stl')