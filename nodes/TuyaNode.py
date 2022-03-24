import json

import udi_interface
import tinytuya

LOGGER = udi_interface.LOGGER

class TuyaNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, device):
        super(TuyaNode, self).__init__(polyglot, primary, address, name)
        self.address = address
        self.name = name
        self.device = device

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (node)')
            self.query()
        else:
            LOGGER.info('longPoll (node)')
            pass

    def query(self):
        LOGGER.info("Query sensor {}".format(self.address))
        d = tinytuya.BulbDevice(self.device['gwId'], self.device['ip'], self.device['key'])
        d.set_version(3.3)
        LOGGER.info("Node Name {}".format(self.name))
        node_status = d.status()
        LOGGER.info("Node Status {}".format(str(node_status)))
        node_brightness = node_status['dps']['107']/10
        LOGGER.info("Node Brightness {}".format(node_brightness))
        node_duration = node_status['dps']['105'].replace('MIN', '')
        LOGGER.info("Node On Time {}".format(node_duration))

        self.setDriver('GV1', 40, True)
        self.setDriver('GV2', 5, True)
        # self.setDriver('GV1', int(node_brightness), True)
        # self.setDriver('GV2', int(node_duration), True)

    def start(self):
        self.query()

    id = 'tuyanode'

    commands = {
        'QUERY': query
    }

    drivers = [
        {'driver': 'GV1', 'value': 0, 'uom': 51},
        {'driver': 'GV2', 'value': 0, 'uom': 45}
    ]
