from random import choice, randint

totalruns = 10000 # how many times to run sim
runs = totalruns

# sim options
newdiecost = 750
refreshopcost = 105

shoptions = [3, 5, 5, 2, 5, 1, 3, 5, 4, 1, 1, 5, 5, 5, 5, 3, 2, 3, 5, 5, 4, 4, 3, 3, 1, 2, 4, 1, 1, 1, 5, 3, 1, 5, 2, 2]
shoptioncosts = [100, 169, 167, 65 , 168, 47, 95, 168, 127, 48, 26, 160, 179, 156, 152, 106, 56, 90, 159, 158, 132, 121, 110, 104, 41, 74, 140, 41, 46, 46, 171, 102, 24, 180, 71, 67]

simscores = []
simlogs = []
currentsimlog = []

def log(string):
    global currentsimlog
    currentsimlog.append(string)
    print(string)

def init():
    global rolls, pnts, currentshop, die, buygoalindex, buygoalcost, freerefreshops, currentsimlog

    rolls = 2500
    pnts = 0
    currentshop = []
    die = [1, 2, 3, 4, 5, 6]
    buygoalindex = 0
    buygoalcost = 0
    freerefreshops = 1
    currentsimlog = []
    

def refreshop(free = False):
    global pnts, refreshopcost, currentshop, shoptions, refeshopcost, rolls
    
    if pnts < refreshopcost and not free:
        log("! Couldn't refreshop, not enough points")
        return
    currentshop = {}
    for i in range(0, 4):
        index = randint(0, len(shoptions)-1)
        currentshop[i] = index
    if not free:
        pnts -= refreshopcost
        log("Bought refreshop for "+str(refreshopcost)+", "+str(rolls)+" rolls left and have "+str(pnts)+" pnts")
    else:
        log("Used free refreshop, "+str(rolls)+" rolls left and have "+str(pnts)+" pnts")

def roll():
    global die, rolls, pnts
    val = choice(die)
    rolls -= 1
    pnts += val

def buyfromshop(itemindex):
    global shoptioncosts, currentshop, pnts, shoptions, die, rolls
    cost = shoptioncosts[currentshop[itemindex]]
    if pnts < cost:
        log("! Couldn't buy, not enough points")
        return
    inc = shoptions[currentshop[itemindex]]
    die[randint(0, 5)] += inc
    pnts -= cost
    log("Bought +"+str(inc)+" for "+str(cost)+", "+str(rolls)+" rolls left and have "+str(pnts)+" pnts")

def newbuygoal():
    global buygoalindex, buygoalcost, shoptioncosts, currentshop, newdiecost, refreshopcost
    buygoalindex = randint(0, 5) # 0-3 are shop items, 4 is new die, 5 is shop refresh
    if buygoalindex < 4:
        buygoalcost = shoptioncosts[currentshop[buygoalindex]]
        inc = shoptions[currentshop[buygoalindex]]
        log("Aiming to buy +"+str(inc)+" for "+str(buygoalcost))
    elif buygoalindex == 4:
        buygoalcost = newdiecost
        log("Aiming to buy new die upgrade for "+str(buygoalcost))
    elif buygoalindex == 5:
        buygoalcost = refreshopcost
        log("Aiming to buy refreshop for "+str(buygoalcost))
    
while runs:
    init() 
    refreshop(free=True)
    
    while True: # game loop
        # new buy goal
        newbuygoal()
        if buygoalindex == 5 and freerefreshops > 1:    # use a free refreshop if have one
            refreshop(free=True)
            freerefreshops -= 1

        # roll till enough pnts to buy
        while pnts < buygoalcost:
            roll()
            if not rolls % 100: # add free refreshop every 100 rolls
                freerefreshops += 1
                log("Gained a free refreshop")

        # buy
        if buygoalindex < 4:
            buyfromshop(buygoalindex)
            
        elif buygoalindex == 4:
            pnts -= newdiecost
            log("Bought new die upgrade for "+str(buygoalcost))
            break # end game loop
            
        elif buygoalindex == 5:
            refreshop()

    log("*** Finished sim run: "+str(pnts)+" points left and "+str(rolls)+" dice rolls left")
    simscores.append(rolls)
    simlogs.append(currentsimlog)
    runs -= 1

print("=== FINISHED "+str(totalruns)+" SIMS ===")

tuplesbigtosmol = sorted(set(zip(range(len(simscores)), simscores)), key=lambda tup: tup[1])
tuplesbigtosmol.reverse()

print("Final Dice rolls left sorted best to worst ('id-rolls'):")
print(', '.join("{}-{}".format(*score) for score in tuplesbigtosmol))

while True:
    inpint = 0
    inp = input("--- Enter a sim id to view logs for that run, or nothing to quit ---\n>>> ")

    if inp == "":
        print("Quitting...")
        break
    
    try:
        inpint = int(inp)
    except e:
        print("Didn't enter int or nothing...")
        continue

    if inpint > len(simlogs)-1:
        print("Didn't enter int within range...")
        continue

    print('\n'.join(" ~ {} - {}".format(*score) for score in enumerate(simlogs[inpint])))

