import sys
import math
import time
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Configurations of apperance
# Basic theme
class SudokuTheme:
	# Empty cells
	empty_ss = (
		'background-color: rgb(255, 255, 255);'
		'color: rgb(255, 255, 255);'
	)
	# In-focus empty cells
	focus_empty_ss = (
		'background-color: rgb(255, 245, 225);'
		'color: rgb(255, 245, 225);'	
	)
	# Static cell (pre generated)
	static_ss = (
		'background-color: rgb(211, 211, 211);'
		'color: rgb(0, 0, 0);'
		'font-size: 25pt; font-family: "consolas";'
	)
	# Dynamic cell (user specified)
	dynamic_ss = (
		'background-color: rgb(255, 255, 255);'
		'color: rgb(0, 0, 0);'
		'font-size: 25pt; font-family: "consolas";'
	)
	# In-focus dynamic cells
	focus_dynamic_ss = (
		'background-color: rgb(255, 245, 225);'
		'color: rgb(0, 0, 0);'
		'font-size: 25pt; font-family: "consolas";'		
	)
	# Widget's background color
	background_ss = (
		'background-color: rgb(41, 44, 51);'
	)
	# Style sheet of buttons
	button_ss = (
		'background-color: rgb(211, 211, 211);'
		'border: 2px groove; border-radius: 10px; padding: 2px 4px;'
		'font-size: 10pt;'
	)

# Single cell (square)
class SudokuCell(QLabel):
	#
	def __init__(self, elem = 0, theme = SudokuTheme(), parent = None):
		super(QLabel, self).__init__(parent)
		# Init element
		self.elem = elem
		self.static = (elem > 0)
		self.setText(str(self.elem))
		# Load theme
		self.theme = theme
		# Color the cells
		self.colorCell()
		# Configurations for the cell
		self.setAlignment(Qt.AlignCenter)
		# Make the cell always a square
		self.setFixedSize(60, 60)

	#
	def colorCell(self):
		if (self.isStatic()):
			self.setStyleSheet(self.theme.static_ss)
		elif (self.isEmpty()):
			if (not self.hasFocus()):
				self.setStyleSheet(self.theme.empty_ss)
			else:
				self.setStyleSheet(self.theme.focus_empty_ss)
		else:
			if (not self.hasFocus()):
				self.setStyleSheet(self.theme.dynamic_ss)
			else:
				self.setStyleSheet(self.theme.focus_dynamic_ss)

	# Update the number of current cell
	def setElement(self, elem = 0):
		if (not self.isStatic()):
			self.elem = elem
			# Emit the corresponding signal to notify the parent-class
			self.emit(SIGNAL('elementChanged(PyQt_PyObject)'), self)
		self.setText(str(self.elem))			
		self.colorCell()

	#
	def isEmpty(self):
		return self.elem == 0

	#
	def isStatic(self):
		return self.static

	#
	def getElement(self):
		return self.elem

	#
	def focusInEvent(self, event):
		self.colorCell()

	def focusOutEvent(self, event):
		self.colorCell()

	# Mouse input
	def mouseReleaseEvent(self, event):
		if (not event.button() == Qt.LeftButton):
			# Clear the index
			self.setElement(0)

	# Keyboard input
	def keyPressEvent(self, event):
		if (event.key() == Qt.Key_Escape):
			self.emit(SIGNAL('quitGame(PyQt_PyObject)'), self)
		elif (event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9):
			self.setElement(event.key() - Qt.Key_0)

# The main UI
class SudokuDialog(QDialog):
	#
	def __init__(self, level = 0, theme = SudokuTheme(), parent = None):
		super(QDialog, self).__init__(parent)
		self.level = level
		self.theme = theme
		# Configure the windows
		self.configure()
		# Start the game
		self.newGame()

	#
	def configure(self):
		# Initialize the windows attributes
		self.setWindowTitle("Sudoku Game by aaahexing")
		# Configurations of layouts
		self.grid_layout = QGridLayout()
		self.grid_layout.setSpacing(3)
		# outer 3 x 3
		for gi in range(3):
			for gj in range(3):
				layout = QGridLayout()
				layout.setSpacing(1)
				self.grid_layout.addLayout(layout, gi, gj)
		# Create three buttons
		self.new_button = QPushButton('New Game')
		self.new_button.setStyleSheet(self.theme.button_ss)
		self.connect(self.new_button, SIGNAL('clicked()'), self.newGame)
		self.restart_button = QPushButton('Restart')
		self.restart_button.setStyleSheet(self.theme.button_ss)
		self.connect(self.restart_button, SIGNAL('clicked()'), self.restartGame)
		self.solution_button = QPushButton('Solution')
		self.solution_button.setStyleSheet(self.theme.button_ss)
		self.connect(self.solution_button, SIGNAL('clicked()'), self.fillSolution)
		# The panel layout
		self.panel_layout = QHBoxLayout()
		self.panel_layout.addStretch()
		self.panel_layout.addWidget(self.new_button)
		self.panel_layout.addSpacing(10)
		self.panel_layout.addWidget(self.restart_button)
		self.panel_layout.addSpacing(10)
		self.panel_layout.addWidget(self.solution_button)
		self.panel_layout.addStretch()
		# The main layout
		self.main_layout = QVBoxLayout()
		self.main_layout.addLayout(self.grid_layout)
		self.main_layout.addSpacing(5)
		self.main_layout.addLayout(self.panel_layout)
		self.setLayout(self.main_layout)

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
				cell = SudokuCell(knows[i * 9 + j], self.theme)
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
					self.grid[index] = SudokuCell(0, self.theme)
					break
		# Backup all the elements
		self.backup_elements = []
		for i in range(81):
			self.backup_elements.append(self.grid[i].getElement())

	# Fill the elements
	def fillGrids(self):
		# Get the global grid-layout
		grid_layout = self.grid_layout
		# Fill the elements
		for i in range(9):
			for j in range(9):
				inner_layout = self.grid_layout.itemAtPosition(i // 3, j // 3)
				cell = self.grid[i * 9 + j]
				inner_layout.addWidget(cell, i % 3, j % 3)
				self.connect(cell, SIGNAL('elementChanged(PyQt_PyObject)'), self.update)
				self.connect(cell, SIGNAL('quitGame(PyQt_PyObject)'), self.quit)
				cell.setFocusPolicy(Qt.StrongFocus)

	#
	def newGame(self):
		#
		self.generatePuzzle()
		# Fill all the cells
		self.fillGrids()
		# Update the appearance
		self.update()

	def restartGame(self):
		#
		for i in range(81):
			self.grid[i] = SudokuCell(self.backup_elements[i], self.theme)
		# Fill all the cells
		self.fillGrids()
		# Update the appearance
		self.update()

	def fillSolution(self):
		print('Solution not implemented.')
	
	# Main loop of current game
	def update(self):
		# Update the appearance of the grids
		self.setStyleSheet(self.theme.background_ss)
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

	# Quit game
	def quit(self):
		self.close()

	#
	def keyPressEvent(self, event):
		if (event.key() == Qt.Key_Escape):
			self.quit()
		elif (event.key() == Qt.Key_F2):
			self.newGame()		

def startGame():
	sudoku_app = QApplication(sys.argv)
	sudoku_dlg = SudokuDialog()
	sudoku_dlg.show()
	sudoku_app.exec()

if __name__ == "__main__":
	startGame()

