#Jose Alexis Valerio Ramírez B77863
#Lucia Elizondo Sancho B72694
from operator import is_
import time
import math

# Taken from https://geekflare.com/prime-number-in-python/


def is_prime(n):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True


def good_abm(n):
    m = 3
    while m < n:
        m = m*3
    b = m/2
    b = int(b)
    while is_prime(b) == False:
        b += 1
    a = m/2
    a = int(a)
    while a % 3 != 0:
        a = a+1
    a = a+1
    return (a, b, m)


class CongruentialGenerator:
    def __init__(self, a, b, m):
        self.a = a
        self.b = b
        self.m = m
        self.x = int(time.time() * 1000)

    def seed(self, s):
        self.x = s

    def random(self):
        rand_num = (self.a * self.x + self.b) % self.m
        self.x = rand_num
        return (rand_num & 16383)/16384

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


def generar_mazo():
    mazo = []
    for i in ["Corazon", "Espada", "Diamante", "Trebol"]:
        for j in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            card = []
            card.append(i)
            card.append(j)
            mazo.append(card)
    return mazo


def mismo_palo(mano):
    cp = mano[0][0]
    contador = 0
    while contador < 5:
        if cp == mano[contador][0]:
            contador = contador+1
        else:
            contador = 6
    if contador == 5:
        if mano[0][1] == 1 and mano[4][1] == 13:
            aws = (True, 14)
        else:
            aws = (True, mano[4][1])
        return aws
    return (False, 0)


def escalera(mano):
    ca = mano[0][1]
    contador = 1
    if mano[0][1] == 1 and mano[4][1] == 13:
        mano[0][1] = 14
        mano.sort(key=lambda x: x[1])
        ca = mano[0][1]
    while contador < 5 and mano[contador][1]-ca == 1:
        ca = mano[contador][1]
        contador = contador+1
    if contador == 5:
        if mano[0][1] == 1 and mano[4][1] == 13:
            aws = (True, 14)
        else:
            aws = (True, mano[4][1])
        return aws
    return (False, 0)


def cuenta_rep(mano):
    val = [mano[0][1], mano[1][1], mano[2][1], mano[3][1], mano[4][1]]
    rev = []
    resp = []
    for x in val:
        if ((x, val.count(x)) in rev) == False:
            rev.append((x, val.count(x)))
    for x in rev:
        if x[1] > 1:
            if x[1] == 2:
                resp.append((x[0], "Doble"))
            if x[1] == 3:
                resp.append((x[0], "Trio"))
            if x[1] == 4:
                resp.append((x[0], "Poker"))
    if resp == []:
        resp.append((0, "Error"))
    return resp


def tipoMano(jugador):
    aux = jugador
    # Royal Flush
    mp = mismo_palo(aux)
    esc = escalera(aux)
    if mp[0] == True and esc[0] == True and esc[1] == 14:
        return (1, 1)

    # straight flush
    escalera1 = esc
    mismopalo = mp
    if escalera1[0] == True and mismopalo[0] == True:
        return (2, escalera1[1])
    # poker
    ptd = cuenta_rep(aux)
    if (ptd[0][1] == "Poker"):
        return (3, ptd[0][0])

    aux2 = [0, 0]
    if len(ptd) == 2:
        aux2 = [ptd[0][1], ptd[1][1]]
    else:
        if ptd[0][1] != "Error":
            aux2 = [ptd[0][1]]
    # full house
    if ("Trio" in aux2) and ("Doble" in aux2):
        asw = [4, ptd[aux2.index("Trio")][0], ptd[aux2.index("Doble")][0]]
        return asw

    # flush
    mismoP = mp
    if mismoP[0] == True:
        return (5, mismoP[1])

    # Straight
    if escalera1[0] == True and mismopalo[0] == False:
        return (6, escalera1[1])

    # trio
    if ("Trio" in aux2) and not ("Doble" in aux2):
        return (7, ptd[0][0])

    # 2 pair
    if aux2.count("Doble") == 2:
        ans = [8, ptd[0][0], ptd[1][0]]
        return ans

    # pair
    elif aux2.count("Doble") == 1:
        return (9, ptd[0][0])

    # mas alta
    if aux[0][1] == 1:
        return (10, 14)
    else:
        return (10, aux[4][1])


