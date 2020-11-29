import random

# 确认编码方式
# 范围：[0,6]  精度：0.000001
# 若分成6/0.0000001=6,000,000 份（600万） 600万*600万 = 360000亿个候选解。不可行
# 采用浮点数编码方式,每个染色体[x1,x2]
# 问题：太短了，交换来交换区都是那几个，没啥意思。
# 解决：能否将x1、x2随机分成两份。染色体编程[x11,x12,x21,x22].  试一下

def encode(scope,accuracy,population):
    """
    编码方式
    :param scope: 自变量范围
    :param accuracy: 目标精度
    :param population : 种群数量
    :return: 每个候选解的编码list
    """
    # 随机初始化population个个体。
    group = []
    for i in range(population):
        x1 = random.uniform(scope[0],scope[1])
        x2 = random.uniform(scope[0],scope[1])
        split1 = random.random()
        split2 = random.random()
        x11 = round(x1*split1,accuracy)
        x12 = round(x1*(1-split1),accuracy)
        x21 = round(x2*split2,accuracy)
        x22 = round(x2*(1-split2),accuracy)
        unit = [x11,x12,x21,x22]
        group.append(unit)
    return group

if __name__ == '__main__' :
    scope = [0,6] #自变量范围
    accuracy = 6  #小数点后6位
    population = 20 #种群数量20
    popu = encode(scope,accuracy,population)
    for p in popu:
        print(p)