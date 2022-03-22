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

    def start(self):
        self.query()

    id = 'tuyanode'
