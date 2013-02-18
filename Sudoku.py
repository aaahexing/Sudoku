import sys
import math
import time
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Single cell
class SudokuCell(QLabel):
	#
	def __init__(self, parent = None):
		super(QLabel, self).__init__(parent)
		self.elem = 0
		# Configurations for the cell
		self.setAlignment(Qt.AlignCenter)
	
	# Update the number of current cell
	def setElement(self, elem = 0):
		self.elem = elem
		self.setText(str(elem))

	def isValid(self):
		return self.elem >= 1 and self.elem <= 9

	# Extend the 'QLabel' class with 'mouseReleaseEvent'
	def mouseReleaseEvent(self, event):
		# Increase the index
		self.setElement(self.elem % 9 + 1)
		# Emit the corresponding signal to notify the parent-class
		self.emit(SIGNAL('elementChanged(PyQt_PyObject)'), self)

# The main UI
class SudokuDialog(QDialog):
	#
	def __init__(self, parent = None):
		super(QDialog, self).__init__(parent)
		# Initialize the windows attributes
		self.setWindowTitle("Sudoku Game by aaahexing")
		self.setFixedSize(500, 500)
		# Init the grids
		self.init()
		self.update()

	#
	def init(self):
		# Init the labels
		self.grid = []
		grid_layout = QGridLayout()
		self.setLayout(grid_layout)
		for i in range(9):
			for j in range(9):
				cell = SudokuCell()
				cell.setElement(random.randint(1, 9))
				self.grid.append(cell)
				grid_layout.addWidget(cell, i, j)
				self.connect(cell, SIGNAL('elementChanged(PyQt_PyObject)'), self.checkGame)
		# Init the appearence
		self.background_ss = 'background-color: rgb(41, 44, 51);'
		self.valid_ss = (
			'background-color: rgb(211, 211, 211);'
			'color: rgb(0, 0, 0);'
			'font: 20pt bold "Times New Roman";'
		)
		self.invalid_ss = (
			'background-color: rgb(255, 255, 255);'
			'color: rgb(255, 255, 255);'
		)
	
	# Update the appearance of the grids
	def update(self):
		self.setStyleSheet(self.background_ss)
		for cell in self.grid:
			if (cell.isValid()):
				cell.setStyleSheet(self.valid_ss)
			else:
				cell.setStyleSheet(self.invalid_ss)

	#
	def restart(self):
		self.init()
	
	# Check the status of current game
	def checkGame(self):
		self.update()

def startGame():
	sudoku_app = QApplication(sys.argv)
	sudoku_dlg = SudokuDialog()
	sudoku_dlg.show()
	sudoku_app.exec()

if __name__ == "__main__":
	startGame()


