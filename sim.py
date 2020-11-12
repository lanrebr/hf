import pandas as pd
from matplotlib import pyplot
from math import sqrt
import json
from tank import Tank
from dual import Dual

class Sym():
    da: None  # upper dual tank
    db: None # lower dual tank
    dt: 0.0 #time increment
    pa: 0.0 #atmospheric pressure
    c: 0.0 # constant volue
    kf = 0.0 #friction coeficient
    ro = 0.0 #density
    h = 0.0 #integration steps
    n = 0 #number of steps
    sp = "true" #allow spill
    p = 0 # current inner pressure
    v = 0 # current inner volume
    c = p*v #fixed volume
    t = 0 # current time

    lsp=[] #inner spill array
    lv=[] #inner volume array
    lp=[] #inner presure array
    lt=[] #time array

    def import_data(self,data):
        param = data.get("parameters",[])
        self.kf = param.get("friction",0.01)
        self.ro = param.get("density",1000.0)
        self.pa = param.get("pressure",101325)
        self.h = param.get("increment",0.005)
        self.n = param.get("intervals",100)
        self.sp = param.get("spill","true")

        tanks = []
        jtks = data.get("tanks",[])
        for jtk in jtks:
            tank = Tank(self.ro,self.kf)
            tank.import_data(jtk)
            tanks.append(tank)
            #print(tank)

        self.da = Dual(tanks[0],tanks[1])
        self.db = Dual(tanks[2],tanks[3])

        self.p = self.pa
        self.v = self.da.tb.available(0) + self.db.ta.available(0)
        self.c = self.p*self.v
        self.t = 0

        self.lsp=[]
        self.lv=[]
        self.lp=[]
        self.lt=[]

    def coeff(self,k,dt):
        tadx = k[0]*dt
        tbdx = k[1]*dt
        tcdx = k[2]*dt
        tddx = k[3]*dt
        v = self.da.tb.available(tbdx) + self.db.ta.available(tcdx)
        p = self.c/v
        r = [0.0,0.0,0.0,0.0]
        r[0], r[1] = self.da.dv(self.pa,p,tadx,tbdx)
        r[2], r[3] = self.db.dv(p,self.pa,tcdx,tddx)
        return r

    def update(self,dx):
        qb = self.da.tb.update(dx[1],0)
        qc = self.db.ta.update(dx[2],0)
        qd = self.db.tb.update(dx[3],0)
        #compute spill from d to a
        spd = 0
        if self.sp=="true" and qd > 0:
            spd = qd*self.da.tb.ta
        qa = self.da.ta.update(dx[0],spd)
        v = self.da.tb.available(0) + self.db.ta.available(0)
        p = self.c/v
        self.t = self.t+self.h
        self.lsp.append(spd)
        self.lv.append(v)
        self.lp.append(p/self.pa)
        self.lt.append(self.t)

    def simulate(self):
        for i in range(self.n):
            # compute runge-kutta coefficents
            k0 = [0.0,0.0,0.0,0.0]
            k1 = self.coeff(k0,0)
            k2 = self.coeff(k1,self.h/2)
            k3 = self.coeff(k2,self.h/2)
            k4 = self.coeff(k3,self.h)

            dx = [0.0,0.0,0.0,0.0]
            for i in range(4):
                dx[i] = (self.h/6)*(k1[i]+2*k2[i]+2*k3[i]+k4[i])

            self.update(dx)

    def graph(self, file):
        fig, ax = pyplot.subplots(figsize=(30, 30), nrows=7, ncols=1)
        pyplot.show(block=False)

        self.da.ta.set_graph(self.t,self.lt,ax[0])
        self.da.tb.set_graph(self.t,self.lt,ax[1])
        self.db.ta.set_graph(self.t,self.lt,ax[2])
        self.db.tb.set_graph(self.t,self.lt,ax[3])

        ax_inf = ax[4]
        ax_inf.cla()
        ax_inf.set_title('Flow')
        ax_inf.set_xlabel('time')
        ax_inf.set_ylabel('m3')
        ax_inf.set_xlim([0,self.t])
        ax_inf.plot(self.lt,self.lsp,label='q')
        ax_inf.legend(loc='upper left')
        ax_inf.grid(True)

        ax_inf = ax[5]
        ax_inf.cla()
        ax_inf.set_title('Pressure')
        ax_inf.set_xlabel('time')
        ax_inf.set_ylabel('atm')
        ax_inf.set_xlim([0,self.t])
        ax_inf.plot(self.lt,self.lp,label='p')
        ax_inf.legend(loc='upper left')
        ax_inf.grid(True)

        ax_inf = ax[6]
        ax_inf.cla()
        ax_inf.set_title('Volume')
        ax_inf.set_xlabel('time')
        ax_inf.set_ylabel('m3')
        ax_inf.set_xlim([0,self.t])
        ax_inf.plot(self.lt,self.lv,label='v')
        ax_inf.legend(loc='upper left')
        ax_inf.grid(True)

        fig.tight_layout()

        pyplot.savefig(file,dpi=100)
        pyplot.draw()
        pyplot.pause(0.001)

    def csv(self, file):
        results = {"ax":self.da.ta.tx, "bx":self.da.tb.tx, "cx":self.db.ta.tx, "dx":self.db.tb.tx, "v":self.lv, "p":self.lp, "t":self.lt }
        df = pd.DataFrame(results, columns= ["ax","bx","cx","dx","v","p","t"])
        df.to_csv(file)

def run(name):
    with open("hf/data/"+name+".json") as f:
        data = json.load(f)
    sim = Sym()
    sim.import_data(data)
    sim.simulate()
    sim.graph("hf/png/"+name+".png")
    sim.csv("hf/data/"+name+".csv")

run("test01")

