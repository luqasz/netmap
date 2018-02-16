# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

# Devices are considered to be directly connected when:
# switch A sees (in direction of switch B) different hosts then
# switch B sees (in direction of switch A)
# In other words, they do not have a common switch between them.

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


def nearest_neighbours(macs, haystack):
    for sw_name in haystack:
        for port, fdb in switch_fdb[sw_name].items():
            fdb = set(fdb)
            # No common macs means direct connection
            if macs.isdisjoint(fdb):
                yield SwitchPort(name=sw_name, port=port)


for sw, sw_mac in switches.items():
    for port, port_macs in switch_fdb[sw].items():
        port_macs = set(port_macs)
        # Construct a tuple with switch names which are visable on a given port.
        haystack = tuple(sw_name for sw_name, mac in switches.items() if mac in port_macs)
        for found in nearest_neighbours(macs=port_macs, haystack=haystack):
            conn = Connection(swa=sw, swa_port=port, swb=found.name, swb_port=found.port)
            print(conn)
