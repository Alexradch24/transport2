from pulp import *
import time
def input_x(noif1, noif2, x_i, uravn, rez, rez_max):
    file1 = open(noif1, 'r')
    file2 = open(noif2, 'r')
    print(file1.readline().strip())
    print(file2.readline().strip())
    text = file1.readline().strip()
    i = 0
    while len(text) != 0:
        text= text.replace('"','').replace(';','').replace('=','').replace(',','')
        mass = list(map(int, text.split()))
        rez.append(mass[0])
        rez_max.append(mass[1])
        uravn.append(mass[2:])
        text = file1.readline().strip()
        i += 1
    text = file2.readline().strip()
    i = 0
    while len(text) != 0:
        text= text.replace('"','').replace('=','').replace(',','')
        mass = list(map(float, text.split(';')))
        test = int(mass[0])
        if len(x_i) == test - 1: x_i.append([mass[1], 0])
        elif len(x_i) > test - 1: x_i[test - 1][0] = mass[1]
        elif len(x_i) < test - 1:
            raz = int(mass[0]) - len(x_i) - 1
            for j in range(raz):
                x_i.append([0, 0])
            x_i.append([mass[1], 0])
        text = file2.readline().strip()
        i += 1    
    file1.close()
    file2.close()
    return x_i, uravn, rez, rez_max
name_of_input_file1 = input()
name_of_input_file2 = input()
start = time.time()
x_i = [] # [koef, max, min]
uravn = []
rez = []
rez_max = []
x_i, uravn, rez, rez_max = input_x(name_of_input_file1, name_of_input_file2, x_i, uravn, rez, rez_max)
m = len(uravn)
rez_per = [0] * m
n = len(x_i)
prob = pulp.LpProblem("myProblem", LpMaximize)
for i in range(n):
    x_i[i][1] = pulp.LpVariable('x;' + str(i + 1), lowBound = 0)
for i in range(m):
    rez_per[i] = pulp.LpVariable('m;' + str(i + 1), lowBound = 0)
prob += sum((1000 * (rez_per[i])) for i in range(m)) - sum((x_i[i][0] * x_i[i][1]) for i in range(n)) # Öåëü
for i in range(m):
    prob += sum(x_i[j - 1][1] for j in uravn[i])  == rez_per[i]
    prob += rez_per[i] <= rez[i]
prob.solve()
file = open("answer_test", "w")
file.write(str(abs(value(prob.objective))) + '\n')
for i in prob.variables():
    file.write(str(i.name) + ';' + str(i.varValue) + '\n')
file.close()
stop = time.time()
print((stop - start) // 3600, ':', (stop - start) % 3600 // 60, ':', (stop - start) % 60)