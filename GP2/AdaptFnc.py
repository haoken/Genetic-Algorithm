import math
# Shubert函数 在 x∈[-10,10]  n=2时的 最优解
# 精确到小数点后6位。


def Shubert(x):
    """
    Shubert函数
    :param x: 自变量  x=[x1,x2,x3,...,xn]
    :return: 函数值
    """
    result = 1.0
    n = len(x)
    for i in range(1,n+1):
        addend = 0
        for j in range(1,6):
            addend = addend + j*math.cos((j+1)*x[i-1]+j)
        result = result * addend
    return result


def AdaptFnc(x):
    """
    适应值函数
    :param x: 自变量  x=[x1,x2,x3,...,xn]
    :return:
    """
    res = Shubert(x)
    return -res

if __name__ == '__main__':
    x = [-10,10]
    z = Shubert(x)
    y = AdaptFnc(x)
    print("Shubert（x）=",z)
    print("fitFne（x）=",y)