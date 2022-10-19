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
		for i in ["Corazon", "Espada", "Diamante", "Trebol"]:
			for j in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
				card = []
				card.append(i)
				card.append(j)
				mazo.append(card)
		return mazo

	def mismo_palo(self,mano):
		cp=mano[0][0]
		contador=0
		while contador<5:
			if cp==mano[contador][0]:  
				contador=contador+1
			else:
				contador=6
		if contador==5:
			if mano[0][1]==1 and mano[4][1]==13:
				aws=(True, 14)
			else:
				aws=(True, mano[4][1])
			return aws
		return (False,0)
	
	def escalera(self,mano):
        ca=mano[0][1]
        contador=1
        if mano[0][1]==1 and mano[4][1]==13:
            mano[0][1]=14
            mano.sort(key = lambda x: x[1])
            ca=mano[0][1]
        while contador<5 and mano[contador][1]-ca==1:
            ca=mano[contador][1]
            contador=contador+1
        if contador==5 :
            if mano[0][1]==1 and mano[4][1]==13:
                aws=(True, 14)
            else:
                aws=(True, mano[4][1])
            return aws
        return (False,0)

    def cuenta_rep(self,mano):
        val=[mano[0][1],mano[1][1],mano[2][1],mano[3][1],mano[4][1]]
        rev=[]
        resp=[]
        for x in val:
            if ((x,val.count(x)) in rev)==False:
                rev.append((x,val.count(x)))
        for x in rev:
            if x[1] > 1:
                if x[1]==2:
                    resp.append((x[0],"Doble"))
                if x[1]==3:
                    resp.append((x[0],"Trio"))
                if x[1]==4:
                    resp.append((x[0],"Poker"))
        print(resp)
        if resp==[]:
            resp.append((0,"Error"))
        return resp

    def tipoMano(self,jugador):
        aux=jugador
        #Royal Flush     
        mp=self.mismo_palo(aux)
        esc=self.escalera(aux)
        if mp[0]==True and esc[0]==True and esc[1]==14:
            print("Royal Flush")
            return (1, 1)

        #straight flush
        escalera=esc
        mismopalo=mp
        if escalera[0] == True and mismopalo[0]==True:
            print("Straight Flush")
            return (2, escalera[1])
        #poker
        ptd=self.cuenta_rep(aux)
        if (ptd[0][1]=="Poker"):
            print("Poker")
            return (3, ptd[0][0])
        
        aux2=[0, 0]
        if len(ptd)==2:
            aux2=[ptd[0][1], ptd[1][1]]
        else:
            if ptd[0][1] != "Error":
                aux2=[ptd[0][1]]
        #full house
        if("Trio" in aux2) and ("Doble" in aux2):
            asw=[4, ptd[aux2.index("Trio")][0], ptd[aux2.index("Doble")][0]]
            return asw
        
        #flush
        mismoP=mp
        if mismoP[0] == True:
            print("flush")
            return (5, mismoP[1]) 
        
        #Straight
        if escalera[0] == True and mismopalo[0]==False:
            print("straight")
            return (6, escalera[1])  
                
        #trio
        if("Trio" in aux2) and not ("Doble" in aux2):
            print("trio")
            return (7, ptd[0][0])

        #2 pair
        if aux2.count("Doble") == 2:
            print("doble doble")
            ans=[8, ptd[0][0], ptd[1][0]]
            return ans
        
        #pair
        elif aux2.count("Doble") == 1:
            print("Par")
            return (9, ptd[0][0])
    
        #mas alta
        print("mas alta")
        if aux[0][1]==1:
            return (10, 14)
        else:
            print(aux[4][1])
            return (10, aux[4][1])    


    def compare_hands(self,player , opponent):
        player.sort(key = lambda x: x[1])
        opponent.sort(key=lambda x: x[1])
        mp=self.tipoMano(player)
        mo=self.tipoMano(opponent)
        if mp[0]<mo[0]:
            return "win"
        elif mp[0]>mo[0]:
            return "loss"
        elif mp[0]==mo[0]:
            if mp[0] == 1:
                return "tie"
            if mp[0]==2 or mp[0]==3 or mp[0]==5 or mp[0]==6 or mp[0]==7:
                if mp[1]>mo[1]:
                    return "win"
                elif mp[1]<mo[1]:
                    return "loss"
                elif mp[1] == mo[1]:
                    return "tie"
            if mp[0]==4:
                if mp[1]>mo[1]:
                    return "win"
                elif mp[1]<mo[1]:
                    return "loss"
                elif mp[1]==mo[1]:
                    if mp[2]>mo[2]:
                        return "win"
                    elif mp[2] < mo[2]:
                        return "loss"
                    elif mp[2]==mo[2]:
                        return "tie"
            if mp[0]==8:
                if mp[1]>mo[1] and mp[1]>mo[2] or  mp[2]>mo[1] and mp[2]>mo[2]:
                    return "win"
                elif mp[1]<mo[1] and mp[2]<mo[1] or  mp[1]<mo[2] and mp[2]<mo[2]:
                    return "loss"
                ppa=0
                ppb=0
                poa=0
                pob=0
                if mp[1]>mp[2]:
                    ppa=mp[1]
                    ppb=mp[2]
                else:
                    ppa=mp[2]
                    ppb=mp[1]
                if mo[1]>mo[2]:
                    poa=mo[1]
                    pob=mo[2]
                else:
                    poa=mp[2]
                    pob=mp[1]
                if ppa>poa:
                    return "win"
                elif ppa<poa:
                    return "loss"
                elif ppa==poa:
                    if ppb>pob:
                        return "win"
                    elif ppb<pob:
                        return "loss"
                    cap=0
                    for x in player:
                        if x[1] != ppa and x[1] != ppb:
                            cap=x[1]
                    cao=0
                    for x in opponent:
                        if x[1] != poa and x[1] != pob:
                            cao=x[1]
                    if cap>cao:
                        return "win"
                    elif cap<cao:
                        return "loss"
                    elif cap==cao:
                        return "tie"
            if mp[0]==9:
                if mp[1]>mo[1]:
                    return "win"
                elif mp[1]<mo[1]:
                    return "loss"
                elif mp[1]==mo[1]:
                    npp=[]
                    for x in player:
                        if x[1] != mp[1]:
                            npp.append=x[1]
                    npo=[]
                    for x in opponent:
                        if x[1] != mp[1]:
                            npo.append=x[1]
                    j=-1
                    while j>-4:
                        if npp[j]>npo[j]:
                            return "win"
                        elif npp[j]<npo[j]:
                            return "loss"
                        j=j-1
                    return "tie"
            if mp[0]==10:
                if mp[1]>mo[1]:
                    return "win"
                elif mp[1]<mo[1]:
                    return "loss"
                elif mp[1]==mo[1]:
                    j=-1
                    while j>-4:
                        if player[j]>opponent[j]:
                            return "win"
                        elif player[j]<opponent[j]:
                            return "loss"
                        j=j-1
                    return "tie"

    def simulate(self,initial_cards, rolls, generator):
        runs = 0
        ganadas = 0
        perdidas = 0 
        empatadas = 0
        while runs < rolls:
            mazo = self.gen_mazo()
            jugador = []
            oponente = []
            carta1 = initial_cards[0]
            carta2 = initial_cards[1]
            jugador.append(carta1)
            jugador.append(carta2)
            oponente.append(carta1)
            oponente.append(carta2)
            mazo.pop(mazo.index(carta1))
            mazo.pop(mazo.index(carta2))

            while jugador.len() < 7:
                cartaN = mazo[generator]
                jugador.append[(cartaN)]
                mazo.pop[generator]
                self.m = self.m-1

            while oponente.len() < 7:
                cartaN = mazo[generator]
                oponente.append[(cartaN)]
                mazo.pop[generator]
                self.m = self.m-1

            mMJ = []
            for j in jugador:
                aux = []
                aux.append(j)
                for i in jugador:
                    if j != i and aux.len() < 5:
                        aux.append(i)
                if mMJ == []:
                    mMJ = aux
                else: 
                    if self.compare_hands(aux, mMJ) == True:
                        mMJ = aux
            
            mMO = []   
            for j in oponente:
                aux = []
                mMO = []
                aux.append(j)
                for i in oponente:
                    if j != i and aux.len() < 5:
                        aux.append(i)
                if mMO == []:
                    mMO = aux
                else: 
                    if self.compare_hands(aux, mMO) == True:
                        mMO = aux

            if self.compare_hands(mMJ, mMO) == "win":
                ganadas = ganadas + 1
            elif self.compare_hands(mMJ, mMO) == "loss":
                perdidas = perdidas + 1
            elif self.compare_hands(mMJ, mMO) == "tie":
                empatadas = empatadas + 1

            runs = runs + 1

        empatadas = empatadas/rolls
        ganadas = ganadas/rolls
        perdidas = perdidas/rolls

        return (ganadas, empatadas, perdidas)