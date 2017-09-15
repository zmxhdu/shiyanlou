import sys
a=sys.argv

global premium,threshold
premium = (8+2+0.5+0+0+6)/100
threshold = 3500
def calculator(salary):
    if (salary-threshold) > 0 :
        ratal=salary-salary*premium-threshold
    else :
        ratal=0

    if ratal <= 1500:
        rate=3/100
        deduction=0
    elif ratal <= 4500:
        rate=10/100
        deduction=105
    elif ratal <= 9000:
        rate=20/100
        deduction=555
    elif ratal <= 35000:
        rate=25/100
        deduction=1005
    elif ratal <= 55000:
        rate=30/100
        deduction=2755
    elif ratal <= 80000:
        rate=35/100
        deduction=5505
    else:
        rate=45/100
        deduction=13505

    real_salary=salary-salary*premium-(ratal*rate-deduction)	
    return real_salary

if __name__ == '__main__':
    for i in  range(1,len(a)):
        b=a[i].split(":",)
        if len(b) !=2:
            print("Parameter Error")
            continue
        try :
            salary=int(b[1])
            int(b[0])
        except ValueError:
            print("Parameter Error")
            continue
        salary=calculator(salary)
        print(int(b[0]),end='')
        print(":",end='')
        print(format(salary,".2f"))