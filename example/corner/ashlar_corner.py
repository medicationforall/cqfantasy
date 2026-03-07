import cadquery as cq
from cqfantasy.corner import AshlarCorner


bp_corner = AshlarCorner()
bp_corner.length = 20
bp_corner.width = 15
bp_corner.height = 75
bp_corner.stone_height = 75/9
bp_corner.chamfer = 1
bp_corner.corner_cut_length = 2
bp_corner.corner_cut_width = 2
bp_corner.make()

ex_corner = bp_corner.build()
ex_outline = bp_corner.build_outline()

ex_mirror = bp_corner.build_mirror()


scene = (
    cq.Workplane("XY")
    .union(ex_corner)
    .union(ex_corner.rotate((0,0,1),(0,0,0),180).translate((40,40,0)))
    .union(ex_mirror.translate((40,0,0)))
    .union(ex_mirror.rotate((0,0,1),(0,0,0),180).translate((0,40,0)))
)

#show_object(scene)
cq.exporters.export(scene, 'stl/corner_ashlarCorner.stl')