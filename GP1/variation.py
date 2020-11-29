import random
import math

#变异
def variate(solutions,posibility,scope,accuracy):
    """
    每个个体都有posibility进行变异
    :param solutions: 个体集
    :param posibility: 变异可能性
    :param scope: 变异范围 [0,3]
    :param accuracy:精度
    :return: 变异后的个体集
    """
    chromLen = len(solutions[0])
    for i in range(len(solutions)):
        x = random.random()
        if x<posibility:
            pos = random.uniform(0,chromLen-0.00000001) #变异位置
            pos = math.floor(pos)
            solutions[i][pos] = round(random.uniform(scope[0],scope[1]),accuracy)
    return solutions
