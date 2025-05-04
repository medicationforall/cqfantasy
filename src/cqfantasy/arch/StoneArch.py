import cadquery as cq
from . import BasicArch, arch

class StoneArch(BasicArch):
    def __init__(self):
        super().__init__()
        self.stone_count:int = 8
        self.stone_arch_count:int = 4
        
        self.stone_margin:float = .5
        self.width_margin:float = .5
        self.stone_modulus:int = 2
        self.outside_stone_position:int = 0
        self.stone_arch_modulus:int = 2
        self.outside_stone_arch_position:int = 1
        
        self.inside_stone:cq.Workplane|None = None
        self.outside_stone:cq.Workplane|None = None
        self.column_stones:cq.Workplane|None = None
        
        self.inside_arch_stone:cq.Workplane|None = None
        self.outside_arch_stone:cq.Workplane|None = None
        self.arch_stones:cq.Workplane|None = None
        
        self.margin_outline:cq.Workplane|None = None
        self.outside_margin_outline:cq.Workplane|None = None
        self.inside_margin_outline:cq.Workplane|None = None
        
    def calculate_stone_height(self) -> float:
        column_height = self.calculate_column_height()
        stone_height = column_height / self.stone_count
        return stone_height
    
    def calculate_stone_margin_height(self) -> float:
        stone_height = self.calculate_stone_height()
        return stone_height - self.stone_margin
    
    def calculate_arch_stone_height(self) -> float:
        perimeter = self.calculate_perimeter() / 2
        height = perimeter / self.stone_arch_count
        return height
    
    def calculate_arch_stone_margin_height(self) -> float:
        height = self.calculate_arch_stone_height() 
        return height - self.stone_margin
    
    def calculate_inside_arch_stone_height(self) -> float:
        perimeter = self.calculate_inside_perimeter() / 2
        height = perimeter / self.stone_arch_count
        return height
    
    def calculate_inside_arch_stone_margin_height(self) -> float:
        height = self.calculate_inside_arch_stone_height() 
        return height - self.stone_margin
    
    def calculate_outside_arch_stone_height(self) -> float:
        perimeter = self.calculate_outside_perimeter() / 2
        height = perimeter / self.stone_arch_count
        return height
    
    def calculate_outside_arch_stone_margin_height(self) -> float:
        height = self.calculate_outside_arch_stone_height() 
        return height - self.stone_margin
        
    def make_inside_stone(self):
        stone_height = self.calculate_stone_margin_height()
        self.inside_stone = cq.Workplane("XY").box(
            self.inside_margin,
            self.width,
            stone_height
        ).rotate((1,0,0),(0,0,0),90)
        
    def make_outside_stone(self):
        stone_height = self.calculate_stone_margin_height()
        length = self.inside_margin+self.outside_margin
        self.outside_stone = cq.Workplane("XY").box(
            length,
            self.width,
            stone_height
        ).translate((-length/2+self.inside_margin/2,0,0)).rotate((1,0,0),(0,0,0),90)
        
    def make_column_stones(self):
        def add_stone():
            count = 0
            def add_stone_count(loc:cq.Location) -> cq.Shape:
                nonlocal count
                stone = self.inside_stone
                
                if count % self.stone_modulus == self.outside_stone_position and self.outside_stone:
                    stone = (
                        self.outside_stone
                        .translate((
                            0,
                            0,
                            0)
                        )
                    )
                count += 1
                #log(f'test {count}')
                return stone.val().located(loc) #type:ignore
            return add_stone_count
        
        stone_height = self.calculate_stone_height()
        
        stones = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = stone_height, 
                ySpacing = stone_height,
                xCount = 1, 
                yCount= self.stone_count, 
                center = True)
            .eachpoint(add_stone())
        ).rotate((1,0,0),(0,0,0),90)
        
        self.column_stones = stones
        
    def make_margin_outline(self):
        self.margin_outline = arch(
            self.length-self.width_margin, 
            self.width-self.width_margin*2, 
            self.height
        )
        
    def make_outside_margin_outline(self):
        self.outside_margin_outline = arch(
            self.length+self.outside_margin*2, 
            self.width-self.width_margin*2,
            self.height+self.outside_margin
        ).translate((0,0,self.outside_margin/2))
        
    def make_inside_margin_outline(self):
        self.inside_margin_outline = arch(
            self.length-self.inside_margin*2+self.width_margin, 
            self.width-self.width_margin*2, 
            self.height-self.inside_margin
        ).translate((0,0,-self.inside_margin/2))
        
    def make_inside_arch_stone(self):
        height = self.calculate_arch_stone_margin_height()
        inside_height = self.calculate_inside_arch_stone_margin_height()
        
        pts = [
            (0,0),
            (0,height),
            (self.inside_margin,height-(height-inside_height)/2),
            (self.inside_margin,(height-inside_height)/2)
        ]
        
        stone = (
            cq.Workplane("XZ")
            .center(-self.inside_margin/2,-height/2)
            .polyline(pts)
            .close()
            .extrude(self.width)
            .translate((-self.length/2+self.inside_margin/2,self.width/2,0))
        )
        
        self.inside_arch_stone = stone
        
    def make_outside_arch_stone(self):
        length = self.inside_margin+self.outside_margin
        height = self.calculate_outside_arch_stone_margin_height()
        inside_height = self.calculate_inside_arch_stone_margin_height()
        inside_length = self.length-self.inside_margin*2
        
        pts = [
            (0,0),
            (0,height),
            (length,height-(height-inside_height)/2),
            (length,(height-inside_height)/2)
        ]
        
        stone = (
            cq.Workplane("XZ")
            .center(-length,-height/2)
            .polyline(pts)
            .close()
            .extrude(self.width)
            .translate((-inside_length/2,self.width/2,0))
        )

        self.outside_arch_stone = stone
        
    def make_arch_stones(self):
        rotate_degrees = 180 / self.stone_arch_count
        
        arch_stones = cq.Workplane("XY")
        for i in range(self.stone_arch_count+1):
            stone = cq.Workplane("XY")

            if self.inside_arch_stone:
                stone = self.inside_arch_stone
            
            if i % self.stone_arch_modulus == self.outside_stone_arch_position:
                stone = self.outside_arch_stone
            
            arch_stones.add(stone.rotate((0,1,0),(0,0,0),-rotate_degrees*i)) #type:ignore
            
        self.arch_stones = arch_stones
    
    def make(self, parent=None):
        super().make(parent)
        self.make_inside_stone()
        self.make_outside_stone()
        self.make_column_stones()
        
        self.make_margin_outline()
        self.make_outside_margin_outline()
        self.make_inside_margin_outline()
        
        self.make_inside_arch_stone()
        self.make_outside_arch_stone()
        self.make_arch_stones()
        
    def build(self) -> cq.Workplane:
        super().build()
        column_height = self.calculate_column_height()
        
        scene = (
            cq.Workplane("XY")
            #.add(self.outside_margin_outline)
            #.add(self.inside_stone)
            #.add(self.outside_stone)
            #.add(self.inside_arch_stone)
            #.add(self.outside_arch_stone)
            #.add(self.column_outline)
        )

        if self.margin_outline:
            scene = scene.add(self.margin_outline)

        if self.inside_margin_outline:
            scene = scene.cut(self.inside_margin_outline)

        if self.column_stones:
            scene = (
                scene
                .add(self.column_stones.translate((-self.length/2+self.inside_margin/2,0,-self.height/2+column_height/2)))
                .add(self.column_stones.translate((-self.length/2+self.inside_margin/2,0,-self.height/2+column_height/2)).rotate((0,0,1),(0,0,0),180))
            )

        if self.arch_stones and self.column_outline:
            arch_stones = (
                self.arch_stones.translate((0,0,self.height/2-self.length/2))
                .cut(self.column_outline)
            )
            scene = scene.add(arch_stones)

        return scene