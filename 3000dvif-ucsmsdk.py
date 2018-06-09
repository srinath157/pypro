from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.vnic.VnicEther import VnicEther
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
from collections import OrderedDict
import itertools
import math


class combgen(object):
    """docstring for combgen"""
    def __init__(self, vnic_count, vlans):
        super(combgen, self).__init__()
        a = ['eth' + str(_) for _ in range(vnic_count)]
        b = [s for i in range(1, len(a) + 1) for s in itertools.combinations(a, i)]
        print len(b)               
        self.vlans = vlans
        count = len(b) if len(b) < 2980 else 2980
        x = [_ for _ in range(self.vlans, self.vlans+count)]
        self.out1 = dict(zip(x, b)).items()
        z = [(eth, vlan) for vlan, ethlist in self.out1 for eth in ethlist]
        self.out2 = z
        print len(z)
        self.out4 = {}
        for _ in a: self.out4[_] = [z[i][1] for i in range(len(z)) if z[i][0] == _]
        vlanm=len(b)/2+1
        k = int(math.ceil(vlanm/350.0) if vlanm > 350 else 1)
        self.out3 = {}
        ygen = self.tuplegen()
        for j in range(int(k)):
            for _ in a: self.out3[ygen.next()] = [z[i][1] for i in range(j*len(z) / k, (j+1)*len(z)/k) if z[i][0] == _]

    def tuplegen(self):
        i=1
        while True:
            for _ in range(32):
                yield (i,_)
            i+=1


x = combgen(12,101)
p = OrderedDict(sorted(x.out3.items()))

p1 = {}
for (sp,eth), vlan in p.items():
    try:
        p1['sp'+ str(sp)].append((eth, vlan))
    except:
        p1['sp'+ str(sp)] = [(eth, vlan)]



handle = UcsHandle('10.127.97.156', 'admin', 'nbv12345')
handle.login()


for sp,eth_vlan in p1.items():
    mo = LsServer(parent_mo_or_dn="org-root", name="x{}".format(sp))
    for ev in eth_vlan:
        mo_1 = VnicEther(parent_mo_or_dn=mo,
                        switch_id="A-B",
                        ident_pool_name="default", 
                        addr="derived",
                        name="{}".format('eth'+ str(ev[0])),
                        mtu="9000")
        for _ in ev[1]:
            VnicEtherIf(parent_mo_or_dn=mo_1, name="x{}".format(_))
     
    
    handle.add_mo(mo)
    handle.commit()
    
handle.logout()
print "loggedout"

