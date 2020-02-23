from .enum_types import WireMode

class Grid:

    def __init__(self, width:int, height: int, wire_mode: WireMode = WireMode.LTR):
        self.width = width
        self.height = height
        self.wire_mode = wire_mode

    def test_position(self, x:int, y:int) -> bool:
        return x >=0 and y >= 0 and x < self.width and y < self.height

    def adjust_column(self, x:int) -> int:
        if x >= self.wire_mode:
            raise ValueError("x value aut of range")

        if self.wire_mode == WireMode.ZIGZAG and x & 1 == 1:
            # Odd Column and ZIGZAG wiring
            return self.width - x - 1
        return x   

    def position_to_index(self, x:int, y:int) -> int:
        return y*self.width + self.adjust_column(x)

    def index_to_position(self, index: int) -> int:
        if index < 0:
            raise ValueError("Index must be a positive value.")

        y = index // self.width
        x = self.adjust_column(index % self.width)
        if self.test_position(x,y):
            return (x,y)
        
        raise ValueError("Cannot convert index to position.")
