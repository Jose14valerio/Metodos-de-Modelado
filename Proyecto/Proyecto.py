#Jose Alexis Valerio Ramírez B77863
#Lucia Elizondo Sancho B72694

from ctypes.wintypes import LONG
from operator import index
import numpy as np
import random as  rd


def degenerate(lambd):
    return lambd

def markovian(lambd):
    if lambd==0:
        valor = -np.log(1-rd.random())/1
    else:
        valor = -np.log(1-rd.random())/lambd
    return valor


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
    def __init__(self, tipo_evento, proximidad_evento):
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
    
    def simulation(self, time_limit, initial_clients, maximun_arrivals):
        initial_time = 0
        cola_eventos = []
        clientes_perdidos = 0
        clientes_esperando = []
        clientes_atendidos = []
        servidores = []
        clientes_sistema = initial_clients
        clientes_llegados = 0
        if (maximun_arrivals == 0):
            maximun_arrivals = max

        servers = 0
        while servers < self.s:
            serv = Server(False,0)
            servidores.append(serv)
            servers = servers+1 

        while initial_time < time_limit:
            if(clientes_llegados < maximun_arrivals and clientes_sistema < self.lmax):
                if(self.arrival == "markovian"):
                    evento = event("NC", markovian(self.calculate_lamdb(clientes_sistema)))
                    cola_eventos.append(evento)
                    cliente = Client(markovian(self.calculate_lamdb(clientes_sistema)), markovian(self.calculate_mu(clientes_sistema))-markovian(self.calculate_lamdb(clientes_sistema)), markovian(self.calculate_mu(clientes_sistema)))
                    clientes_esperando.append(cliente)
                    clientes_sistema += 1
                    initial_time += markovian(self.calculate_lamdb(clientes_sistema))
                else: 
                    evento = event("NC", degenerate(self.calculate_lamdb(clientes_sistema)))
                    cola_eventos.append(evento)
                    cliente = Client(degenerate(self.calculate_lamdb(clientes_sistema)), degenerate(self.calculate_mu(clientes_sistema))-degenerate(self.calculate_lamdb(clientes_sistema)), self.calculate_mu(clientes_sistema))
                    clientes_esperando.append(cliente)
                    clientes_sistema += 1
                    initial_time += degenerate(self.calculate_lamdb(clientes_sistema))
            elif clientes_sistema == self.lmax:
                clientes_perdidos += 1

            






        
