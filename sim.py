import pandas as pd
from matplotlib import pyplot
from math import sqrt

from tank import Tank
from dual import Dual

kf = 0.001  #friction loss coefficient
ro = 1000  #density

#tank a
aph = 2.1 #pipe height
apd = 0.05 #pipe diameter
ath = 1.0  #tank height
atd = 1.0  #tank diameter
atx = 2.5  #tank x

ta = Tank(aph,apd,ath,atd,ro,kf,atx)

#tank b
bph = 0.1  #pipe height
bpd = 0.05 #pipe diameter
bth = 1.0  #tank height
btd = 1.0  #tank diameter
btx = 0.0  #tank water level

tb = Tank(bph,bpd,bth,btd,ro,kf,btx)

#tank c
cph = 0.1  #pipe height
cpd = 0.05 #pipe diameter
cth = 1.0  #tank height
ctd = 1.0  #tank diameter
ctx = 1    #tank water level

tc = Tank(cph,cpd,cth,ctd,ro,kf,ctx)

#tank d
dph = 1.0  #pipe height
dpd = 0.05 #pipe diameter
dth = 0.05  #tank height
dtd = 1.0  #tank diameter
dtx = 1    #tank water level

td = Tank(dph,dpd,dth,dtd,ro,kf,dtx)

da = Dual(ta,tb)
db = Dual(tc,td)

#initialize
pa = 101325 # 1 atm
p = pa
v = tb.available(0) + tc.available(0)
c = p*v
h = 0.005
t = 0

lax=[]
lbx=[]
lcx=[]
ldx=[]
lsp=[]
lv=[]
lp=[]
lt=[]

for i in range(8000):

    # first coefficient
    v1 = tb.available(0) + tc.available(0)
    p1 = c/v1
    tav1, tbv1 = da.dv(pa,p1,0,0)
    tcv1, tdv1 = db.dv(p1,pa,0,0)

    # second coefficient at x + h*(dv/dt)/2
    tadx = tav1*h/2
    tbdx = tbv1*h/2
    tcdx = tcv1*h/2
    tddx = tdv1*h/2
    v2 = tb.available(tbdx) + tc.available(tcdx)
    p2 = c/v2
    tav2, tbv2 = da.dv(pa,p2,tadx,tbdx)
    tcv2, tdv2 = db.dv(p2,pa,tcdx,tddx)

    # third coefficient at x + h*(dv/dt)/2
    tadx = tav2*h/2
    tbdx = tbv2*h/2
    tcdx = tcv2*h/2
    tddx = tdv2*h/2
    v3 = tb.available(tbdx) + tc.available(tcdx)
    p3 = c/v3
    tav3, tbv3 = da.dv(pa,p3,tadx,tbdx)
    tcv3, tdv3 = db.dv(p3,pa,tcdx,tddx)

    # forth coefficient at x + h*(dv/dt)
    tadx = tav3*h
    tbdx = tbv3*h
    tcdx = tcv3*h
    tddx = tdv3*h
    v4 = tb.available(tbdx) + tc.available(tcdx)
    p4 = c/v4
    tav4, tbv4 = da.dv(pa,p4,tadx,tbdx)
    tcv4, tdv4 = db.dv(p4,pa,tcdx,tddx)

    #compute increments
    qb = tb.update(h*(tbv1+2*tbv2+2*tbv3+tbv4)/6,0)
    qc = tc.update(h*(tcv1+2*tcv2+2*tcv3+tcv4)/6,0)
    qd = td.update(h*(tdv1+2*tdv2+2*tdv3+tdv4)/6,0)

    #compute spill from d to a
    spd = 0
    if qd > 0:
        spd = qd*td.ta
    qa = ta.update(h*(tav1+2*tav2+2*tav3+tav4)/6,spd)

    v = tb.available(0) + tc.available(0)
    p = c/v
    t = t+h

    lax.append(ta.x)
    lbx.append(tb.x)
    lcx.append(tc.x)
    ldx.append(td.x)
    lsp.append(spd)
    lv.append(v)
    lp.append(p/pa)
    lt.append(t)

fig, ax = pyplot.subplots(figsize=(30, 30), nrows=7, ncols=1)
pyplot.show(block=False)
ax_inf = ax[0]
ax_inf.cla()
ax_inf.set_title('Tank height')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('m')
ax_inf.set_xlim([0,t])
ax_inf.axhline(y=ta.ph, color='r', linestyle='-')
ax_inf.axhline(y=ta.th+ta.ph, color='b', linestyle='-')
ax_inf.set_ylim([0,ta.th+ta.ph+0.1])
ax_inf.plot(lt,lax,label='a')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

ax_inf = ax[1]
ax_inf.cla()
ax_inf.set_title('Tank height')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('m')
ax_inf.set_xlim([0,t])
ax_inf.axhline(y=tb.ph, color='r', linestyle='-')
ax_inf.axhline(y=tb.th+tb.ph, color='b', linestyle='-')
ax_inf.set_ylim([0,tb.th+tb.ph+0.1])
ax_inf.plot(lt,lbx,label='b')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

ax_inf = ax[2]
ax_inf.cla()
ax_inf.set_title('Tank height')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('m')
ax_inf.set_xlim([0,t])
ax_inf.axhline(y=tc.ph, color='r', linestyle='-')
ax_inf.axhline(y=tc.th+tc.ph, color='b', linestyle='-')
ax_inf.set_ylim([0,tc.th+tc.ph+0.1])
ax_inf.plot(lt,lcx,label='c')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

ax_inf = ax[3]
ax_inf.cla()
ax_inf.set_title('Tank height')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('m')
ax_inf.set_xlim([0,t])
ax_inf.axhline(y=td.ph, color='r', linestyle='-')
ax_inf.axhline(y=td.th+td.ph, color='b', linestyle='-')
ax_inf.set_ylim([0,td.th+td.ph+0.1])
ax_inf.plot(lt,ldx,label='d')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

ax_inf = ax[4]
ax_inf.cla()
ax_inf.set_title('Flow')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('m3')
ax_inf.set_xlim([0,t])
ax_inf.plot(lt,lsp,label='q')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

ax_inf = ax[5]
ax_inf.cla()
ax_inf.set_title('Pressure')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('atm')
ax_inf.set_xlim([0,t])
ax_inf.plot(lt,lp,label='p')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

ax_inf = ax[6]
ax_inf.cla()
ax_inf.set_title('Volume')
ax_inf.set_xlabel('time')
ax_inf.set_ylabel('m3')
ax_inf.set_xlim([0,t])
ax_inf.plot(lt,lv,label='v')
ax_inf.legend(loc='upper left')
ax_inf.grid(True)

fig.tight_layout()
pyplot.savefig('png/tank.png',dpi=100)
pyplot.draw()
pyplot.pause(0.001)

results = {"ax":lax, "bx":lbx, "cx":lcx, "dx":ldx, "v":lv, "p":lp, "t":lt }
df = pd.DataFrame(results, columns= ["ax","bx","cx","dx","v","p","t"])
df.to_csv("heron.csv")