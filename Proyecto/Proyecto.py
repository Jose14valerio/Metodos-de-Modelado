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

    
class Queue:
    def __init__(self, lmax, s, arrival, lambd, service, mu):
        self.lmax = lmax
        self.s = s
        self.arrival = arrival
        self.lambd = lambd
        self.sevice = service
        self.mu = mu
    
    def simulation(self, time_limit, initial_clients, maximun_arrivals):
        initial_time = 0
        cola_eventos = []
        clientes_perdidos = 0
        clientes_esperando = []
        clientes_atendidos = []
        servidores = []
        clientes_sistema = 0

        servers = 0
        while servers < Queue.s:
            serv = Server(False,0)
            servidores.append(serv)
            servers = servers+1 

        while initial_time < time_limit:
            initial_time = initial_time + markovian(Queue.lambd)
            #Tipos de evento Llegada de cliente (NC), Cliente en atención (CA), salida de cliente (SC)


