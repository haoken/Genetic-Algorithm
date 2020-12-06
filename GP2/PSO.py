# PSO算法实现
# Shubert n==2 时 的最小值
# 精确到小数点后6位。  x1,x2 ∈[-10,10]
# 一个可能的最小值 ： 186.730909

import matplotlib.pyplot as plt
import numpy as np
import random

from GP2.Partical import Partical


def PSO(n=2, score=[-10, 10], accuracy=6):
    """
    使用PSO算法寻找Shubert的解
    :param n:
    :param score:
    :param accuracy:
    :return:
    """
    ParticalNumber = 1000  # 粒子群大小
    ParticalSwarm = []  # 粒子群
    epochs = 50  # 迭代次数

    # 初始化粒子群
    for i in range(ParticalNumber):
        x = []
        for j in range(n):
            x1 = random.uniform(score[0], score[1])  # 在解空间中取ParticalNumber个解
            x.append(x1)
        partical = Partical(x)  # 创建一个粒子对象
        ParticalSwarm.append(partical)  # 加入到粒子群中

    for epoch in range (epochs):#每次迭代 是每个粒子更新一次位置
        for partical in ParticalSwarm:
            partical.updateSolution()
        # print(Partical.globalBest,"  adapt:",Partical.gloAdapt,"  value:",Partical._value(Partical.globalBest))

        #显示所有点
        x = [partical.solution[0] for partical in ParticalSwarm]
        y = [partical.solution[1] for partical in ParticalSwarm]
        x = np.array(x)
        y = np.array(y)
        plt.xlim(-10,10)
        plt.ylim(-10,10)
        plt.plot(x,y,'ro')
        x_bestN = np.array([best[0][0] for best in Partical.bestN])
        y_bestN = np.array([best[0][1] for best in Partical.bestN])
        plt.plot(x_bestN,y_bestN,"go")
        plt.plot(Partical.globalBest[0],Partical.globalBest[1],"bo")
        plt.show()

    for best in Partical.bestN:
        print(best[0],"  adapt:",best[1])




if __name__ == '__main__':
    PSO()




