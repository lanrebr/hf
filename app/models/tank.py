import json

class Tank(): 
    id = "" # tank id
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
    x0 = 0.0 #initial hight
    px = 0.0 # horizontal position
    py = 0.0 # verical position

    def __init__(self, ro, kf):
        self.ro = ro
        self.kf = kf
        self.init()
        
    def init(self):
        self.tx = []
        self.x = self.x0

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
        self.tx.append(x)
        return qx

    def import_data(self,data):
        self.id = data.get("id","")
        self.ph = data.get("pipeheight",0.1)
        self.pd = data.get("pipediameter",0.05)
        self.th = data.get("tankheight",0.1)
        self.td = data.get("tankdiameter",1.0)
        self.px = data["positionx"]
        self.py = data["positiony"]
        x = data.get("level",0)
        if x<0:
            x=0
        elif x > self.ph + self.th:
            x = self.ph + self.th
        self.x0 = x
        self.pa = 3.1415*self.pd*self.pd/4
        self.pv = self.pa*self.ph
        self.ta = 3.1415*self.td*self.td/4
        self.tv = self.ta * self.th
        self.init()

    def export_data(self):
        dat ={}
        dat["id"] = self.id
        dat["pipeheight"] = self.ph
        dat["pipediameter"] = self.pd
        dat["tankheight"] = self.th
        dat["tankdiameter"] = self.td
        dat["level"] = self.x
        dat["pipearea"] = self.pa
        dat["pipevolume"] = self.pv
        dat["tankarea"] = self.ta
        dat["tankvolume"] = self.tv
        dat["positionx"]=self.px
        dat["positiony"]=self.py
        return dat

    def __str__(self):
        dat = self.export_data()
        return json.dumps(dat)

    def set_graph(self, t, lt, ax_inf):
        ax_inf.cla()
        ax_inf.set_title('Tank height')
        ax_inf.set_xlabel('time')
        ax_inf.set_ylabel('m')
        ax_inf.set_xlim([0,t])
        ax_inf.axhline(y=self.ph, color='r', linestyle='-')
        ax_inf.axhline(y=self.th+self.ph, color='b', linestyle='-')
        ax_inf.set_ylim([0,self.th+self.ph+0.1])
        ax_inf.plot(lt,self.tx,label=self.id)
        ax_inf.legend(loc='upper left')
        ax_inf.grid(True)