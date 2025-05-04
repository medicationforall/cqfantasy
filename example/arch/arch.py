import cadquery as cq
from cqfantasy.arch import arch

ex_arch = arch(
    length=30, 
    width=5, 
    height=75
)

#show_object(ex_arch)
cq.exporters.export(ex_arch, 'stl/arch_arch.stl')