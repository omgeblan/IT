a=[int(x)for x in input("Введите набор чисел: ").split()]
for i in range(1,len(a)):
    for j in range(i+1,len(a)):
        for k in range(j+1, len(a)):
            if a[i]+a[j]>a[k] and a[i]+a[k]>a[j] and a[k]+a[j]>a[i] and a[i]>0 and a[j]>0 and a[k]>0:
                pp=(a[i]+a[j]+a[k])/2
                print("Подходящие числа:",a[i],a[j],a[k])
                print("Площадь треугольника:",((pp*(pp-a[i])*(pp-a[j])*(pp-a[k]))**(1/2)))