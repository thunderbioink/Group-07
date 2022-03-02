import pygame
from level import Level
from player import Player
import json
import random

class Quesion_Event:
	def __init__(self, level, player):
		question = self.pull_question()
		vecotrs = self.get_and_stop_movement(level, player)
		

	def pull_question():
		file = open('questions.json')
		questions = json.load(file)

		return questions[random(1, len(questions))]

	def get_and_stop_movement(level, player):
		world_shift = level.world_shift
		level.world_shift = 0
		speed = player.speed
		player.speed = 0
		gravity = player.gravity
		player.gravity = 0
		jump_speed = player.jump_speed
		player.jump_speed = 0

		return (world_shift, speed, gravity, jump_speed)

