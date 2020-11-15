from math import sqrt

class Dual():
    ta = None
    tb = None

    def __init__(self,ta,tb):
        self.ta = ta
        self.tb = tb
    
    def dv(self, tap, tbp, dax, dbx):
        # tap + 0.5*ro*tav^2+ ro*g*(x+dax) = tbp + 0.5*ro*tbv^2+ro*g*(y+dy)+0.5*ro*fk*(pah/pad+pbh/pbd)*pv^2
        # tav*taa = pv*pad
        # tbv*tba = pv*pbd
        # tav = (pad/taa)*pv
        # tbv = (pbd/tba)*pv
        # tap + 0.5*ro*(pad/taa)^2*pv^2+ ro*g*(x+dx) = tbp + 0.5*ro*(pbd/tba)^2*pv^2+ro*g*(y+dy)+0.5*ro*fk*(pah/pad+pbh/pbd)*pv^2
        # 0.5*ro*[(pad/taa)^2 - (pbd/tba)^2 - fk*(pah/pad+pbh/pbd)]*pv^2  = tbp - tap +ro*g*(y-x+dy-dx)
        # pv^2 = 2*[(tbp - tap)/ro + g*(y-x+dy-dx)]/[(pad/taa)^2 - (pbd/tba)^2 - fk*(pah/pad+pbh/pbd)]
        # pv^2 = 2*[(tap - tbp)/ro + g*(tax-tbx+dax-dbx)]/[fk*(pah/pad+pbh/pbd) + (pba/tba)^2 - (paa/taa)^2]

        pah = self.ta.ph/self.ta.pd
        raa = self.ta.pa/self.ta.ta
        if self.ta.sts() == 0:
            pah = self.ta.x/self.ta.pd
            raa = 1

        pbh = self.tb.ph/self.tb.pd
        rba = self.tb.pa/self.tb.ta
        if self.tb.sts() == 0:
            pbh = self.tb.x/self.tb.pd
            rba = 1
        
        vd = self.ta.kf*pah + self.tb.kf*pbh + rba*rba - raa*raa
        dp = tap/self.ta.ro - tbp/self.tb.ro
        vn = 2*(dp + 9.8*(self.ta.x-self.tb.x+dax-dbx))

        v2 = vn/vd
        v = 0
        if v2>0.0:
            v = sqrt(v2)
        
        tav = -raa*v
        tbv = rba*v
        return tav, tbv

        

