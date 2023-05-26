import sys
import time
import json
from copy import deepcopy
from modules import logics
import pygame

def _tepos(x:float, y:float, zoom:float, dx:int, dy:int):
    return [[x*zoom + dx, y*zoom + dy], [zoom, zoom]]

def _etpos(x:float, y:float, zoom:float, dx:int, dy:int, cx:int, cy:int):
    return [round((cx-dx)/zoom-0.5-x),round((cy-dy)/zoom-0.5-y)]

class Map:
    def __init__(self, mpx: int, mpy: int):
        self.mpx, self.mpy = mpx, mpy
        self.world = [[ -1  for j in range(mpx)] for i in range(mpy)]
        self.tosee=[]
        self.totick=[]
        
    def open(self, file: str):
        with open(file, 'rb') as f:
            sBlocks = json.load(f)
            
        for i in range(len(sBlocks)):
            cBlock = sBlocks[i]
            
            blockClass = logics.blocksList[cBlock[2]-1]

            self.world[cBlock[0]][cBlock[1]]=i
            
            self.tosee.append(blockClass(cBlock[5], cBlock[4], pos=[cBlock[0],cBlock[1]], index=i))

            if logics.tot.count(self.tosee[i].rul)!=0:
                self.totick.append(self.tosee[i])
        #tosee.append(block(imMisstake = True))
        for cBlock in self.tosee:
            for i in range(len(cBlock.out)):
                cBlock.out[i] = self.tosee[cBlock.out[i]]
                cBlock.out[i].lin+=1
            
    def save(self, file: str):
        with open(file, "w") as f:
            json.dump([[i.pos[0],i.pos[1],i.idm,i.lin,[ia.index for ia in i.out],i.rul] for i in self.tosee], f)

    def delL(self, x:int, y:int):
        index = self.world[x][y]
        self.world[x][y] = -1

        for i in self.tosee[index].out:
            i.lin-=1
        for i in self.tosee:
            try:
                i.out.remove(self.tosee[index])
            except:
                pass
        self.tosee[index]=logics.block(imMisstake = True)

    def addL(self, x:int, y:int, name:str):
        rul = logics.blocksListRul.index(name)
        blocku = logics.blocksList[rul](rul)
        if blocku:
            index=len(self.tosee)
            blocku.pos = [x,y]
            blocku.index = index
            self.tosee.append(deepcopy(blocku))
            if logics.tot.count(blocku.rul)!=0:
                logics.totick.append(self.tosee[index])
            self.world[x][y]=index

    def getB(self, x:int, y:int):
        return self.tosee[self.world[x][y]]

    def tick(self):
        for cBlock in self.totick:
            cBlock.tick()

    def draw(self, sc, x:int, y:int, zoom:float, dx:int, dy:int, cx:int, cy:int):
        font = pygame.font.Font(None, round(zoom/2))
        cgx,cgy = _etpos(x, y, zoom, dx, dy, cx, cy)
        pygame.draw.rect(sc, (155,0,0), _tepos(x, y, zoom, dx, dy)[0]+[zoom*self.mpx,zoom*self.mpy],1)

        pygame.draw.rect(sc, (255,0,0), _tepos(x+cgx, y+cgy, zoom, dx, dy),1)
        for i in self.tosee:
            pygame.draw.rect(sc, (220,220,220) if i.al else (22,22,22), _tepos(x+i.pos[0], y+i.pos[1], zoom, dx, dy))
            sc.blit(font.render(i.rul, 1, [0,0,255]), _tepos(x+i.pos[0], y+i.pos[1], zoom, dx, dy)[0])
            
        for i in self.tosee:
            for ia in i.out:
                pygame.draw.line(sc, (250,250,250) if i.al else (100,100,100), _tepos(x+ia.pos[0], y+ia.pos[1], zoom, dx, dy)[0],_tepos(x+i.pos[0], y+i.pos[1], zoom, dx, dy)[0], 1)             

        pygame.draw.circle(sc,(255,255,255),[cx,cy],2)

    def rBits(self, x:int, y:int):
        return [self.getB(x+7-i, y).al for i in range(8)]

    def wBits(self, x:int, y:int, bits:list):
        for i in range(len(bits)):
            self.getB(x+i, y).al = int(bits[i])

        #return [self.getB(x+7-i,y).al for i in range(8)]
        #for i in range(8):
        #    if self.getB(43+7-i,99).al:
        #        cs+=2**i
