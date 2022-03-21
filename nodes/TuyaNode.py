import udi_interface

LOGGER = udi_interface.LOGGER


class TuyaNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(TuyaNode, self).__init__(polyglot, primary, address, name)
        self.address = address

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

    def start(self):
        self.query()

    id = 'tuyanode'
