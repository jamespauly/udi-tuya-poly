import udi_interface
import tinytuya
import json

from nodes import TuyaNode

# IF you want a different log format than the current default
LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom


class TuyaController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(TuyaController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.primary = primary
        self.address = address

        self.Notices = Custom(polyglot, 'notices')
        self.Parameters = Custom(polyglot, 'customparams')

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameter_handler)

        self.poly.ready()
        self.poly.addNode(self)

    def parameter_handler(self, params):
        self.Notices.clear()
        self.Parameters.load(params)
        # self.check_params()

    def start(self):
        LOGGER.info('Staring Tuya NodeServer')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        self.discover()

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))
        self.discover()

    def discover(self, *args, **kwargs):
        LOGGER.info("Starting Tuya Device Discovery")
        devices_list = json.loads(self.Parameters['devices'])

        LOGGER.info(json.dumps(devices_list))
        scan_results = tinytuya.deviceScan()

        for value in scan_results.values():
            ip = value['ip']
            device_id = value['gwId']
            if len(device_id) > 10:
                device_id = device_id[:10]

            LOGGER.info(f"Device Scan Device IP: {ip}")
            for dict_found in [x for x in devices_list if x["id"] == value['gwId']]:
                value['name'] = dict_found['name']
                value['key'] = dict_found['key']
                device_node = self.poly.getNode(device_id)
                if device_node is None:
                    LOGGER.info(f"Adding Node: {device_id} - {dict_found['name']}")
                    self.poly.addNode(TuyaNode(self.poly, self.address, device_id, dict_found['name'], value))

        LOGGER.info('Finished Tuya Device Discovery')

    def delete(self):
        LOGGER.info('Deleting Tuya Node Server')

    def stop(self):
        LOGGER.info('Daikin Tuya stopped.')

    id = 'tuya'
    commands = {
        'QUERY': query,
        'DISCOVER': discover
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]
