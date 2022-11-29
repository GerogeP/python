# CalBMI.py
h, w = eval(input())
bmi = w / pow(h, 2)
who, nat = '', ''
if bmi < 18.5:
    who, nat = '偏瘦', '偏瘦'
elif bmi < 24:
    who, nat = '正常', '正常'
elif bmi < 25:
    who, nat = '正常', '偏胖'
elif bmi < 28:
    who, nat = '偏胖', '偏胖'
elif bmi < 30:
    who, nat = '偏胖', '肥胖'
else:
    who, nat = '肥胖', '肥胖'
print("BMI数值为:{:.2f}".format(bmi))
print("BMI指标为:国际'{}',国内'{}'".format(who, nat))
