import time
import random

class CongruentialGenerator:
	def __init__(self, a,b,m):
		self.a = a
		self.b = b
		self.m = m
		self.x = int(time.time() * 1000)

	def seed(s):
		s = random.seed(x)
		return s

	def random():
		rand_num = 0
		rand_num = random.randint(0,16384)
		rand_num = rand_num/16383 
		return rand_num
	
	def period():
		return ""