# -*- coding: utf-8 -*-
"""
@author: sosene
"""
#Przepisac na wersje kolumnowo-macierzowa...
import random
import numpy as np
import seaborn as sb
import pandas as pd
#from sklearn import datasets
import matplotlib.pyplot as plt

random.seed(7)
entityNumber = 100
worldSize = {'x': 100, 'z': 100}
numKinds = 3

class Entity:
    # current state
    kind = 0.
    intensity = 0.25
    px = 0.
    pz = 0.
    v = 0.
    alpha = 0.
    
    # parameters
    aMax = 2.
    rotMax = 45.
    viewRange = 100.
    rangeSegments = 5
    rotSegments = 11 # better to have odd number probably
    halfBeta = 30
    
    # init function
    def __init__(self,rx,rz,alpha,kind):
        #print('Hej')
        self.px = rx
        self.pz = rz
        self.alpha = alpha
        self.kind = kind
        
    def move(self, dt):
        self.px = (self.px + self.v * np.cos(self.alpha * 2*np.pi/360) * dt) % worldSize['x']
        self.pz = (self.pz + self.v * np.sin(self.alpha * 2*np.pi/360) * dt) % worldSize['z']
    
    def accelerate(self, aFrac):
        self.v = self.v + aFrac*self.aMax
        
    def rotate(self, rotFrac):
        self.alpha = (self.alpha + rotFrac * self.rotMax/(1+self.v)) % 360
    
entityList = []

# generate entities
for i in range(entityNumber):
    rx = random.random()*worldSize['x']
    rz = random.random()*worldSize['z']
    alpha = random.random()*360
    kind = int(random.random()*3)
    entityList.append(Entity(rx,rz,alpha,kind))
    
# accelerate entities
for i in range(len(entityList)):
    entityList[i].accelerate(random.random())   
   

for j in range(1):
    # move entities
    for i in range(len(entityList)):
        entityList[i].move(1)
        
    # rotate entities
    for i in range(len(entityList)):
        entityList[i].rotate(random.random()*2-1)


    pxList = []
    pzList = []
    vList = []
    for i in range(len(entityList)):
        pxList.append(entityList[i].px)
        pzList.append(entityList[i].pz)
        vList.append(entityList[i].v)
    
    df = pd.DataFrame(
        {
            'px': pxList,
            'pz': pzList,
            'v': vList
        })


    sb.set(font_scale=1.2, style="ticks") #set styling preferences


    sb.plt.xlim(0,100)
    sb.plt.ylim(0,100)

    points = plt.scatter(df["px"], df["pz"],
                         c=df["v"], s=20, cmap="Spectral") #set style options
    points.figure.set_size_inches(10, 10)           
    points.figure.savefig("oaa_1_"+str(j)+".png")
    plt.clf()
    
t=0
tE = entityList[0]
print("tE position ",tE.px, " ", tE.pz)
print("tE angle ",tE.alpha)
perception = np.zeros((numKinds, tE.rangeSegments, tE.rotSegments))
rangeSegmentsList = [tE.viewRange*(2**n-1)/(2**tE.rangeSegments-1) for n in range(tE.rangeSegments+1)]
rotSegmentsList = [180-tE.halfBeta-angle*(360.-2*tE.halfBeta)/tE.rotSegments for angle in range(tE.rotSegments+1)]

for i in range(len(entityList)):
    if (i != t):
        tF = entityList[i]
        dist = np.sqrt((tE.px-tF.px)**2+(tE.pz-tF.pz)**2)
        print('Distance: ', dist)
        if(dist < tE.viewRange):
            if(tE.pz < tF.pz):
                relativeAngle = ((90 - tE.alpha+np.arcsin((tE.px-tF.px)/dist)*360/(2*np.pi))%360)-180
            else:
                relativeAngle = ((90 - tE.alpha+180-np.arcsin((tE.px-tF.px)/dist)*360/(2*np.pi))%360)-180
            print('Angle: ', relativeAngle)
            rangeSegment = tE.rangeSegments
            for seg in reversed(range(tE.rangeSegments)):
                if (dist>= rangeSegmentsList[seg]):
                    rangeSegment = seg
                    break
            print('Segment: ', rangeSegment)
            if(np.abs(relativeAngle) < (180- tE.halfBeta)):
                for angSeg in range(1,len(rotSegmentsList)):
                    if(relativeAngle > rotSegmentsList[angSeg]):
                        rotSegment = angSeg-1
                        print('rotSegment: ', angSeg)
                        perception[tF.kind,rangeSegment,rotSegment] += tF.intensity
                        break


#    viewRange = 10.
#    rangeSegments = 5
#    rotSegments = 5
#    halfBeta = 30

print(perception[0])
print(perception[1])
print(perception[2])
