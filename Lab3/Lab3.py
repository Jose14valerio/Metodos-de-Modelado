#Jose Alexis Valerio Ramírez B77863
#Lucia Elizondo Sancho B72694

from genericpath import exists

import numpy as np
from csv import reader
import random


class pokeGenerador:

    def loadwords(filename):        
        nombres=[]
        # open file
        with open(filename, "r") as my_file:
            # pass the file object to reader()
            file_reader = reader(my_file)
            # do this for all the rows
            for row in file_reader:
                # print the rows
                nombres.append(row[0])
        return nombres
    
    def add_decorators(words, decorator, n):
        decoradas=[]
        dec = ""
        count = 0
        while count < n:
            dec = dec+decorator
            count = count+1

        for word in words:
            palabra = ""
            palabra = dec+word+dec            
            decoradas.append(palabra)
        return decoradas

    def get_secuences(words, n):
        list_secuencias=[]
        for i in words:
            q=0
            while q <= len(i)-n:
                if not i[q:q+n] in list_secuencias:
                    list_secuencias.append(i[q:q+n])
                q=q+1
        list_secuencias.sort()
        return list_secuencias
    
    def secuenciador(word,size):
        secuencias=[]
        q=0
        while q <= len(word)-size:
            secuencias.append(word[q:q+size])
            q=q+1
        return secuencias

    def decorador(word, decorator, n):
        i=0
        dec=""
        while i < n:
            dec=dec+decorator
            i=i+1
        return dec+word+dec
    
    def calculate_transitions(words, sequences):
        matriz = np.zeros((len(sequences),len(sequences)))
        size=len(sequences[0])
        for i in words:
            fragmento=pokeGenerador.secuenciador(i,size)
            j=0
            while j <len(fragmento)-1:
                f=sequences.index(fragmento[j])
                c=sequences.index(fragmento[j+1])
                matriz[f][c]=matriz[f][c]+1
                j=j+1
        for f in range(len(matriz)):
            div=0
            for c in matriz[f]:
                div=div+c
            if div>0:
                matriz[f][:] = matriz[f][:]/div
        return matriz            

    def create_model(words, ngrams):
        decoradas=pokeGenerador.add_decorators(words, "$", 1)
        secuencias=pokeGenerador.get_secuences(decoradas,ngrams)
        matriz=pokeGenerador.calculate_transitions(decoradas,secuencias)
        return tuple((matriz,secuencias))

    def generate_word(model, seed):
        nueva_palabra=""
        matriz=model[0]
        secuencias=model[1]
        r = random.Random(seed)
        celda=0
        for i in secuencias:
            if i[0] == "$":
                celda=celda+1
        celda=r.randint(0,celda)
        nueva_palabra= nueva_palabra+secuencias[celda]
        while nueva_palabra[-1] != "$" or len(nueva_palabra) == 1: 
            valor= r.random()
            buscando=True
            c=0
            while buscando and c<len(secuencias):
                if matriz[celda][c]<valor:
                    c=c+1
                else:
                    nueva_palabra=nueva_palabra+secuencias[c][-1]
                    buscando=False
                    celda=c
        return nueva_palabra

    def get_probability(model, word):
        palabra_decorada=pokeGenerador.decorador(word, "$", 1)
        matriz=model[0]
        secuencias = model[1]
        celda=0
        for i in secuencias:
            if i[0] == "$":
                celda=celda+1
        probabilidad=1/celda
        fragmentos = pokeGenerador.secuenciador(palabra_decorada,len(secuencias[0]))
        fila=secuencias.index(fragmentos[0])
        for i in fragmentos:
            if i[0] !="$":
                columna=secuencias.index(i)
                probabilidad=probabilidad*matriz[fila][columna]
                fila=columna
        return probabilidad


nombres = pokeGenerador.loadwords("pokemon.csv")

tupla = pokeGenerador.create_model(nombres,3)

nueva_palabra = pokeGenerador.generate_word(tupla,15)

proba = pokeGenerador.get_probability(tupla,"Gible")

print(nueva_palabra)

"""
8.a Entre más grande sea la N, la secuencias son más grandes y por ende al juntarlas es más probable encontrar un nombre con sentido

8.b Encontramos Espeon con n=3 y seed = 21
nombres=pokeGenerador.loadwords("pokemon.csv")

tupla = pokeGenerador.create_model(nombres,3)

nueva_palabra= pokeGenerador.generate_word(tupla,21)

Xat n=2 seed=20

Regislash n=3 seed=9

Bar n=2 seed=2

Gible n=3 seed=15

8.c Para formar una palabra la secuencia siguente depende directamente de la probabilidad que tiene de relacionarse con la secuencia anterior 
(exceptuando el caso inicial que es aleatorio)

"""