import cadquery as cq
from cqfantasy.arch import arch
from cadqueryhelper import Base
from cadqueryhelper.shape import chevron

class VDoor(Base):
    def __init__(self):
        super().__init__()
        self.length:float = 30
        self.width:float = 5
        self.height:float = 75
        
        self.v_margin:float = 1
        self.v_width:float = 15
        self.v_intersect:float = 10
        
        self.door_chamfer:float = 0.5
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.arch:cq.Workplane|None = None
        self.v_top:cq.Workplane|None = None
        self.door_half:cq.Workplane|None = None
        
    def calculate_column_height(self) -> float:
        return (self.height)-self.length/2
    
    def make_outline(self):
        self.outline = (
            cq.Workplane("XY")
            .box(self.length, self.width+self.v_margin, self.height)
        )
        
    def make_arch(self):
        ex_arch = arch(
            self.length, 
            self.width, 
            self.height
        )
        self.arch = ex_arch
        
    def make_top_v(self):
        column_height = self.calculate_column_height()-self.v_intersect
        #log(f'{column_height=}')
        
        v_top = chevron(
          length=self.length,
          width=column_height,
          height=self.width+self.v_margin,
          inner_width=self.v_width,
          alt=False
        ).rotate((1,0,0),(0,0,0),90).translate((0,0,-self.height/2+column_height/2+self.v_intersect))
        
        self.v_top = v_top
        
    def make_bottom_v(self):
        column_height = self.calculate_column_height()-self.v_intersect
        #log(f'{column_height=}')
        
        v_bottom = chevron(
          length=self.length,
          width=column_height,
          height=self.width+self.v_margin,
          inner_width=self.v_width,
          alt=False
        ).rotate((1,0,0),(0,0,0),-90).translate((
            0,
            0,
            -self.height/2-column_height/2+self.v_intersect
        ))

        if self.outline:
            v_bottom = v_bottom.intersect(self.outline)
        
        self.v_bottom = v_bottom
        
    def make_door_half(self):
        door = cq.Workplane("XY")#.add(self.outline)
        
        if self.arch and self.outline:
            door = door.union(self.arch)
            door_half = door.intersect(self.outline.translate((-self.length/2,0,0)))
            
            if self.door_chamfer:
                door_half = door_half.faces(">X").edges(">Y or <Y").chamfer(self.door_chamfer)
            
        if self.v_top:
            door_half = door_half.union(self.v_top)
            
        if self.v_bottom:
            door_half = door_half.union(self.v_bottom)
            
        if self.outline:
            self.door_half = door_half.intersect(self.outline.translate((-self.length/2,0,0)))
        else:
            raise Exception("Unable for resolve VDoor outline.")
        #self.door_half = door_half
        
    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_arch()
        self.make_top_v()
        self.make_bottom_v()
        
        self.make_door_half()
        
    def build(self) -> cq.Workplane:
        super().build()
        scene = cq.Workplane("XY")#.add(self.outline)
        
        if self.door_half:
            scene = (
                scene
                .union(self.door_half)
                .union(self.door_half.rotate((0,0,1),(0,0,0),180))
            )
        
        return scene