#coding=utf-8
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#打开交互模式，好让我画动态图
plt.ion()
plt.figure()
vector = range(1,3601) #1-3600
#原地搅乱序列vector
random.shuffle(vector)
white = vector[0:1400]
black = vector[1400:2800]
temp = vector[2800:3600]
#创建一个三维数组，以0填充，第一维62，第二维62，第三维3
tmap = np.zeros((62,62,3))
# init
for i in range(1,3601):
    if i in white:
    	#红色（1，0，0）
        tmap[(i - 1) / 60 + 1][(i - 1) % 60 + 1] = [1, 0, 0]
    elif i in black:
    	#蓝色（0，0，1）
        tmap[(i - 1) / 60 + 1][(i - 1) % 60 + 1] = [0, 0, 1]
    else:
    	#绿色（0，1，0）
        tmap[(i - 1) / 60 + 1][(i - 1) % 60 + 1] = [0, 1, 0]
#邻居节点，按照行来表示（neiborhood,by row）
row = [-1,-1,-1, 0, 0, 1, 1, 1] #neiborhood
col = [-1, 0, 1,-1, 1,-1, 0, 1]
simv = []
for m in range(7):
	#阈值
    thd = 0.3+m*0.1
    print 'Threshold:'+str(thd)
    #同质性
    sim = 0.0 #similarity
    nosat = 1
    times = 0
    #如果有节点不满意，那么就搬家，同时总循环次数小于100次
    while nosat and times<100:
        times=times+1
        sim = 0.0
        #蓝色未定居
        bnosat = 0
        #红色未定居
        rnosat = 0
        #未定居节点位置
        nosatv=[]
        for i in range(1,61):
            for j in range(1,61):
            	#不是空，既不是绿色节点
                if(tmap[i][j][1] != 1):
                    ns=0.0
                    #居住个数
                    n=0.0
                    for k in range(8):
                    	#判断邻居节点是不是红色或者蓝色
                        if tmap[i+row[k]][j+col[k]][0]==1 or tmap[i+row[k]][j+col[k]][2]==1:
                            n=n+1.0
                            #判断邻居节点是不是和当前节点相同
                            if tmap[i+row[k]][j+col[k]][0] == tmap[i][j][0]:
                                ns=ns+1.0
                    if n!=0:
                    	#同质性=性质相同节点数/当前范围总节点数
                        sim = sim + ns/n #similarity plus
                        #如果同质性小于阈值
                        if(ns/n < thd):
                        	#那么红色色未定居的人数加一
                            if(tmap[i][j][0]==1):
                                rnosat = rnosat+1
                            #或者蓝色未定居的人加一
                            else:
                                bnosat = bnosat+1
                            #记录下当前未定居的节点位置
                            nosatv.append([i, j])
                else:
                	#记录空节点
                    nosatv.append([i, j])
        nosat = rnosat + bnosat
        #不满意率
        print 'Unsatisfied:' + str(nosat / 2800.0*100)+'%'
        #搬家开始
        #-----------------
        #原地搅乱顺序,随机搬家
        random.shuffle(nosatv)
        rnosatv=nosatv[0:rnosat]
        bnosatv=nosatv[rnosat:rnosat+bnosat]
        tempv = nosatv[rnosat+bnosat:]
        #从所有的未定居的节点（包括空节点）中随机的选出之前红色不满意的人数 因为搬家总是再这些人之间，其他人不变。这样，即使之前的蓝色变成红色也无所谓。
        #所以我们在这些节点中随机挑出一定数量的节点，使他们变成红色，那么就代表了之前红色节点搬家了
        for i in range(rnosat):
            tmap[rnosatv[i][0]][rnosatv[i][1]]=[1,0,0]
        plt.cla()
        plt.axis("off")
        plt.imshow(tmap,interpolation="nearest")
        plt.title('Threshold = '+str(thd)+'    Homoplily:'+ str(sim/2800*100)+'%')
        plt.pause(0.03)
        for i in range(bnosat):
            tmap[bnosatv[i][0]][bnosatv[i][1]]=[0,0,1]
        plt.cla()
        plt.axis("off")
        plt.imshow(tmap,interpolation="nearest")
        plt.title('Threshold = '+str(thd)+'    Homoplily:'+ str(sim/2800*100)+'%')
        plt.pause(0.03)
        for i in range(tempv.__len__()):
            tmap[tempv[i][0]][tempv[i][1]] = [0, 1, 0]
        plt.cla()
        plt.axis("off")
        plt.imshow(tmap,interpolation="nearest")
        plt.title('Threshold = '+str(thd)+'    Homoplily:'+ str(sim/2800*100)+'%')
        plt.pause(0.03)
    plt.ioff()
    plt.show()
    plt.ion()
    sim = sim/2800.0
    simv.append(sim)
    print 'Homoplily:' + str(sim*100)+'%'
plt.ioff()
plt.show()
plt.figure()
plt.plot([0.3+m*0.1 for m in range(7)],simv,'-')
plt.title('Homoplily of different threshold')
plt.xlabel('threshold')# make axis labels
plt.ylabel('Homoplily')
plt.xlim(0.2, 1.0)
plt.xlim(0.2, 1.0)
plt.show()
