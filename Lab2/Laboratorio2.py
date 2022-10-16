from operator import is_
import time

# Taken from https://geekflare.com/prime-number-in-python/
def is_prime(n):
	for i in range(2,n):
		if ( n % i) == 0:
			return False
	return True


class CongruentialGenerator:
	def __init__(self, a,b,m):
		self.a = a
		self.b = b
		self.m = m
		self.x = int(time.time() * 1000)

	def seed(self,s):
		self.x = s

	def random(self):
		rand_num = (self.a * self.x + self.b) % self.m 
		rand_num = rand_num / 16384
		self.x = rand_num
	
	def period(self):
		a = []
		repetido = False
		periodo = 0
		while repetido == False:
			self.random()
			if self.x in a:
				repetido = True
			else:
				a.append(self.x)
				periodo += 1
		return periodo

	def good_abm(self, n):
		a = 0
		b = n+1
		m = n+1
		b_primo = False
		while is_prime(m) == False:
			m += 1
		while b <= m and b_primo == False:
			b = b+1
			if b > m:
				b_primo= is_prime(b)
		a =  self.random() * m  + 1
		return a,b,m 