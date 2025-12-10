from . import Fireplace, HearthTiledTwo, FireBoxTiled, FireTop, ChimneyTiled

class FireplaceTiled(Fireplace):
    def __init__(self):
        super().__init__()
        self.bp_hearth = HearthTiledTwo()
        self.bp_firebox = FireBoxTiled()
        self.bp_firebox.layers = 6
        
        self.bp_firetop = FireTop()
        self.bp_chimney = ChimneyTiled()
        self.bp_chimney.layers = 10
        
    def make(self):
        super().make()
        