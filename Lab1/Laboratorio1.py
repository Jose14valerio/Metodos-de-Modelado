#Jose Alexis Valerio Ramírez B77863
#Lucia Elizondo Sancho B72694

import numpy as np

def parse_equation(equation):
    diccionario= {}
    equa_split = equation.split()
    for i in equa_split:
        if i !=  "+":
            if i != "-":
                variable = i.split("x")
                variable[1] = "x" + variable[1]
                if variable[0] == '':
                    variable[0] = 1
                diccionario.update({variable[1]:float(variable[0])})
            else:
                equa_split[equa_split.index(i)+1]="-"+equa_split[equa_split.index(i)+1]

    return(diccionario) 

#print(parse_equation("-3.8x1 + 5x2 -2x3")) 

def parse_restriction(restriction):
    rest_split = []
    valor_rest = []
    if "<=" in restriction:
        rest_split = restriction.split("<=")
        valor_rest = [float(rest_split[1]), True]
    elif ">=" in restriction:
        rest_split = restriction.split(">=")
        valor_rest = [float(rest_split[1]), False]
    
    diccionario = parse_equation(rest_split[0])
    tupla = [diccionario,valor_rest]
    return(tupla)

#print(parse_restriction("-3.8x1 + 5x2 - 2x3 <= 35"))

def parse_problem(objetive, restrictions, maximize):
    obj_dic = parse_equation(objetive)
    list_rest=[]
    var_z=[]
    val_z=[]
    matriz=[]
    for i in restrictions:
        list_rest.append(parse_restriction(i))

    for x in obj_dic:
        var_z.append(x)
        val_z.append(obj_dic[x])

    index=0
    #ciclo para llenar Z
    for y in list_rest:
        index = index+1
        if y[1][1] == True:
          var_z.append("s"+str(index))
          val_z.append(0)
        elif y[1][1] == False:
            var_z.append("s"+str(index)) 
            var_z.append("a"+str(index))
            val_z.append(0)
            if maximize:
                val_z.append(-100000)
            else:
                val_z.append(100000)

    #Ciclo para llenar matriz
    i=0
    while i < len(list_rest):
        array_matriz=[]
        for x in var_z:
            if x in list_rest[i][0]:
                array_matriz.append(list_rest[i][0][x])
            else:
                if "x" in x:
                    array_matriz.append(0)
                elif "s"+str(i+1) in x and list_rest[i][1][1]==True:
                    array_matriz.append(1)
                elif "s"+str(i+1) in x and list_rest[i][1][1]==False:
                    array_matriz.append(-1)
                elif "a"+str(i+1) in x:
                    array_matriz.append(1)
                else:
                    array_matriz.append(0)
        array_matriz.append(list_rest[i][1][0])
        matriz.append(array_matriz)
        i=i+1
    
    return [val_z,matriz,var_z]

#print(parse_problem("30x1 + 100x2",["x1 + x2 <= 7","4x1 + 10x2 <= 40","10x1 >= 30"],True))


def simplex(objective, restrictions, variables, maximize):
    cb=[]
    var=[]
    b=[]
    z=objective
    matriz=[]
    z=np.array(z)
    zj=np.zeros(len(objective))
    z_zj=np.zeros(len(objective))

    #Preparar llena la matriz de var y cb
    i=0
    while i < len(restrictions):
        if "s"+str(i+1) in variables:
                if "a"+str(i+1) in variables:
                    cb.append(objective[variables.index("a"+str(i+1))])
                    var.append("a"+str(i+1))
                else:
                    cb.append(objective[variables.index("s"+str(i+1))])
                    var.append("s"+str(i+1))
        i+=1
    
    #Matriz
    for x in restrictions:
        index=0
        temporal=[]
        aux=len(x)-1
        while index < aux:
            temporal.append(x[index])
            index+=1
        matriz.append(temporal)
        b.append(x[-1])
    matriz=np.array(matriz)
    b=np.array(b)

    #Iterar
    while True:
        zj=calcular_zj(matriz,cb)   
        z_zj=z-zj
        min=z_zj.min()
        max=z_zj.max()
        columna_pivote=[]

        if maximize:    
            if min <= 0.0 and max <= 0.0:
                break
            else:
                cpi=np.where(z_zj==max)                
        else:
            if min >= 0.0 and max >= 0.0:
                break
            else:
                cpi=np.where(z_zj==min)
        cpi=cpi[0][0]
        for w in matriz:
            columna_pivote.append(w[cpi])
        columna_pivote=np.array(columna_pivote)
        ratio=np.zeros(len(b))
        with np.errstate(divide='ignore'):
            np.divide(b,columna_pivote,ratio)
        #buscar el ratio valido menor 
        i=0
        valor_fila_pivote=100000
        while i<len(ratio):
            if columna_pivote[i] > 0 and ratio[i]<valor_fila_pivote:
                valor_fila_pivote=ratio[i]
                fila_pivote=i
            i+=1

        divisor=np.full((1,len(matriz[0])),matriz[fila_pivote][cpi])
        aux=np.zeros(len(matriz[0]))
        np.divide(matriz[fila_pivote],divisor[0],aux)
        b[fila_pivote]=b[fila_pivote]/matriz[fila_pivote][cpi]
        matriz[fila_pivote]=aux
        
        for h in matriz:
            if not np.array_equal(h,matriz[fila_pivote]):
                l=h[cpi]
                bi=0
                while not np.array_equal(h,matriz[bi]):
                    bi+=1
                b[bi]=b[bi]-b[fila_pivote]*l
                aux=matriz[fila_pivote]*l
                aux2=h-aux
                matriz[bi]=aux2
        cb[fila_pivote]=z[cpi]
        var[fila_pivote]=variables[cpi]
    
    suma=np.sum(np.multiply(cb,b))
    valores=pares(var,cb,b)
    resp=(valores,suma)
    return resp

