# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

# Switch are considered to be directly connected when:
# switch A sees (in direction of switch B) different hosts then
# switch B sees (in direction of switch A)

from collections import namedtuple

Connection = namedtuple('Connection', ('swa', 'swa_port', 'swb', 'swb_port'))
SwitchPort = namedtuple('SwitchPort', ('name', 'port'))

switches = {
        'sw1': '00:00:00:00:00:11',
        'sw2': '00:00:00:00:00:22',
        'sw3': '00:00:00:00:00:33',
        'sw4': '00:00:00:00:00:44',
        }

switch_fdb = {
        'sw1': {
                2: (switches['sw2'], switches['sw3'], switches['sw4']),
            },
        'sw2': {
                1: (switches['sw1'],),
                2: (switches['sw3'], switches['sw4']),
            },
        'sw3': {
                1: (switches['sw2'], switches['sw1']),
                2: (switches['sw4'],),
            },
        'sw4': {
                1: (switches['sw1'], switches['sw3'], switches['sw2']),
            },
        }

connections = set()


def nearest_neighbour(target_sw, macs):
    # z macs wez macki wszyskich switchy
    macs = set(macs)
    found_on = (sw_name for sw_name, mac in switches.items() if mac in macs)
    for sw_name in found_on:
        for port, fdb in switch_fdb[sw_name].items():
            fdb = set(fdb)
            if macs.isdisjoint(fdb):
                return SwitchPort(name=sw_name, port=port)
        # przejdz po switchach i
        # poszukaj portow na ktorych widac target_sw
        # iterujac po tym znajdz set(macs).isdisjoint(macki z portu danego sw)


for sw, sw_mac in switches.items():
    # wez tablice fdb dla danego sw
    # dla kazdego portu i mackow z portu, poszukaj najblizszego sasiada
    for port, port_macs in switch_fdb[sw].items():
        found = nearest_neighbour(sw, port_macs)
        if found:
            conn = Connection(swa=sw, swa_port=port, swb=found.name, swb_port=found.port)
            print(conn)
            connections.add(conn)
