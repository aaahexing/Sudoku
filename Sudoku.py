import sys
import math
import time
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Single cell
class SudokuCell(QLabel):
	#
	def __init__(self, elem = 0, parent = None):
		super(QLabel, self).__init__(parent)
		self.elem = elem
		self.static = (elem > 0)
		self.setText(str(self.elem))
		# Configurations for the cell
		self.setAlignment(Qt.AlignCenter)

	# Update the number of current cell
	def setElement(self, elem = 0):
		if (not self.static):
			self.elem = elem
			# Emit the corresponding signal to notify the parent-class
			self.emit(SIGNAL('elementChanged(PyQt_PyObject)'), self)
		self.setText(str(self.elem))

	#
	def isEmpty(self):
		return self.elem == 0

	#
	def isStatic(self):
		return self.static

	#
	def getElement(self):
		return self.elem

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
		self.setFixedSize(600, 600)
		# Set the layout
		self.configure()
		# Start the game
		self.level = level
		self.start()

	#
	def configure(self):
		# Configurations of layouts
		grid_layout = QGridLayout()
		grid_layout.setSpacing(3)
		self.setLayout(grid_layout)
		# outer 3 x 3
		for gi in range(3):
			for gj in range(3):
				layout = QGridLayout()
				layout.setSpacing(1)
				grid_layout.addLayout(layout, gi, gj)
		# Configurations of apperance
		self.background_ss = (
			'background-color: rgb(41, 44, 51);'
		)
		# Empty cells
		self.empty_ss = (
			'background-color: rgb(255, 255, 255);'
			'color: rgb(255, 255, 255);'
		)
		# Static cell (pre generated)
		self.static_ss = (
			'background-color: rgb(211, 211, 211);'
			'color: rgb(0, 0, 0);'
			'font-size: 25pt; font-family: "consolas";'
		)
		# Dynamic cell (user specified)
		self.dynamic_ss = (
			'background-color: rgb(255, 255, 255);'
			'color: rgb(0, 0, 0);'
			'font-size: 25pt; font-family: "consolas";'
		)

	# Generate puzzle using transformations on know solutions
	def simpleGen(self):
		knows = [4,2,9,3,1,6,5,7,8,
			 8,6,7,5,2,4,1,9,3,
			 5,1,3,8,9,7,2,4,6,
			 9,3,1,7,8,5,6,2,4,
			 6,8,2,9,4,1,7,3,5,
			 7,4,5,2,6,3,9,8,1,
			 3,5,4,6,7,2,8,1,9,
			 1,7,8,4,5,9,3,6,2,
			 2,9,6,1,3,8,4,5,7]
		self.grid = []
		for i in range(9):
			for j in range(9):
				cell = SudokuCell(knows[i * 9 + j])
				self.grid.append(cell)
		# Apply transformations
		for iter in range(random.randint(10, 20)):
			transform = random.randint(0, 3)
			if (transform == 0):
				# swap horizontally
				for i in range(4):
					for j in range(9):
						backup = self.grid[i * 9 + j]
						self.grid[i * 9 + j] = self.grid[(8 - i) * 9 + j]
						self.grid[(8 - i) * 9 + j] = backup
			elif (transform == 1):
				# swap vertically
				for j in range(4):
					for i in range(9):
						backup = self.grid[i * 9 + j]
						self.grid[i * 9 + j] = self.grid[i * 9 + (8 - j)]
						self.grid[i * 9 + (8 - j)] = backup
			elif (transform == 2):
				# swap diagonally
				for i in range(9):
					for j in range(i, 9):
						backup = self.grid[i * 9 + j]
						self.grid[i * 9 + j] = self.grid[j * 9 + i]
						self.grid[j * 9 + i] = backup
			else:
				# swap vice-diagonally
				for i in range(9):
					for j in range(i):
						backup = self.grid[i * 9 + j]
						self.grid[i * 9 + j] = self.grid[(8 - j) * 9 + (8 - i)]
						self.grid[(8 - j) * 9 + (8 - i)] = backup

	# Generate puzzle
	def generatePuzzle(self, method = 0, level = 0):
		if (method == 0):
			# Simplest method
			self.simpleGen()
		# Apply the specified difficulty: empty = 6 + level * 2
		empty = 7 + (level + 1) * 2
		for iter in range(empty):
			while (True):
				index = random.randint(0, 80)
				if (self.grid[index].isStatic()):
					self.grid[index] = SudokuCell(0)
					break
		# Get the global grid-layout
		grid_layout = self.layout()
		# Fill the elements
		for i in range(9):
			for j in range(9):
				inner_layout = grid_layout.itemAtPosition(i // 3, j // 3)
				# inner 3 x 3
				cell = self.grid[i * 9 + j]
				self.connect(cell, SIGNAL('elementChanged(PyQt_PyObject)'), self.update)
				inner_layout.addWidget(cell, i % 3, j % 3)

	#
	def start(self):
		# Fill all the cells
		self.generatePuzzle()
		# Update the appearance
		self.update()
	
	# Main loop of current game
	def update(self):
		# Update the appearance of the grids
		self.setStyleSheet(self.background_ss)
		for cell in self.grid:
			if (cell.isEmpty()):
				cell.setStyleSheet(self.empty_ss)
			elif (cell.isStatic()):
				cell.setStyleSheet(self.static_ss)
			else:
				cell.setStyleSheet(self.dynamic_ss)
		# Check the game status
		row = []
		col = []
		box = []
		for i in range(9):
			row.append(set())
			col.append(set())
			box.append(set())
		for i in range(9):
			for j in range(9):
				if (not self.grid[i * 9 + j].isEmpty()):
					elem = self.grid[i * 9 + j].getElement()
					row[i].add(elem)
					col[j].add(elem)
					box[(i // 3) * 3 + (j // 3)].add(elem)
		finish = True
		for i in range(9):
			if (len(row[i]) < 9 or len(col[i]) < 9 or len(box[i]) < 9):
				finish = False
				break
		if (finish):
			print("You win ^_^")

	# Event handlers
	def keyPressEvent(self, event):
		if (event.key() == Qt.Key_Escape):
			self.close()
		elif (event.key() == Qt.Key_F2):
			self.start()

def startGame():
	sudoku_app = QApplication(sys.argv)
	sudoku_dlg = SudokuDialog()
	sudoku_dlg.show()
	sudoku_app.exec()

if __name__ == "__main__":
	startGame()

