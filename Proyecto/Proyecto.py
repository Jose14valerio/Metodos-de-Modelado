#Jose Alexis Valerio Ramírez B77863
#Lucia Elizondo Sancho B72694

from ctypes.wintypes import LONG
from operator import index
import numpy as np
import random as  random
import sys
import math

def degenerate(lambd):
	return lambd

def markovian(lambd):
	if lambd <= 0:
		return (-1)*math.log(1 - random.random())
	else:
		return (-1 / lambd)*math.log(1 - random.random())


class Client:
	def __init__(self, llegada, atencion, salida):
		self.llegada = llegada
		self.atencion = atencion
		self.salida = salida


class Server:
	def __init__(self, ocupado, lurk_time): 
		self.ocupado = ocupado
		self.lurk_time = lurk_time


class event:
	def __init__(self, tipo_evento, proximidad_evento, s = 0):
		self.s = s
		self.tipo_evento = tipo_evento
		self.proximidad_evento = proximidad_evento

	
class Queue:
	def __init__(self, lmax, s, arrival, lambd, service, mu):
		self.lmax = lmax
		self.s = s
		self.arrival = arrival
		self.lambd = lambd
		self.sevice = service
		self.mu = mu

	def calculate_lamdb(self, n):
		lambd = self.lambd.replace("n", str(n)) 
		return eval(lambd)

	def calculate_mu(self, n):
		mu = self.mu.replace("n", str(n)) 
		return eval(mu)
	
	def new_client(self, lambd, mu):
		cliente = Client(lambd, mu-lambd, mu)
		return cliente

	def simulation(self, time_limit, initial_clients, maximum_arrivals):
		initial_time = 0
		cola_eventos = []
		clientes_perdidos = 0
		clientes_esperando = []
		clientes_atendidos = []
		servidores = []
		clientes_sistema = initial_clients
		clientes_llegados = 0
		if (maximum_arrivals == 0):
			maximum_arrivals = sys.maxsize


		# Crean los servidores
		servers = 0
		while servers < self.s:
			serv = Server(False,0)
			servidores.append(serv)
			servers = servers+1 

		lambd = 0

		# Se puede atender clientes mientras la cola esté abierta (no se ha cerrado)
		while initial_time < time_limit:
			# Llega un cliente y lo pongo a esperar
			if(self.arrival == "markovian"):
				lambd = markovian(self.calculate_lamdb(clientes_sistema))
				mu = markovian(self.calculate_mu(clientes_sistema))
				cliente = self.new_client(lambd,mu)
				clientes_esperando.append(cliente)
				clientes_sistema += 1
				initial_time += lambd
			else:
				lambd = degenerate(self.calculate_lamdb(clientes_sistema))
				mu = degenerate(self.calculate_mu(clientes_sistema))
				cliente = self.new_client(lambd,mu)
				clientes_esperando.append(cliente)
				clientes_sistema += 1
				initial_time += lambd
				
			# Genera evento que llega cliente (NC)
			evento = event("NC", initial_time)
			cola_eventos.append(evento)

			clientes_llegados += 1
			
			# En algún momento Se verifica el evento siguiente
			eventos = 0
			prox_evento = event("NA", sys.maxsize)
			while (eventos < len(cola_eventos)):
				if(cola_eventos[eventos].proximidad_evento < prox_evento.proximidad_evento):
					prox_evento = cola_eventos[eventos]
				eventos += 1
			# Si NC no lo han atendido (sigue esperando)
				# Se suma el tiempo
			# Si TA se pone a atender 
				# se genera un nuevo NC si no se ha cerrado
			servidor = 0
			encontrado = False
			atendido = False
			if (prox_evento.tipo_evento == "NC"):
				while (servidor < len(servidores) and encontrado == False):
					if (servidores[servidor].ocupado == False):
						encontrado = True
						servidores[servidor].ocupado = True
						index = cola_eventos.index(prox_evento)
						cola_eventos.remove(cola_eventos[index])
						evento = event("TA", clientes_esperando[0].salida)
						atendido = True
				if(atendido == False):
					initial_time += clientes_esperando[0].llegada
			elif(prox_evento.tipo_evento == "TA"):
				clientes_atendidos.append(clientes_esperando[0])
				servidores[servidor].ocupado = False
				initial_time += clientes_esperando[0].salida
				clientes_esperando.remove(clientes_esperando[0])
				clientes_sistema -= 1
				if(initial_time < time_limit):
					if(self.arrival == "markovian"):
						lambd = markovian(self.calculate_lamdb(clientes_sistema))
						mu = markovian(self.calculate_mu(clientes_sistema))
						cliente = self.new_client(lambd,mu)
						clientes_esperando.append(cliente)
						clientes_sistema += 1
						initial_time += lambd
					else:
						lambd = degenerate(self.calculate_lamdb(clientes_sistema))
						mu = degenerate(self.calculate_mu(clientes_sistema))
						cliente = self.new_client(lambd,mu)
						clientes_esperando.append(cliente)
						clientes_sistema += 1
						initial_time += lambd
					# Genera evento que llega cliente (NC)
					evento = event("NC", initial_time)
					cola_eventos.append(evento)

					clientes_llegados += 1
					

			# Para atender el servidor tiene que estar desocupado
			# si LC y un servidor está D 
				# el servidor empieza a atender al cliente
				# se genera evento TA con el tiempo y el servidor que lo atendió 
				# el cliente sale del sistema 
				
			# Si todos estan ocupados, se pone el cliente a esperar
			
			
#self, lmax, s, arrival, lambd, service, mu):
cola = Queue(15, 1, "markovian","64-n**1.5", "markovian","5+3n")
cola.simulation(1000,0,0)





		
