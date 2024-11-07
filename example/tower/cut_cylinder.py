import cadquery as cq
from cqfantasy.tower import cut_cylinder

test_shape = cq.Workplane("XY").box(50,50,50)

test_shape = cut_cylinder(test_shape,40, 40)

#show_object(test_shape)

cq.exporters.export(test_shape, 'stl/tower_cut_cylinder.stl')