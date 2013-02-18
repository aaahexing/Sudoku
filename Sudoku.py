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
		self.static = False
		# Configurations for the cell
		self.setAlignment(Qt.AlignCenter)

	# The index in the cell cannot be changed
	def setFixedElement(self, elem = 0):
		self.setElement(elem)
		self.static = True
	
	# Update the number of current cell
	def setElement(self, elem = 0):
		if (not self.static):
			self.elem = elem
			self.setText(str(elem))
			# Emit the corresponding signal to notify the parent-class
			self.emit(SIGNAL('elementChanged(PyQt_PyObject)'), self)

	#
	def isValid(self):
		return self.elem >= 1 and self.elem <= 9

	# Extend the 'QLabel' class with 'mouseReleaseEvent'
	def mouseReleaseEvent(self, event):
		if (event.button() == Qt.LeftButton):
			# Increase the index
			self.setElement((self.elem + 1) % 10)
		else:
			# Clear the index
			self.setElement(0)

# The main UI
class SudokuDialog(QDialog):
	#
	def __init__(self, level = 0, parent = None):
		super(QDialog, self).__init__(parent)
		# Initialize the windows attributes
		self.setWindowTitle("Sudoku Game by aaahexing")
		self.setFixedSize(500, 500)
		# Start the game
		self.level = level
		self.start()

	# Generate puzzle
	def generatePuzzle(self):
		self.grid = []
		for i in range(9):
			for j in range(9):
				cell = SudokuCell()
				cell.setElement(random.randint(0, 9))
				self.connect(cell, SIGNAL('elementChanged(PyQt_PyObject)'), self.checkGame)
				self.grid.append(cell)

	#
	def configure(self):
		# Configurations of layouts
		grid_layout = QGridLayout()
		grid_layout.setSpacing(3)
		self.setLayout(grid_layout)
		# outer 3 x 3
		for gi in range(3):
			for gj in range(3):
				base_i = gi * 3
				base_j = gj * 3
				layout = QGridLayout()
				layout.setSpacing(1)
				grid_layout.addLayout(layout, gi, gj)
				# inner 3 x 3
				for i in range(3):
					for j in range(3):
						cell = self.grid[(base_i + i) * 9 + (base_j + j)]
						layout.addWidget(cell, i, j)
		# Configurations of apperance
		self.background_ss = (
			'background-color: rgb(41, 44, 51);'
		)
		self.valid_ss = (
			'background-color: rgb(211, 211, 211);'
			'color: rgb(0, 0, 0);'
			'font-size: 25pt; font-family: "consolas";'
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
	def start(self):
		# Fill all the cells
		self.generatePuzzle()
		#
		self.configure()
		# Update the appearance
		self.update()
	
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


