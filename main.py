word_list = []

f = open("words.txt", "r")
for line in f.readlines():
	word_list.append(line[:-1])
f.close()



import pygame
from string import ascii_lowercase
import random

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 100)
small_font = pygame.font.Font("freesansbold.ttf", 50)

width, height = 300, 300
screen = pygame.display.set_mode((width, height + 50))

grid = {}

def reset_grid():
	for x in range(3):
		for y in range(3):
			grid[x, y] = " "

reset_grid()
selected = [0, 0]


def generate_possible():
	ans = "".join(random.choice(word_list) for i in range(3))
	answer = ans
	ans = [char for char in ans]
	random.shuffle(ans)
	ans = "".join(ans)
	return ans, answer

possible, answer = generate_possible()


def draw_grid():
	for x in range(3):
		for y in range(3):
			rect = pygame.Rect(x * 100, y * 100, 100, 100)
			if ([x, y] == selected):
				pygame.draw.rect(screen, (200, 51, 51), rect)
			pygame.draw.rect(screen, (255, 255, 255), rect, 5)
			text = font.render(grid[x, y], True, (255, 255, 255))
			screen.blit(text, (x * 100 + 50 - text.get_rect().width / 2, y * 100 + 50 - text.get_rect().height / 2))



def check_victory():
	string = ""
	for x in range(3):
		for y in range(3):
			string += grid[y, x]
	if string[:3] in word_list and string[3:6] in word_list and string[6:] in word_list:
		return True
	return False



running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			break

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseX = pygame.mouse.get_pos()[0]
			mouseY = pygame.mouse.get_pos()[1]
			selected = [mouseX // 100, mouseY // 100]

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				selected[1] = min(2, selected[1] + 1)
			if event.key == pygame.K_UP:
				selected[1] = max(0, selected[1] - 1)
			if event.key == pygame.K_RIGHT:
				selected[0] = min(2, selected[0] + 1)
			if event.key == pygame.K_LEFT:
				selected[0] = max(0, selected[0] - 1)
			if chr(event.key) in possible:
				if not grid[selected[0], selected[1]] == " ":
					possible += grid[selected[0], selected[1]]

				grid[selected[0], selected[1]] = chr(event.key)
				if selected[0] == 2:
					if (not selected[1] == 2):
						selected[0] = 0
					selected[1] = min(2, selected[1] + 1)
				else:
					selected[0] += 1

				possible = possible.replace(chr(event.key), "", 1)
				if len(possible) == 0 and check_victory():
					reset_grid()
					possible, answer = generate_possible()

			if event.key == pygame.K_BACKSPACE:
				if not grid[selected[0], selected[1]] == " ":
					possible += grid[selected[0], selected[1]]
					grid[selected[0], selected[1]] = " "

			if event.key == pygame.K_SPACE:
				for x in range(3):
					for y in range(3):
						grid[x, y] = answer[x + y * 3]
				possible = ""
				if check_victory():
					reset_grid()
					possible, answer = generate_possible()


	screen.fill((255, 51, 51))

	draw_grid()
	text = small_font.render(possible, True, (255, 255, 255))
	screen.blit(text, (0, height))

	pygame.display.update()


