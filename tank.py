class Tank(): 
    ph = 0 #pipe height
    pd = 0 #pipe diameter
    pa = 0 #pipe area
    pv = 0 #pipe volume
    th = 0 #tank height
    td = 0 #tank diameter
    ta = 0 #tank area
    tv = 0 #tank volume
    ro = 0 #content density
    kf = 0 #friction coefficient
    x = 0.0 #current heigt

    def __init__(self, ph, pd, th, td, ro, kf, x):
        self.ph = ph
        self.pd = pd
        self.th = th
        self.td = td
        self.ro = ro
        self.kf = kf
        if x<0:
            x=0
        elif x > ph + th:
            x = ph + th
        self.x = x
        self.pa = 3.1415*self.pd*self.pd/4
        self.pv = self.pa*self.ph
        self.ta = 3.1415*self.td*self.td/4
        self.tv = self.ta * self.th

    def sts(self):
        if self.x <0:
            return -1 #empty
        elif self.x<self.ph:
            return 0 #pipe
        elif self.x < self.ph + self.th:
            return 1  #tank
        else:
            return 2  #full

    def area(self):
        sts = self.sts()
        if sts==0:
            return self.pd
        elif sts==1:
            return self.pa
        return 0

    def volume(self,dx):
        sts = self.sts()
        if sts == -1:
            return 0
        elif sts == 0:
            return self.pa*(self.x + dx)
        elif sts == 1:
            return self.ta*(self.x + dx - self.ph) + self.pv
        elif sts == 2:
            return self.tv + self.pv

    def available(self,dx):
        return self.tv + self.pv + self.pa*(self.th+self.ph) - self.volume(dx)

    def update(self,dx,sp):
        x = self.x + dx
        if sp >0 and x < self.ph:
            if x + sp/self.pa > self.ph:
                sp = sp - (self.ph - x)*self.pa
                x = self.ph
            else:
                x = x + sp/self.pa
                sp = 0
        if sp >0 and x < self.ph + self.th:
            if x + sp/self.ta > self.ph + self.th:
                x = self.ph + self.th
            else:
                x = x + sp/self.ta
    
        qx = 0
        if x < 0:
            qx = - x
            x = 0
        elif x > self.th + self.ph:
            qx = x - self.th - self.ph
            x = self.th+self.ph
        self.x = x
        return qx
        
    def der(self, dx, tp, pp):
        # tp + 0.5*ro*tv^2 + ro*g*(x+dx) = pp + 0.5*ro*(1+kf*ph/pd)pv^2
        # pa*pv = ta*tv => pv = ta*tv/pa
        # tp + 0.5*ro*tv^2 + ro*g*(x+dx) = pp + 0.5*ro*(1+kf*ph/pd)*ta^2*tv^2/pa^2 
        # 0.5*ro*(1 - (1+kf*ph/pd)*ta^2/pa^2)*tv^2 = pp - tp - ro*g*(x+dx)
        # tv^2 = 2*[(tp-pp)/ro + g*(x+dx)]/[(1+kf*ph/pd)*ta^2/pa^2-1]
        sts = self.sts()
        dn = 1.0
        if sts==0:
            dn = self.kf*(self.x+dx)/self.pd
        elif sts>0:
            ph = (1+self.kf*self.ph/self.pd)
            rt = self.ta/self.pa
            dn = ph*rt*rt-1

        dc = [(tp-pp)/self.ro + 9.8*(self.x + dx)]/dn
        if dc >0:
            return sqrt(2*dc)
        else:
            return 0
