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

	def generar_mazo(self):
		mazo = []
		for i in ["corazon", "espada", "diamante", "trebol"]:
			for j in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
				card = []
				card.append(i)
				card.append(j)
				mazo.append(card)
		return mazo

	def mismo_palo(self, mano):
		# ["corazon", "espada", "diamante", "trebol"]
		contador = 0
		palo = mano[contador][0]
		mismo_palo = False 
		while contador < 5:
			if mano[contador][0] == palo:
				mismo_palo = True
				contador += 1
			else:
				mismo_palo = False
				contador = 6

		return mismo_palo

	def escalera(self, mano):
		return

	def compare_hands(self, player, opponent):

		return

def simulate(initial_cards, rolls, generator):
	return