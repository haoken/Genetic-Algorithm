import random
import math
#杂交染色体

def hybrid(breedPool,probability):
    """
    繁殖池杂交
    :param breedPool: 需要杂交的个体
    :param probability: 杂交概率
    :return: 杂交后产生的新个体集合
    """
    #根据杂交概率选出需要杂交的个体
    hybridPool = []
    for i in range(len(breedPool)):
        p = random.random()
        if p<=probability:  #例如75%   0~0.75之间的可以进行杂交
            hybridPool.append(breedPool[i])

    #按顺序杂交 0&1  2&3 4&5 .......  得到新个体
    chromLen = len(breedPool[0]) #染色体长度
    newPool = []
    i = 0
    while(i<len(hybridPool) and i+1<len(hybridPool)):
        unit1 = hybridPool[i]
        unit2 = hybridPool[i+1]
        #单点杂交  有chromLen个点可供选择
        position = math.floor(random.uniform(1,chromLen)-0.0000000001)
        #交换
        new1 = []
        new2 = []
        for j in range(position):
            new1.append(unit1[j])
            new2.append(unit2[j])
        for j in range(position,chromLen):
            new1.append(unit2[j])
            new2.append(unit1[j])
        newPool.append(new1)
        newPool.append(new2)
        i = i+2

    return newPool

if __name__ == '__main__':
    breedPool = [[0.9876234902016693, 4.49218950979833, 1.448236775626226, 3.1005082243737743], [0.4724596807825379, 0.45958331921746204, 1.867829197058241, 0.25471580294175905], [0.23580358878269642, 0.8887484112173035, 3.2568669663443743, 0.6305360336556257], [1.5697191832521378, 2.475627816747862, 0.2991479476481794, 0.08609705235182061], [3.571358005654843, 0.9768229943451568, 0.23845098462513759, 0.9898970153748624], [0.2704587950124394, 0.28604820498756056, 4.75464733485781, 0.6078206651421894], [2.5030336410503664, 1.1152423589496336, 0.7387650419739393, 1.9448129580260605], [0.15156056425428732, 0.4069404357457127, 0.6927837713065912, 0.07119522869340882], [0.1911154758278359, 1.1227005241721641, 2.7590925897897467, 0.8236194102102533], [0.30827246929243046, 0.29868653070756956, 2.6746639941153423, 0.9368370058846576]]
    newPool = hybrid(breedPool,0.8)
    i = 0
    print("\n\n================breed pool====================")
    for breed in breedPool :
        print(i, end=" ")
        print(breed)
        i = i + 1
    i = 0
    print("\n\n================new pool====================")
    for newUnit in newPool:
        print(i,end=" ")
        print(newUnit)
        i = i+1