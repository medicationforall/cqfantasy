import cadquery as cq

def arch(
        length:float = 30, 
        width:float = 5, 
        height:float = 75
    ) -> cq.Workplane:
    if length > height:
        raise Exception(f'{length=} is greater than {height=}')
    cylinder = cq.Workplane("XZ").cylinder(width, length/2)
    base = cq.Workplane("XY").box(length, width, height-length/2)
    
    combined_arch = (
        base
        .union(cylinder.translate((0,0,height/2-length/4)))
        .translate((0,0,-length/4))
    )
    return combined_arch