def calcular_zj(matrix,cb):
    g=0
    zj=[]
    while g < len(matrix[0]):
        i=0
        m=0
        x=0
        while m < len(cb):
            x+=(cb[m]*matrix[i][g])
            m+=1
            i+=1
        g+=1
        zj.append(x)
    zj=np.array(zj)
    return zj

def pares(var,cb,b):
    tupla=[]
    auxA=[]
    auxB=[]

    for letra in var:
        if letra[0]=="x":
            auxA.append(letra)
        else:
            auxB.append(letra)
    auxA.sort(key=lambda y: y[1])
    auxB.sort(key=lambda y: y[1])

    for letra in auxA:
        bround=round(b[var.index(letra)], 3)
        tupla.append((letra,bround))
    for letra in auxB:
        bround=round(b[var.index(letra)], 3)
        tupla.append((letra,bround))    
    return tupla

def simplex_solver(objective, restrictions, maximize):
    problema=parse_problem(objective, restrictions, maximize)
    respuesta=simplex(problema[0], problema[1], problema[2], maximize)
    return respuesta

#print(simplex_solver("0.65x1 + 0.45x2", ["2x1 + 3x2 <= 400", "3x1 + 1.5x2 <= 300", "x1 <= 90"], True))
#print(simplex_solver("30x1 + 100x2", ["x1 + x2 <= 7", "4x1 + 10x2 <= 40", "10x1 >= 30"], True))
#print(simplex_solver("3x1 + 8x2", ["x1 + 4x2 >= 3.5" , "x1 + 2x2 >= 2.5"], False))


#Punto 6
#PL1 = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5"], True))
#respuesta = ([('x1', 3.8), ('x2', 3.0), ('s3', 1.2)], 15.8)

#PL2 = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 <= 3"], True))
#Respuesta = ([('x1', 3.0), ('x2', 2.6), ('s2', 8.0), ('s3', 2.0)], 13.4)

#PL3 = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 >= 4"], True))
#Respuesta = ([('x1', 4.0), ('x2', 2.9), ('s1', 4.0), ('s3', 1.0)], 15.6)

#PL4(proveniente de PL2) = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 <= 3", "x2 <= 2"], True))
#Respuesta = ([('x1', 3.0), ('x2', 2.0), ('s1', 12.0), ('s2', 14.0), ('s3', 2.0)], 11.0)

#PL5(proveniente de PL2) = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 <= 3", "x2 >= 3"], True))
#Respuesta = ([('x1', 3.0), ('x2', 2.6), ('s2', 8.0), ('s3', 2.0), ('a5', 0.4)], -39986.59999999999) (Ninguna solución factible)

#PL6(proveniente de PL3) = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 >= 4", "x2 <= 2"], True))
#Respuesta = ([('x1', 5.0), ('x2', 2.0), ('s1', 32.0), ('s2', 4.0), ('s4', 1.0)], 13.0)

#PL7(proveniente de PL3) = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 >= 4", "x2 >= 3"], True))
#Respuesta = ([('x1', 4.0), ('x2', 2.9), ('s1', 4.0), ('s3', 1.0), ('a5', 0.1)], -9984.400000000009) (Ninguna solución factible)

#la solucion al problema es:
#PL6(proveniente de PL3) = print(simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5", "x1 >= 4", "x2 <= 2"], True))
#Respuesta = ([('x1', 5.0), ('x2', 2.0), ('s1', 32.0), ('s2', 4.0), ('s4', 1.0)], 13.0)