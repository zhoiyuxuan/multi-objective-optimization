from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from opt_all import Opt3Problem
from opt_except_I import Opt2Problem

#todo:从handle interface传入参数过来,interface做一个dict的函数然后传过来


#是否优化I
iout = 2

#算法参数
pop_size = 40
ngen = 300

if iout != 0:
    problem  = Opt2Problem()
else:
    problem  = Opt3Problem()

algorithm = NSGA2(pop_size=pop_size, eliminate_duplicates=False)
res = minimize(problem,
               algorithm,
               ('n_gen', ngen),
               verbose=False)

X = res.X
F = res.F