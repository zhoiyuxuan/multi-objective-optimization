import time

import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import pandas as pd

class DrSun(Problem):

    def __init__(self,OD,ID,HT,a,b,c,d,e,qa,g,h,j,AL,LE,VE):
        super().__init__(n_var=3,
                         n_obj=1,
                         n_ieq_constr=0,
                         xl=np.array([1.0,10000.0,0.0]),
                         xu=np.array([4.0,200000.0,50.0]))
        self.OD = OD
        self.ID = ID
        self.HT = HT
        self.a  = a
        self.b  = b
        self.c  = c
        self.d  = d
        self.e  = e
        self.qa = qa
        self.g  = g
        self.h  = h
        self.j  = j
        self.AL = AL
        self.LE = LE
        self.VE = VE

    def _evaluate(self, x, out, *args, **kwargs):
        # 0 常量
        # todo：读取excel给变量赋值

        # 1 固定损耗
        # I 0 f 1 N 2

        # 2 死区损耗
        death_loss = 2.5 * 10 ** (-4) * x[:, 0] * x[:, 1]

        # 3 直流铜损
        direct_coper = 15 * x[:, 0] ** 2

        # 4电感铜损 铜损
        direct = x[:, 0] ** 2 * x[:, 2] * (self.OD - self.ID + 2 * self.HT) * 18 / 3000
        alternating = 8.7 * (10 ** 14) * (self.OD - self.ID + 2 * self.HT) / (self.AL ** 2 * x[:, 2] ** 3 * x[:, 1] ** 1.5)

        # 铁损temp:
        delta_I = 6.7 * (10 ** 9) / (self.AL * x[:, 2] ** 2 * x[:, 1] * 2 * 1.414)
        OE1 = (x[:, 0] + delta_I) * x[:, 2] * 1.25 / self.LE
        OE2 = x[:, 0] * x[:, 2] * 1.25 / self.LE
        B1 = ((self.a + self.b * OE1 + self.c * (OE1 ** 2)) / (1 + self.d * OE1 + self.e * OE1 ** 2)) ** self.qa
        B2 = ((self.a + self.b * OE2 + self.c * (OE2 ** 2)) / (1 + self.d * OE2 + self.e * OE2 ** 2)) ** self.qa
        delta_B = B1 - B2

        # 铁损last
        iron_loss = self.g * (delta_B ** self.h) * ((x[:, 1] / 1000) ** self.j) * self.VE / 1000

        # 5 电容
        capacity = 4.489 * 10 ** 20 / (self.AL ** 2 * x[:, 2] ** 4 * x[:, 1] ** 2)

        # 6 开关损耗
        switch_loss = (38 + 60 * x[:, 0]) * x[:, 1] * 10 ** (-6)

        f1 = ( death_loss + direct_coper + direct + alternating + iron_loss + capacity + switch_loss + 23 ) / (20 * x[:, 0] * 1000)
        # print(death_loss[-1],direct_coper[-1],direct[-1],alternating[-1],iron_loss[-1],capacity[-1],switch_loss[-1])
        out["F"] = np.column_stack([f1])


len1 =4
iter = 0
len = 22
time0 = time.time()
df = pd.read_excel('multi-variable-optimization/playdata.xlsx')

for index, row in df.iterrows():
    duration = time.time()-time0
    time0 = time.time()
    iter += 1

    try:
        if iter <= 6:

            print(f'\n last iter {duration} iter begin : {iter} \n')

            OD = row['OD']
            ID = row['ID']
            HT = row['HT']
            a  = row['a']
            b  = row['b']
            c  = row['c']
            d  = row['d']
            e  = row['e']
            qa = row['qa']
            g  = row['g']
            h  = row['h']
            j  = row['j']
            AL = row['AL']
            LE = row['LE']
            VE = row['VE']

            problem = DrSun(OD,ID,HT,a ,b ,c ,d ,e ,qa,g ,h ,j ,AL,LE,VE)
            algorithm = NSGA2(pop_size=40, eliminate_duplicates=False)
            res = minimize(problem,
                           algorithm,
                           ('n_gen',300),
                           verbose=False)

            X = res.X
            F = res.F
            f = open('result.txt', 'a+')

            try:
                print(X[-1][0],X[-1][1],X[-1][2])
                #写入文件
                f.write('{iter: <{len1}} {s1:0<{len}} {s2:0<{len}} {s3:0<{len}} '.format(iter = iter,len1 = len1, len = len,s1 = X[-1][0], s2 = X[-1][1], s3 = X[-1][2]))
            except IndexError:
                print(X[0], X[1], X[2])
                f.write('{iter: <{len1}} {s1:0<{len}} {s2:0<{len}} {s3:0<{len}} '.format(iter = iter,len1 = len1, len = len,s1 = X[0], s2 = X[1], s3 = X[2]))

            try:
                print(F[-1][0])
                f.write('{s1:0<{len}}\n'.format(len=len,s1 = F[-1][0]))
            except IndexError:
                print(F[0])
                f.write('{s1:0<{len}}\n'.format(len=len,s1 = F[0]))

            f.close()

    except AssertionError:
        print(f'{iter} error!')
