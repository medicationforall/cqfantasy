import cadquery as cq
from cqfantasy.fence import BasicFence

bp_fence = BasicFence()
bp_fence.make()

ex_fence = bp_fence.build()

#show_object(ex_fence)

cq.exporters.export(ex_fence, 'stl/fence_basic_fence.stl')