###########################################################################################################
'''
Implement of : Batch calcuate of Object Keypoint Similarity 
'''

import numpy as np
from decimal import Decimal, ROUND_HALF_UP

class OKSCalculator:
    def __init__(self, sigma, Decimal=Decimal, ROUND_HALF_UP=ROUND_HALF_UP):
        self.sigma = sigma
        self.Decimal = Decimal
        self.ROUND_HALF_UP = ROUND_HALF_UP

    def oks_pair(self, kpts1, kpts2, area, visibilitySame=False):
        vi1 = kpts1[..., -1]
        vi2 = kpts2[..., -1]
        if visibilitySame:
            vi1Low = vi1 < 0.1
            vi2Low = vi2 < 0.1
            vi1[vi1Low] = 0
            vi2[vi1Low] = 0
            vi1[vi2Low] = 0
            vi2[vi2Low] = 0

        if np.shape(kpts1) != np.shape(kpts2):
            raise ValueError("not same size")

        k = 2 * self.sigma
        s = area

        d = np.linalg.norm(kpts1 - kpts2, ord=2, axis=1)
        v = np.ones(len(d))

        for part in range(len(d)):
            if vi1[part] == 0 or vi2[part] == 0:
                d[part] = 0
                v[part] = 0

        if np.sum(v) != 0:
            OKS = (np.sum([(np.exp((-d[i]**2) / (2 * s * (k[i]**2)))) * v[i] for i in range(len(d))]) / np.sum(v))
        else:
            OKS = 0
        OKS = float(self.Decimal(str(OKS)).quantize(self.Decimal('0.000001'), rounding=self.ROUND_HALF_UP))
        return OKS

    def oks(self, kpts1, kpts2, areas, visibilitySame=False):
        n = kpts1.shape[0]
        m = kpts2.shape[0]
        oks_matrix = np.zeros((n, m))

        for i in range(n):
            for j in range(m):
                oks_matrix[i, j] = self.oks_pair(kpts1[i], kpts2[j], areas[j], visibilitySame)

        return oks_matrix



### -------------------------------------------------------------------------------------------
### example ###
sigma = [0.26, 0.25, 0.25, 0.35, 0.35, 0.79, 0.79, 0.72, 0.62, 0.79, 0.79, 0.72, 0.62, 0.26, 0.25, 0.25, 0.35]
calculator = OKSCalculator(sigma)

kpts1 = np.random.rand(2, 17, 3) 
kpts2 = np.random.rand(3, 17, 3)  
areas = np.random.rand(3)        

oks_matrix = calculator.oks(kpts1, kpts2, areas)
print(oks_matrix)
