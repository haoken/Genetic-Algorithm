# 粒子 ，即个体

from GP2.AdaptFnc import AdaptFnc,Shubert

import random
import sys


class Partical:
    # 以下四个属性所有粒子共享
    globalBest = []  # 全局最佳解
    gloAdapt = -1 * sys.float_info.min  # 全局最佳适应值
    c1 = 2  # 自我认知系数
    c2 = 2  # 全局认知系数
    bestN = [] # 适应值前N的解  [[solution1,adaptValue1],[solution2,adaptValue2],.....]
    N = 50
    similar = 0.1  # bestN中允许相似的程度 （欧式距离）
    scale = [-10,10] # 解的定义域


    def __init__(self, initSolution):
        """
        粒子构造函数，完成初始化操作
        :param initSolution: 初始化位置
        :param globalBest: 全局最优
        """
        self.solution = initSolution[:]  # 初始化位置
        self.adaptValue = self.calAdaptiveValue(self.solution)  # 初始值对应的适应值
        self.updataGlobalBest()  # 更新全局最佳
        self.updateBestN() #更新全局最佳前N
        self.demension = len(initSolution)  # 解的维度
        self.speed = [0] * self.demension  # 初始化速度为0
        self.pastBest = initSolution[:]  # 个人历史最佳初位置
        self.pastAdapt = 0  # 个人历史最佳适应值
        self.R1 = []  # 自我认知随机矩阵，这里压缩为list
        self.R2 = []  # 全局认知随机矩阵，这里压缩为list
        self.inertia = 0.9 # 速度惯性，用来遏制速度爆炸
        self.inertia_sub = 0.05 # 速度惯性 是线性递减的。每次递减inertia_sub
        self.maxSpeed = 1 # 速度的最大值


    def calNewSpeed(self):
        """
        计算新的速度，并更新到对象的speed中。
        :return:
        """
        # 得到随机对角矩阵R1、R2
        self.R1 = self.RandomVector(self.demension)[:]
        self.R2 = self.RandomVector(self.demension)[:]
        # 自我认知部分
        selfPart = [self.c1 * (past - now) * ran for past, now, ran in zip(self.pastBest, self.solution, self.R1)]
        # 全局认知部分
        globalPart = [self.c2 * (glo - now) * ran for glo, now, ran in zip(self.globalBest, self.solution, self.R2)]
        # 新的速度
        self.speed = [self.inertia * oldSpeed + glo + past for oldSpeed, glo, past in zip(self.speed, selfPart, globalPart)]
        for speed_i in self.speed :
            if speed_i>self.maxSpeed:
                speed_i = self.maxSpeed

        # 更新速度惯量，最小值为0.4
        if self.inertia-self.inertia_sub > 0.4 :
            self.inertia = self.inertia-self.inertia_sub
        else :
            self.inertia = 0.4

    def updateSolution(self):
        """
        根据新的速度，更新位置
        :return:
        """
        # 计算新的速度
        self.calNewSpeed()
        # 更新位置
        self.solution = [oldSolution + speed for oldSolution, speed in zip(self.solution, self.speed)]
        # 计算并更新适应值
        self.adaptValue = self.calAdaptiveValue(self.solution)
        # 调整历史最佳
        self.updataPastBest()
        # 调整全局最佳
        self.updataGlobalBest()
        # 调整全局最佳前N
        self.updateBestN()


    def updataPastBest(self):
        """
        根据当前解，调整局部最佳。 注意：只有在定义域中的解才会被放到pastBest中。
        :return:
        """
        if self.adaptValue > self.pastAdapt :
            flag = True
            for i in self.solution:
                if i<Partical.scale[0] or i>Partical.scale[1]:
                    flag = False
            if flag == True:
                self.pastBest = self.solution[:]
                self.pastAdapt = self.adaptValue


    def updataGlobalBest(self):
        """
        根据当前解，调整全局最佳。 注意：只有在定义域中的解才会被放到GlobalBest中。
        :return:
        """
        if self.adaptValue > Partical.gloAdapt:
            flag = True
            for i in self.solution:
                if i < Partical.scale[0] or i > Partical.scale[1]:
                    flag = False
            if flag == True:
                Partical.globalBest = self.solution[:]
                Partical.gloAdapt = self.adaptValue



    def updateBestN(self):
        """
        更新最佳前N解
        :return:
        """
        length = len(Partical.bestN)
        if length == 0 : #空
            Partical.bestN.append([self.solution,self.adaptValue])
        elif length < self.N : #bestN未满
            pos = self.findInsertPos() #插入位置
            if pos==length : #插入最后
                Partical.bestN.append([self.solution,self.adaptValue])
            elif pos < length: #插入到中间
                sim = self.findSimilar(0)  # 查找后面相似的删掉
                if len(sim)>0 and sim[0][1] >= pos :  # pos位置前面没有相似的才插入
                    for elem in sim:
                        Partical.bestN.remove(elem[0])
                    Partical.bestN.insert(pos,[self.solution,self.adaptValue])
        elif self.adaptValue > Partical.bestN[-1][1]: #满了
            pos = self.findInsertPos() #插入位置
            if pos < length: #只能在中间插入
                sim = self.findSimilar(0)#删除后面相同的
                if len(sim)>0 and sim[0][1] >=pos: # pos位置前面没有相似的才插入
                    for elem in sim:
                        Partical.bestN.remove(elem[0])
                    Partical.bestN.insert(pos,[self.solution,self.adaptValue])
                    if len(Partical.bestN) > Partical.N: #如果上面没有删除，这里会多出一个。
                        Partical.bestN.pop()




    def findSimilar(self,pos):
        """
        在Partical.bestN中查找在pos后面相似的元素
        :return: 列表 [[相似元素,下标]]
        """
        res = []
        for i in range(pos,len(Partical.bestN)): # 在本元素插入位置之后相似的元素全部删除。
            sim = self.compareSolution(Partical.bestN[i][0],self.solution)
            if sim < Partical.similar : # 太过相似
                res.append([Partical.bestN[i],i])
        return res


    def findInsertPos(self):
        """
        找到在Partical.bestN里插入的位置
        :return: 位置的下标
        """
        length = len(Partical.bestN)
        for i in range(length - 1, -1, -1):
            if Partical.bestN[-1][1] > self.adaptValue:  # 小于最后一个插入到最后
                return length
            if i - 1 >= 0 and Partical.bestN[i][1] < self.adaptValue and Partical.bestN[i - 1][1] > self.adaptValue:  # 找到插入位置
                return i
            if i == 0:  # 该值是最大的。
                return 0


    def calAdaptiveValue(self,solution):
        """
        计算当前解的适应值
        :param solution: 解
        :return: 适应值
        """
        res = AdaptFnc(solution)
        return res

    def RandomVector(self,demension):
        """
        得到一个demension大小的随机列表（向量）
        :param demension: 维度
        :return:
        """
        res = []
        for i in range(demension):
            res.append(random.random())
        return res

    def compareSolution(self,sol1,sol2):
        """
        比较两个解，计算两个解的欧式距离
        :param sol1: 第一个解
        :param sol2: 第二个解
        :return:
        """
        length = len(sol1)
        if len(sol2) != length : #如果维度不一样无法比较，返回最大浮点值
            return sys.float_info.max
        res = 0.0
        for i in range(length):
            sub = sol1[i]-sol2[i]
            sub = sub*sub
            res = res + sub
        return res

    @staticmethod
    def _value(solution):
        return Shubert(solution)



if __name__ == '__main__':
    # x = [-7.0848,-0.80121]
    # res = Partical._value(x)
    # print(res)
    # bestN = []
    # length = len(bestN)
    # solution = [[1,2,3],[2,3,4],[3,4,5]]
    # adaptValue = [10,20,15]
    N = 2
    # for i in range (3):
    #     beatN = update(bestN,solution[i],adaptValue[i])[:]
    #
    # print(bestN)



