from GP1.variation import variate
from GP1.GenieEncode import encode
from GP1.roulette import rouletteChoice
from GP1.hybridization import hybrid
from GP1.GenieDecode import *


# 使用遗传算法完成函数优化问题。

def targetFunc(j, x1, x2):
    """
    目标函数 f(x1,x2)=3-sin^2(j*x1)-sin^2(j*x2)
    适应值函数 g(x1,x2)=1.0/f(x1,x2)
    :param j: 参数
    :param x1: 自变量1
    :param x2: 自变量2
    :return:
    """
    if x1 > 6: x1 = 6
    if x2 > 6: x2 = 6

    m = math.sin(j * x1) * math.sin(j * x1)
    n = math.sin(j * x2) * math.sin(j * x2)
    res = 1.0/(3-m-n)
    return res


# x1,x2 ∈ [0,6]    j=2
# 要求：求 j=2时 函数取最小值时  x1x2的值 精确到小数点后6位
# 提示：函数j=2时最小值有16个、

def printFitness(solutions, fitness):
    for i in range(len(solutions)):
        res = [solutions[i][0]+solutions[i][1],solutions[i][2]+solutions[i][3]]
        print(i, res, end="\t")
        print("fitness:", fitness[i])


def sortSolutions(solutions, fitness):
    """
    根据对应的fitness对solution进行排序
    :param solutions:
    :param fitness:
    :return: 排序好的solution,fitness
    """
    population = len(solutions)
    for i in range(population):
        for j in range(i + 1, population):
            if fitness[i] < fitness[j]:
                tmp = fitness[i]
                fitness[i] = fitness[j]
                fitness[j] = tmp
                tmp1 = solutions[i]
                solutions[i] = solutions[j]
                solutions[j] = tmp1
    return solutions, fitness


def epoch(solutions, j, varProbability, hybridProbability, scope,breedPoolNum,accuracy):
    """
    一次迭代
    :param solutions:
    :param j: 目标函数参数j
    :param varProbability: 变异概率
    :param hybridProbability: 繁殖概率
    :param scope 定义域
    :param breedPoolNum 繁殖池数量
    :param accuracy 精度
    :returns:
        solutions:一次迭代之后的个体集
        fitness  :改革体制对应的适应值
    """

    # 变异
    variate(solutions, varProbability, scope,accuracy)

    # 计算适应值
    fitness = []  # 适应值列表,与solutions一一对应
    for solution in solutions:
        fit = targetFunc(j, solution[0] + solution[1], solution[2] + solution[3])
        fitness.append(fit)

    # 根据适应值排序
    solutions, fitness = sortSolutions(solutions, fitness)

    # 选择策略：轮盘赌选择算法,从种群中选出繁殖池
    breedPool, breedIndex, breedFitness = rouletteChoice(solutions, fitness, breedPoolNum)

    # 杂交得到新个体集
    newPool = hybrid(breedPool, hybridProbability)

    # 计算新个体适应值
    newFitness = []  # 与newPool意义对应
    for newUnit in newPool:
        newfit = targetFunc(j, newUnit[0] + newUnit[1], newUnit[2] + newUnit[3])
        newFitness.append(newfit)

    # 对新个体集根据适应值进行排序
    newPool, newFitness = sortSolutions(newPool, newFitness)

    # 将新个体插入到
    index = 0  # newPool下标
    i = 0  # solutions下标
    while i < len(fitness):
        while index < len(newFitness) and newFitness[index] >= fitness[i]:
            if solutions.count(newPool[index]) == 0:  # 个体不一样才可以插入。
                solutions.insert(i, newPool[index])
                fitness.insert(i, newFitness[index])
                i = i + 1
            index = index + 1
        if index == len(newFitness):  # 个体插入完成，退出循环
            break;
        i = i + 1
        # 边界值：当新个体中的适应值小于老个体最小值时，该个体不会插入到solution中。

    # 截取前population个
    solutions = solutions[0:population]
    fitness = fitness[0:population]

    return solutions, fitness


if __name__ == '__main__':
    scope = [0, 6]  # x1、x2范围
    accuracy = 6  # 小数点后6位
    population = 200 # 个体集数量32
    breedPoolNum = 100  # 繁殖池大小
    hybridProbability = 0.80  # 繁殖概率
    variationProbability = 0.01  # 变异概率
    epochs = 50  # 迭代次数
    j_para = 2  # 参数j
    n = 32 #取前个体中前n个个体

    #编码
    solutions = encode(scope, accuracy, population)

    fitSum = []  # 总体适应值
    fitMax = []  # 最大适应值
    fitness = []  # 适应值列表
    #开始迭代
    for i in range(epochs):
        solutions, fitness = epoch(solutions, j_para, variationProbability, hybridProbability, scope,breedPoolNum,accuracy)
        fitMax.append(fitness[0])
        sum = 0.0
        for k in range(n):
            sum = sum + fitness[k]
        fitSum.append(sum)

    #前n适应值的迭代变化
    plt.xlabel('epochs')
    plt.ylabel('fitSum')
    plt.plot(fitSum)
    plt.show()

    # 散点图
    show_scatter(solutions,n)


    printFitness(solutions, fitness)




