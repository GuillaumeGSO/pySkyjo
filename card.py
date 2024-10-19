class Card:
    def __init__(self, value: int, visible: bool=False, row: int = None, column: int = None):
        self.value: int = value        # Card value, from -2 to 12
        self.visible: bool = visible
        self.row: int = row
        self.column: int = column
        
    
    def __repr__(self) -> str:
        visibility = "Visible" if self.visible else "Hidden"
        column_info = f"Row {self.row}, Column {self.column}"
        return f"Card(value={self.value}, {visibility}, {column_info})"
