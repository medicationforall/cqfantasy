import cadquery as cq

def make_magnet(diameter:float=3.2, height:float=2.4)->cq.Workplane:
    cut = cq.Workplane("XY").cylinder(height,diameter/2)
    return cut

def make_magnets(magnet:cq.Workplane, count:int=4, diameter:float=130):
    magnets = cq.Workplane("XY")
    degrees = 360 / count

    for i in range(count):
        magnets = magnets.union(magnet.translate((0,diameter/2,0)).rotate((0,0,1),(0,0,0),degrees*i))

    return magnets