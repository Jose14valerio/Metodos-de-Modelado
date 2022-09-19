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


# [30.0, 100.0, 0, 0, 0, -100000.0],
#       [	[1, 1, 1, 0, 0, 0, 7.0],
# 			[4.0, 10.0, 0, 1, 0, 0, 40.0],
# 			[10.0, 0, 0, 0, -1, 1, 30.0]	],
#       	['x1', 'x2', 's1', 's2', 's3', 'a3'],
# 	True


def calcularZ_ZJ(Z_array, Z_ZJ_array):
	for i in range(len(Z_ZJ_array)):
		Z_ZJ_array[i] =  Z_array[i]-Z_ZJ_array[i] 
	return Z_ZJ_array

def calcularZj(matriz, cb):
	return ""

def simplex(objective, restrictions, variables, maximize):
	cb_array = []
	var_array = []
	Zj_array = []
	Z_ZJ_array = []
	
	valor_objetivo = 0

	for i in range(len(restrictions)):
		cb_array.append(0)

	for i in range(len(variables)):
		Zj_array.append(0)
		Z_ZJ_array.append(0)

	for i in range(2, len(variables)):
		var_array.append(variables[i])

	

	return ""

# print( simplex( [30.0, 100.0, 0, 0, 0, -100000.0],
# 				[	[1, 1, 1, 0, 0, 0, 7.0],
# 					[4.0, 10.0, 0, 1, 0, 0, 40.0],
# 					[10.0, 0, 0, 0, -1, 1, 30.0]	],
#       			['x1', 'x2', 's1', 's2', 's3', 'a3'],
# 	  			True
# ))
	

print( simplex (  [0.65, 0.45, 0, 0, 0], 
					[[2.0, 3.0, 1, 0, 0, 400.0], 
					[3.0, 1.5, 0, 1, 0, 300.0], 
					[1.0, 0, 0, 0, 1, 90.0]], 
					['x1', 'x2', 's1', 's2', 's3'], 
					True
				) 
)
