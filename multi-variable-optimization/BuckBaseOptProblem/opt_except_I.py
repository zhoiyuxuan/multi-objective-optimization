import numpy as np
from pymoo.core.problem import Problem

class Opt2Problem(Problem):

    def __init__(self,OD,ID,HT,a,b,c,e,qa,g,h,j,AL,LE,
                 Rin = 10,Rout = 10,Rnds = 7.5, RLds = 7.5, Vin = 30, Vout = 20, iout = 2,
                 ttr = 10,Qg = 40,VDD = 5,
                 tdead = 125,
                 rc = 10,d = 2,
                 fixed_loss=21,
                 fdown = 10000.0, fup = 200000,
                 Ndown = 0.0, Nup = 70.0):

        super().__init__(n_var=2,
                         n_obj=1,
                         n_ieq_constr=0,
                         xl=np.array([fdown,Ndown]),
                         xu=np.array([fup,Nup]))

        self.OD = OD
        self.ID = ID
        self.HT = HT
        self.a  = a
        self.b  = b
        self.c  = c
        self.e  = e
        self.qa = qa
        self.g  = g
        self.h  = h
        self.j  = j
        self.AL = AL
        self.LE = LE

        #公式中
        self.Rin = Rin
        self.Rout = Rout
        self.Rnds = Rnds
        self.RLds = RLds
        self.Vin = Vin
        self.Vout = Vout
        self.iout = iout
        self.ttr  = ttr
        self.Qg = Qg
        self.VDD = VDD
        self.tdead  = tdead
        self.rc = rc
        self.d = d
        self.fixed_loss = fixed_loss


    def _evaluate(self, x, out, *args, **kwargs):
        # 0 常量
        # todo：读取excel给变量赋值

        # 1 固定损耗
        # I 0 f 1 N 2
        fixed_loss = self.fixed_loss

        # 2 直流铜损
        direct_coper = (self.Rin + self.Rnds) * (self.Vout * self.iout / self.Vin) **2 + (self.Rout + self.RLds) * self.iout**2

        # 3 开关损耗
        switch_loss = 2 * self.Qg * self.VDD * (10 ** (-6)) + self.Vin * self.iout * x[:, 0] * self.ttr * (10 ** (-6))

        # 4 死区损耗
        death_loss = 2 * self.iout * x[:, 0] * (10 ** (-6)) * self.tdead

        # 5 电容损耗
        delta_I = (self.Vin - self.Vout) * self.Vout * (10**9) / (2 * 1.414 * self.Vin * x[:, 0] * self.AL * x[:, 1] ** 2)
        capacity_loss  = self.rc * delta_I **2

        # 6 电感损耗
        # (1) 直流电感铜损
        direct_copper_l = self.iout ** 2 * x[:, 1] * (self.OD - self.ID + 2* self.HT) * 18 / (250 * 3.1415926535 * self.d **2)
        # (2) 交流电感通讯
        alternating_current_l = x[:, 1] * (self.OD - self.ID + 2*self.HT) * x[:, 0] ** 0.5 *9 * delta_I ** 2 /(132* 3.1415926535 * 1000)

        # 7 铁损temp:
        delta_I = 6.7 * (10 ** 9) / (self.AL * x[:, 2] ** 2 * x[:, 1])
        OE1 = (self.iout + delta_I)* x[:, 1] *12.5 / self.LE
        OE2 = (self.iout * x[:, 1] * 12.5)/self.LE
        B1 = ((self.a + self.b * OE1 + self.c * (OE1 ** 2)) / (1 + self.d * OE1 + self.e * OE1 ** 2)) ** self.qa
        B2 = ((self.a + self.b * OE2 + self.c * (OE2 ** 2)) / (1 + self.d * OE2 + self.e * OE2 ** 2)) ** self.qa
        delta_B = B1 - B2
        # 铁损last
        iron_loss = self.g * (delta_B ** self.h) * (( x[:, 0] /1000) ** self.j) * self.VE / 1000

        result = ( fixed_loss + direct_coper + switch_loss + death_loss + capacity_loss + direct_copper_l + alternating_current_l+ iron_loss) / (2 * self.iout * 1000 * self.Vout)
        # print(death_loss[-1],direct_coper[-1],direct[-1],alternating[-1],iron_loss[-1],capacity[-1],switch_loss[-1])
        out["F"] = np.column_stack([result])

        # f N

