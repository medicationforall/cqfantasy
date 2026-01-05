# Copyright 2025 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        