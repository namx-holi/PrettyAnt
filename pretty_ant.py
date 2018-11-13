import tkinter as tk
import random



class Direction:
	N = ( 0, -1)
	E = ( 1,  0)
	S = ( 0,  1)
	W = (-1,  0)

	NE = ( 1, -1)
	NW = (-1, -1)
	SE = ( 1,  1)
	SW = (-1,  1)

	_DIRECTION_LIST = [N, NE, E, SE, S, SW, W, NW]

	@classmethod
	def rotate_direction(cls, direction, rotations):
		rotation_int = int(rotations * len(cls._DIRECTION_LIST))
		current_index = cls._DIRECTION_LIST.index(direction)

		next_index = (current_index + rotation_int) % len(cls._DIRECTION_LIST)
		return cls._DIRECTION_LIST[next_index]


	@classmethod
	def rand_direction(cls):
		return random.choice(cls._DIRECTION_LIST)

	@classmethod
	def rand_compass_direction(cls):
		return random.choice([
			cls.N,
			cls.E,
			cls.S,
			cls.W
		])



class Rotation:
	Right = 0.25
	Left = -0.25
	Straight = 0
	UTurn = 0.5



class Ruleset:

	def __init__(self):
		self._rules = []


	def add_rule(self, colour, rotations):
		self._rules.append(dict(colour=colour, rotations=rotations))


	def get_colours(self):
		return [rule["colour"] for rule in self._rules]


	def get_rotations(self, colour):
		try:
			current_index = self.get_colours().index(colour)
		except ValueError:
			current_index = 0

		return self._rules[current_index]["rotations"]


	def get_first_colour(self):
		return self._rules[0]["colour"]


	def get_next_colour(self, colour):
		try:
			current_index = self.get_colours().index(colour)
		except ValueError:
			return get_first_colour()

		next_index = (current_index + 1) % len(self._rules)
		return self._rules[next_index]["colour"]



class Grid:

	def __init__(self, width, height, ruleset):
		self._width = width
		self._height = height
		self._ruleset = ruleset

		self._ants = []

		# x along width
		# y along height
		self._squares = [[
				ruleset.get_first_colour()
				for y in range(height)
			] for x in range(width)]


	def get_width(self):
		return self._width


	def get_height(self):
		return self._height


	def get_squares(self):
		return self._squares


	def get_square_colour(self, x, y):
		return self._squares[x][y]


	def get_square_rotation(self, x, y):
		return self._ruleset.get_rotations(self.get_square_colour(x, y))


	def next_square_colour(self, x, y):
		next_colour = self._ruleset.get_next_colour(self.get_square_colour(x, y))
		self._squares[x][y] = next_colour


	def add_ant(self, x, y, direction):
		if x >= self._width:
			print("Ant x out of range. Set to 0.")
			x = 0
		if y >= self._height:
			print("Ant y out of range. Set to 0.")
			y = 0

		new_ant = Ant(x, y, direction, self)
		self._ants.append(new_ant)


	def step(self):
		for ant in self._ants:
			ant.step()



class Ant:

	def __init__(self, x, y, direction, grid):
		self._x = x
		self._y = y
		self._direction = direction
		self._grid = grid


	def step(self):
		# Get the rotation count
		rotations = self._grid.get_square_rotation(self._x, self._y)

		# Rotate
		next_direction = Direction.rotate_direction(self._direction, rotations)
		self._direction = next_direction

		# Change square colour
		self._grid.next_square_colour(self._x, self._y)

		# Move forward one
		delta_x, delta_y = self._direction
		new_x = (self._x + delta_x) % self._grid.get_width()
		new_y = (self._y + delta_y) % self._grid.get_height()
		self._x = new_x
		self._y = new_y



class GridDisplay(tk.Tk):

	def __init__(self, grid, scale):
		tk.Tk.__init__(self)

		self.grid = grid
		self.scale = scale

		self.initialise()


	def initialise(self):
		width  = self.grid.get_width()  * self.scale
		height = self.grid.get_height() * self.scale

		self.grid_canvas = tk.Canvas(self, width=width, height=height)
		self.grid_canvas.pack(fill=tk.BOTH, expand=True)


	def draw_grid(self):
		for y, row in enumerate(self.grid.get_squares()):
			for x, colour in enumerate(row):
				self.grid_canvas.create_rectangle(
					    x*self.scale,     y*self.scale, # Top left corner
					(x+1)*self.scale, (y+1)*self.scale, # Bot right corner
					outline=colour, fill=colour)



if __name__ == "__main__":

	width, height = 80, 80
	scale = 10

	# Create ruleset
	ruleset = Ruleset()
	ruleset.add_rule("#000000", Rotation.Right)
	ruleset.add_rule("#D60270", Rotation.Left)
	ruleset.add_rule("#9B4F96", Rotation.Straight)
	ruleset.add_rule("#0038A8", Rotation.UTurn)

	# Create grid
	grid = Grid(width, height, ruleset)

	# Add a few ants
	ant_count = 4
	for i in range(ant_count):
		x = random.randint(0, width-1)
		y = random.randint(0, height-1)
		direction = Direction.rand_compass_direction()

		grid.add_ant(x, y, direction)

	# Step a few times
	for i in range(10000):
		grid.step()

	# Draw!!
	app = GridDisplay(grid, scale)
	app.draw_grid()
	app.mainloop()
