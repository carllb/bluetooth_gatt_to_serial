#!/usr/bin/env python3
import gatt

class AnyDevice(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))

    def services_resolved(self):
        super().services_resolved()

        print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))
                print(dir(characteristic))
                print("*****")


class AnyDeviceManager(gatt.DeviceManager):
    def __init__(self, adapter_name, mac_list):
        super().__init__(adapter_name)
        self.mac_list = mac_list

    def device_discovered(self, device):
        #print("Discovered [%s] %s" % (device.mac_address, device.alias()))
        if ('powertap' in device.alias() and 'L' in device.alias()):
            print(device.mac_address)
            manager.stop()
            
manager = AnyDeviceManager(adapter_name='hci0',mac_list=[])
manager.start_discovery()
manager.run()


#74:5c:4b:0b:4e:f2


#device = AnyDevice(mac_address='66:12:d1:56:6b:3c', manager=manager)

