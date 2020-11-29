import math
# Shubert函数 在 x∈[-10,10]  n=2时的 最优解
# 精确到小数点后6位。

# Shubert函数
def Shubert(x):
    """
    Shubert函数
    :param x: 自变量  x=[x1,x2,x3,...,xn]
    :return: 函数值
    """
    result = 1.0
    n = len(x)
    for i in range(n):
        for j in range(5):
            addend = j*math.cos((j+1)*x[i]+j)
        result = result * addend
    return result

# 适应值函数
def fitFnc(x):
    """
    适应值函数
    :param x: 自变量  x=[x1,x2,x3,...,xn]
    :return:
    """
    res = math.exp(-1*Shubert(x)) # Shubert最小值为负数，所以要加个符号，负得越小fitFnc 就越大。
    return res

if __name__ == '__main__':
    x = [-10,10,-10,10,-10,5,6]
    z = Shubert(x)
    y = fitFnc(x)
    print("Shubert（x）=",z)
    print("fitFne（x）=",y)