"""
This program does flood fill by replacing
a color at a target coordinate with a new
color. Like a fill bucket with paint.
Uses the BFS algorithm 

Name: Osayi Odiase
Date: 03/22/2025
CPSC42501 Artificial Intelligence
"""

from collections import deque

# Below lists detail all eight possible movements, directions
row = [-1, -1, -1, 0, 0, 1, 1, 1]
col = [-1, 0, 1, -1, 1, -1, 0, 1]

# check that the new_x/new_y are within the bounds of th row and col
# then also check that it's the color you want to replace
def isSafe(mat, n_x, n_y, old) -> bool:
	return 0 <= n_x < len(row) and 0 <= n_y < len(col) and mat[n_x][n_y] == old


# Flood fill using BFS
def floodfill(mat, x, y, replacement):
	# base case
	if not mat or not len(mat):
		return

	# color you will be replacing
	old = mat[x][y]

	# if the current collor you will be replacing 
	# is the new color
	if old == replacement:
		return mat
	
	# create queue
	queue = deque()
	queue.append((x, y))

	# replace the current/old color with the 
	# new replacement color
	mat[x][y] = replacement

	# -- BFS --
	# process all eight adjacent pixels 
	# of the current pixel and
	while queue:
		# get the first x and y
		curr_x, curr_y = queue.popleft()

		# iterate through the directions
		for k in range(len(row)):

			# 
			new_x,new_y = curr_x+row[k],curr_y+col[k]
			# get the target color
			
			if isSafe(mat, new_x, new_y, old):

				# replace the current pixel color with that of replacement
				mat[new_x][new_y] = replacement
				queue.append((new_x, new_y))


if __name__ == '__main__':

	# matrix showing portion of the screen having different colors
	mat = [
			['Y', 'Y', 'Y', 'G', 'G', 'G', 'G', 'G', 'G', 'G'],
			['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'G', 'X', 'X', 'X'],
			['G', 'G', 'G', 'G', 'G', 'G', 'G', 'X', 'X', 'X'],
			['W', 'W', 'W', 'W', 'W', 'G', 'G', 'G', 'G', 'X'],
			['W', 'R', 'R', 'R', 'R', 'R', 'G', 'X', 'X', 'X'],
			['W', 'W', 'W', 'R', 'R', 'G', 'G', 'X', 'X', 'X'],
			['W', 'B', 'W', 'R', 'R', 'R', 'R', 'R', 'R', 'X'],
			['W', 'B', 'B', 'B', 'B', 'R', 'R', 'X', 'X', 'X'],
			['W', 'B', 'B', 'X', 'B', 'B', 'B', 'B', 'X', 'X'],
			['W', 'B', 'B', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
		]

	# start node
	position = input("Enter the position you want to replace \nEx. 'W' is at (3,4) so type 3,4: ").strip()
	position = position.split(',')
	if len(position) != 2:
		print("Invalid position!")
		exit(1)
	x, y = (int(position[0]), int(position[1]))   # having a target color `Y`

	# replacement color
	replacement = input("Enter replacement color(what you want to replace with): ").strip()
	if not replacement:
		replacement = 'R'
	print(f"Replacing {mat[x][y]} with {replacement}")
	# replace the target color with a replacement color using DFS
	floodfill(mat, x, y, replacement)

	# the new mat with replaced color
	for r in mat:
		print(r)
