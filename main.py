import pygame
from copy import deepcopy
import numpy
import random
import math
import sys
import time
import json
import threading
from modules import saveS

pygame.init()
dx, dy = [600, 400]
sc = pygame.display.set_mode((dx * 2, dy * 2))
clockg = pygame.time.Clock()
pygame.mouse.set_visible(0)
font = pygame.font.Font(None, 20)
font_l = pygame.font.Font(None, 40)

mpx,mpy = [100,100]
smap = saveS.Map(mpx, mpy)
smap.open("save.json")

keyloc = {pygame.K_q:"and",pygame.K_w:"Bt",pygame.K_e:"cA",pygame.K_r:"cB",pygame.K_t:"st",pygame.K_y:"cl"}
x,y = [0,0]

with open('prog.txt', 'r') as f:
    prog = [i.replace('\n','') for i in f.readlines()]
    prog = prog + ["00000000" for i in range(256-len(prog))]

def bitoi(bits:list):
    cs = 0
    for i in range(len(bits)):
        if bits[i]:
            cs+=2**i
    
    return cs

marktemp = 0
def mark():
    global marktemp
    c = time.time()-marktemp
    marktemp = time.time()
    try:
        return 1/c
    except:
        return 999
marks=[]


tools = 0

size = 5
pressedo = [0,0,0]
keys = pygame.key.get_pressed()

aver=0
globalTime = 21

smap.getB(39,59).press([1,0,0])
smap.getB(39,57).press([1,0,0])

startime=time.time()
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            smap.save("save.json")
            sys.exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                smap.tick()
            if i.button == 4:
                size+=1
            elif i.button == 5:
                size-=1
    keyso = keys
    keys = pygame.key.get_pressed()
    cx,cy=pygame.mouse.get_pos()
    cgx,cgy = [round(((cx-x)-size/2)/size),round(((cy-y)-size/2)/size)]
    pressed=pygame.mouse.get_pressed()
    
    pressup = [pressedo[i] and not pressed[i] for i in range(3)]
    pressdw = [not pressedo[i] and pressed[i] for i in range(3)]

    if keys[pygame.K_UP]:
        y+=1
    elif keys[pygame.K_DOWN]:
        y-=1
    if keys[pygame.K_LEFT]:
        x+=1
    elif keys[pygame.K_RIGHT]:
        x-=1
        
    if keys[pygame.K_1]:
        tools=0
    elif keys[pygame.K_2]:
        tools=1
    elif keys[pygame.K_3]:
        tools=2
        
    if tools == 0:
        try:
            tosee[world[cgx][cgy]].press(pressup)
        except:
            pass
        if pressup[0]:
            if keys[pygame.K_a]:
                index = world[cgx][cgy]
                print(tosee[index].imMisstake)
                world[cgx][cgy] = -1

                for i in tosee[index].out:
                    i.lin-=1
                for i in tosee:
                    try:
                        i.out.remove(tosee[index])
                    except:
                        pass
                #tosee.pop(index)
                tosee[index]=block(imMisstake = True)
                print(tosee[index].imMisstake)
            else:
                blocku = 0
                for key in list(keyloc.keys()):
                    if keys[key]:
                        addL(cx, cy, keyloc[key])
                if keys[pygame.K_q]:
                    blocku = logic("and")
                if keys[pygame.K_w]:
                    blocku = button("Bt")
                elif keys[pygame.K_e]:
                    blocku = clapa("cA")
                elif keys[pygame.K_r]:
                    blocku = clapb("cB")
                elif keys[pygame.K_t]:
                    blocku = stepper("st")
                elif keys[pygame.K_y]:
                    blocku = clock("cl")
                addL()
                if blocku:

                    index=len(tosee)
                    blocku.pos = [cgx,cgy]
                    blocku.index = index
                    tosee.append(deepcopy(blocku))
                    if tot.count(blocku.rul)!=0:
                        totick.append(tosee[index])
                    world[cgx][cgy]=index

    elif tools == 1:
        if pressup[2]:
            ado = [cgx,cgy]
        if pressup[0]:
            a,b = (tosee[world[ado[0]][ado[1]]],tosee[world[cgx][cgy]])
            if not ((cgx==ado[0] and cgy==ado[1]) or (a.imMisstake or b.imMisstake)):
                try:
                    a.out.remove(b)
                    b.lin-=1
                    print("del " + str(a.index) + "->" + str(b.index))
                except:
                    a.out.append(b)
                    b.lin+=1
                    print("add " + str(a.index) + "->" + str(b.index))
        if pressup[1]:
            a,b = (tosee[world[ado[0]][ado[1]]],tosee[world[cgx][cgy]])
            if not ((cgx==ado[0] and cgy==ado[1]) or (a.imMisstake or b.imMisstake)):
                try:
                    b.out.remove(a)
                    a.lin-=1
                    print("del " + str(a.index) + "<-" + str(b.index))
                except:
                    b.out.append(a)
                    a.lin+=1
                    print("add " + str(a.index) + "<-"+ str(b.index))
        
    elif tools == 2:
        if pressup[2]:
            adf = [cgx,cgy]
        if pressup[0]:
            tosee.append([cgx,cgy])
            tosee.remove(adf)
            world[cgx][cgy] = deepcopy(world[adf[0]][adf[1]])
            world[adf[0]][adf[1]] = block(imMisstake = True)
            
            for i in tosee:
                af = world[i[0]][i[1]]
                try:
                    af.out.remove(adf)
                    af.out.append([cgx,cgy])
                except:
                    pass
            adf=[cgx,cgy]
                
    pressedo = pressed
        
    
    mark()
    for i in range(50):
        cs = bitoi(smap.rBits(43, 99))

        smap.wBits(33, 99, prog[cs])
                
        if smap.getB(41,99).al:
            prog[cs] = ''
            for i in smap.rBits(33, 97):
                prog[cs] += str(int(i))

        if smap.getB(64,99).al:
            cs = bitoi(smap.rBits(56, 99))
            print(chr(cs),end='')
            
        smap.tick()
    smap.draw(sc, x, y, size, dx, dy, cx, cy)
    
    if globalTime%200==0:
        aver = round(sum(marks)/len(marks))
        marks=[]
        smap.save("save.json")
    else:
        marks.append(mark())
        
    sc.blit(font_l.render(str(aver), 1, [0,0,255]), [0,60*2])
    sc.blit(font_l.render(str([cgx,cgy]), 1, [0,0,255]), [0,60])
    sc.blit(font_l.render(str(tools), 1, [0,0,255]), [0,0])
    
    
    #startime=time.time()

    pygame.display.update()
    sc.fill((0,0,0))
    clockg.tick(100)
    globalTime+=1
