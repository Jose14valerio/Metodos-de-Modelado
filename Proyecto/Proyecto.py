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
		espera = 0
		if mu > lambd:
			espera = mu-lambd 
		else: 
			espera = lambd-mu
		cliente = Client(lambd, espera, mu)
		return cliente

	def simulation(self, time_limit, initial_clients, maximum_arrivals):
		initial_time = 0
		cola_eventos = []
		clientes_esperando = []
		clientes_atendidos = []
		servidores = []
		clientes_sistema = initial_clients
		clientes_llegados = 0
		if (maximum_arrivals == 0):
			maximum_arrivals = sys.maxsize


		servers = 0
		while servers < self.s:
			serv = Server(False,0)
			servidores.append(serv)
			servers = servers+1 

		lambd = 0

		while initial_time < time_limit:
			if(self.arrival == "markovian" and clientes_sistema < self.lmax):
				lambd = markovian(self.calculate_lamdb(clientes_sistema))
				mu = markovian(self.calculate_mu(clientes_sistema))
				cliente = self.new_client(lambd,mu)
				clientes_esperando.append(cliente)
				clientes_sistema += 1
				initial_time += lambd
			elif(self.arrival == "degenerate" and clientes_sistema < self.lmax):
				lambd = degenerate(self.calculate_lamdb(clientes_sistema))
				mu = degenerate(self.calculate_mu(clientes_sistema))
				cliente = self.new_client(lambd,mu)
				clientes_esperando.append(cliente)
				clientes_sistema += 1
				initial_time += lambd
				
			evento = event("NC", initial_time)
			cola_eventos.append(evento)

			clientes_llegados += 1

			eventos = 0
			prox_evento = event("NA", sys.maxsize)
			while (eventos < len(cola_eventos)):
				if(cola_eventos[eventos].proximidad_evento < prox_evento.proximidad_evento):
					prox_evento = cola_eventos[eventos]
				eventos += 1
			servidor = 0
			encontrado = False
			atendido = False
			if (prox_evento.tipo_evento == "NC"):
				while (servidor < len(servidores) and encontrado == False):
					if (servidores[servidor].ocupado == False):
						encontrado = True
						servidores[servidor].ocupado = True
						servidores[servidor].lurk_time += clientes_esperando[0].llegada
						index = cola_eventos.index(prox_evento)
						cola_eventos.remove(cola_eventos[index])
						evento = event("TA", clientes_esperando[0].salida)
						cola_eventos.append(evento)
						atendido = True
						initial_time += clientes_esperando[0].atencion 
				if(atendido == False):
					initial_time += clientes_esperando[0].llegada
			elif(prox_evento.tipo_evento == "TA"):
				clientes_atendidos.append(clientes_esperando[0])
				servidores[servidor].ocupado = False
				initial_time += clientes_esperando[0].salida
				clientes_esperando.remove(clientes_esperando[0])
				clientes_sistema -= 1
				
				if(initial_time < time_limit and clientes_sistema < self.lmax):
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
					evento = event("NC", initial_time)
					cola_eventos.append(evento)

					clientes_llegados += 1
		print("Clientes atendidos: " + str(len(clientes_atendidos)))
		print("Clientes perdidos: " + str(clientes_llegados-len(clientes_atendidos)))
		i = 0
		tiempo_atencion = 0
		while (i < len(clientes_atendidos)): 
			tiempo_atencion += clientes_atendidos[i].atencion
			i += 1
		tiempo_atencion = tiempo_atencion/len(clientes_atendidos) 
		print("El tiempo promedio de espera fue de " + str(tiempo_atencion))

		i = 0
		tiempo_salida = 0
		while (i < len(clientes_atendidos)): 
			tiempo_salida += clientes_atendidos[i].salida
			i += 1
		tiempo_salida = tiempo_salida/len(clientes_atendidos) 
		print("El tiempo promedio de atencion fue de " + str(tiempo_salida))

		i = 0 
		ocio = 0
		while (i < len(servidores)): 
			ocio += servidores[i].lurk_time
			i += 1
		ocio = ocio/len(servidores) 
		print("El tiempo ocio promedio fue de: " + str(ocio))
			
cola = Queue(15, 1, "markovian","64-n**1.5", "markovian","5+3n")
cola.simulation(1000,0,0)





		