def compare_hands(player, opponent):
    player.sort(key=lambda x: x[1])
    opponent.sort(key=lambda x: x[1])
    mp = tipoMano(player)
    mo = tipoMano(opponent)
    if mp[0] < mo[0]:
        return "win"
    elif mp[0] > mo[0]:
        return "loss"
    elif mp[0] == mo[0]:
        if mp[0] == 1:
            return "tie"
        if mp[0] == 2 or mp[0] == 3 or mp[0] == 5 or mp[0] == 6 or mp[0] == 7:
            if mp[1] > mo[1]:
                return "win"
            elif mp[1] < mo[1]:
                return "loss"
            elif mp[1] == mo[1]:
                return "tie"
        if mp[0] == 4:
            if mp[1] > mo[1]:
                return "win"
            elif mp[1] < mo[1]:
                return "loss"
            elif mp[1] == mo[1]:
                if mp[2] > mo[2]:
                    return "win"
                elif mp[2] < mo[2]:
                    return "loss"
                elif mp[2] == mo[2]:
                    return "tie"
        if mp[0] == 8:
            if mp[1] > mo[1] and mp[1] > mo[2] or mp[2] > mo[1] and mp[2] > mo[2]:
                return "win"
            elif mp[1] < mo[1] and mp[2] < mo[1] or mp[1] < mo[2] and mp[2] < mo[2]:
                return "loss"
            ppa = 0
            ppb = 0
            poa = 0
            pob = 0
            if mp[1] > mp[2]:
                ppa = mp[1]
                ppb = mp[2]
            else:
                ppa = mp[2]
                ppb = mp[1]
            if mo[1] > mo[2]:
                poa = mo[1]
                pob = mo[2]
            else:
                poa = mp[2]
                pob = mp[1]
            if ppa > poa:
                return "win"
            elif ppa < poa:
                return "loss"
            elif ppa == poa:
                if ppb > pob:
                    return "win"
                elif ppb < pob:
                    return "loss"
                cap = 0
                for x in player:
                    if x[1] != ppa and x[1] != ppb:
                        cap = x[1]
                cao = 0
                for x in opponent:
                    if x[1] != poa and x[1] != pob:
                        cao = x[1]
                if cap > cao:
                    return "win"
                elif cap < cao:
                    return "loss"
                elif cap == cao:
                    return "tie"
        if mp[0] == 9:
            if mp[1] > mo[1]:
                return "win"
            elif mp[1] < mo[1]:
                return "loss"
            elif mp[1] == mo[1]:
                npp = []
                for x in player:
                    if x[1] != mp[1]:
                        npp.append(x[1])
                npo = []
                for x in opponent:
                    if x[1] != mp[1]:
                        npo.append(x[1])
                j = -1
                while j > -4:
                    if npp[j] > npo[j]:
                        return "win"
                    elif npp[j] < npo[j]:
                        return "loss"
                    j = j-1
                return "tie"
        if mp[0] == 10:
            if mp[1] > mo[1]:
                return "win"
            elif mp[1] < mo[1]:
                return "loss"
            elif mp[1] == mo[1]:
                j = -1
                while j > -4:
                    if player[j] > opponent[j]:
                        return "win"
                    elif player[j] < opponent[j]:
                        return "loss"
                    j = j-1
                return "tie"


def simulate(initial_cards, rolls, generator):
    runs = 0
    ganadas = 0
    perdidas = 0
    empatadas = 0
    while runs < rolls:
        cartasRestantes = 52
        mazo = generar_mazo()
        jugador = []
        oponente = []
        carta1 = initial_cards[0]
        carta2 = initial_cards[1]
        if carta1[1] != 14:
            if initial_cards[1] == initial_cards[0]:
                mazo.pop(mazo.index(initial_cards[0]))
                cartasRestantes = cartasRestantes - 1
                print(carta1)
            else:
                mazo.pop(mazo.index(initial_cards[0]))
                mazo.pop(mazo.index(initial_cards[1]))
                cartasRestantes = cartasRestantes - 2
        jugador.append(carta1)
        jugador.append(carta2)
        oponente.append(carta1)
        oponente.append(carta2)

        while len(jugador) < 7:
            cartaGenerada = math.floor(generator.random()*cartasRestantes)
            cartasRestantes = cartasRestantes - 1
            cartaN = mazo[cartaGenerada]
            jugador.append(cartaN)
            mazo.pop(cartaGenerada)

        while len(oponente) < 7:
            cartaGenerada = math.floor(generator.random()*cartasRestantes)
            cartasRestantes = cartasRestantes - 1
            cartaN = mazo[cartaGenerada]
            oponente.append(cartaN)
            mazo.pop(cartaGenerada)

        mMJ = []
        for j in jugador:
            aux = []
            aux.append(j)
            for i in jugador:
                if j != i and len(aux) < 5:
                    aux.append(i)
            if mMJ == []:
                mMJ = aux
            else:
                if compare_hands(aux, mMJ) == True:
                    mMJ = aux

        mMO = []
        for j in oponente:
            aux = []
            mMO = []
            aux.append(j)
            for i in oponente:
                if j != i and len(aux) < 5:
                    aux.append(i)
            if mMO == []:
                mMO = aux
            else:
                if compare_hands(aux, mMO) == True:
                    mMO = aux

        if compare_hands(mMJ, mMO) == "win":
            ganadas = ganadas + 1
        elif compare_hands(mMJ, mMO) == "loss":
            perdidas = perdidas + 1
        elif compare_hands(mMJ, mMO) == "tie":
            empatadas = empatadas + 1

        runs = runs + 1

    empatadas = empatadas/rolls
    ganadas = ganadas/rolls
    perdidas = perdidas/rolls

    return (ganadas, empatadas, perdidas)


def main():
    abm = good_abm(10000001)
    generador = CongruentialGenerator(abm[0], abm[1], abm[2])
    print(generador.m)
    #print(generador.period())
    #se genera el mismo periodo y m (14348907)
    print(simulate([["Diamante",1],["Diamante",1]],100000, generador))
    #0.021 de ganar
    print(simulate([["Corazon",2],["Corazon",2]],100000, generador))
    #0.26 de ganar
    print(simulate([["Trebol",7],["Espada",7]],100000, generador))
    #0.48 de ganar

if __name__ == "__main__":
    main()
