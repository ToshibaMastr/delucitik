import sys
import time
import json
from copy import deepcopy


class block:
    idm=0
    
    lin = 0
    al = 0
    def __init__(self, rul:str="unn", out:list=[], pos:list = [0,0], index:int = 0, imMisstake:bool = False):
        self.imMisstake = imMisstake
        self.inbs = 0
        self.rul = rul
        self.out = deepcopy(out)
        self.pos = pos
        self.index=index
        
    def ttl(self):
        for i in range(len(self.out)):
            self.out[i] = tosee[self.out[i]]
            self.out[i].lin+=1
            try:
                self.out[i] = tosee[self.out[i]]
                self.out[i].lin+=1
            except:
                print(self.out[i])
                
    def press(self, pressed):
        pass
    def tick(self):
        pass
    def update(self, bit):
        pass
            
class logic(block):
    idm=1
    cc = {"and": lambda a,b: a and b, "or": lambda a,b: a or b,
          "nand": lambda a,b: a and b, "nor": lambda a,b: a or b}
    vso = {"and":"nand", "nand":"or", "or":"nor", "nor":"and"}
    
    def press(self, pressed):
        if pressed[0]:
            self.rul = vso[self.rul]
    
    def update(self, bit):
        self.al = self.cc[self.rul](self.al,bit) if self.inbs else bit
        self.inbs += 1
        if self.inbs == self.lin:
            if self.rul[0]=='n':
                self.al=not self.al
            for i in self.out:
                i.update(self.al)
            self.inbs=0
             
class button(block):
    idm=2
    def press(self, pressed):
        if pressed[0]:
            self.al = not self.al
    def tick(self):
        for i in self.out:
            i.update(self.al)

class clapa(block):
    idm=3
    def update(self, bit):
        if bit==1:
            for i in self.out:
                i.lock()
            #for i in self.out:
            #    world[i[0]][i[1]].lock()

class clapb(block):
    idm=4
    lck=0
    alk=0
    def lock(self):
        self.lck=1
        self.al=self.alk
    def tick(self):
        for i in self.out:
            i.update(self.al)
        self.lck=0
    def update(self, bit):
        self.alk=bit
        if self.lck==1:
            self.al=bit

class stepper(block):
    idm=5
    indexa=0
    active=True
    
    def press(self, pressed):
        if pressed[0]:
            if self.active:
                self.active=False
            else:
                self.active=True
        if pressed[2]:
            self.indexa=(self.indexa+1)%len(self.out)
            
    def update(self, bit):
        return
        if bit==0:
            if self.active:
                self.indexa=(self.indexa+1)%len(self.out)
                self.active=False
        else:
            self.active=True
    def tick(self):
        for il in range(len(self.out)):
            i=self.out[il]
            i.update(il==self.indexa)
        if self.active:
            self.indexa=(self.indexa+1)%len(self.out)
           
class clock(block):
    idm=6
    active=False
    def press(self, pressed):
        if pressed[0]:
            self.active = not self.active
        if pressed[2]:
            self.al = not self.al
    def tick(self):
        for i in self.out:
            i.update(self.al)
        if self.active:
            self.al = not self.al


#keyloc = {pygame.K_q:"and",pygame.K_w:"Bt",pygame.K_e:"cA",pygame.K_r:"cB",pygame.K_t:"st",pygame.K_y:"cl"}
blocksListRul = ["and", "Bt", "cA", "cB", "st", "cl"]
blocksList = [logic, button, clapa, clapb, stepper, clock]
tot = ["cB","Bt","cl","st"]
