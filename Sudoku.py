import sys
import math
import time
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Single cell
class SudokuCell(QLabel):
	
	def __init__(self, parent = None):
		super(QLabel, self).__init__(parent)
		self.elem = 0
		# font specification
		font = QFont()
		font.setPointSize(32)
		font.setBold(True)
		self.setFont(font)
		# configurations for the cell
		self.setAlignment(Qt.AlignCenter)
	
	def setElement(self, elem = 0):
		self.elem = elem
		self.setText(str(elem))

# The main UI
class SudokuDialog(QDialog):
	
	def __init__(self, parent = None):
		super(QDialog, self).__init__(parent)
		grid = QGridLayout()
		for i in range(9):
			for j in range(9):
				cell = SudokuCell()
				cell.setElement(random.randint(1, 9))
				grid.addWidget(cell, i, j)
		self.setLayout(grid)
		self.setWindowTitle("Sudoku Game by aaahexing")
		self.setFixedSize(500, 500)
	
def startGame():
	sudoku_app = QApplication(sys.argv)
	sudoku_dlg = SudokuDialog()
	sudoku_dlg.show()
	sudoku_app.exec()

if __name__ == "__main__":
	startGame()

