import dbcon
from pprint import pprint as pp
from netaddr import *

dbs = dbcon.MyDB()
con = dbs.connect()

def get_free_net():
    sql = """SELECT * FROM net WHERE `rootnet` = 1 """
    root_net = dbs.queryone(sql)
    root_net = IPNetwork('%s/%s' % (root_net['red'], root_net['BM']))

    # pp(root_net)

    sql = """SELECT * FROM net WHERE `rootnet` != 1 """
    net = dbs.queryall(sql)
    # pp(net)

    used_net = []

    for n in net:
        used_net.append(IPNetwork('%s/30' % n['red']))
    
    free_nets = list(root_net.subnet(30))

    for fn in free_nets:
        if fn not in used_net:
            free_network = fn
            break

    return free_network

def get_next_vlan():
    sql = """SELECT * FROM vlans """
    all_vlan = dbs.queryall(sql)

    # print(all_vlan)
    vlan_num = []
    for vlan in all_vlan:
        vlan_num.append(vlan['vlan_num'])
    
    last_vlan = max(vlan_num)
    next_vlan = int(last_vlan) + 1
    return next_vlan

print(get_next_vlan())

print(get_free_net())