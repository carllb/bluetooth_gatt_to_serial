#!/usr/bin/env python3
import gatt
import sys
import struct
import serial
import serial.tools.list_ports

if len(sys.argv) < 2:
    print("Please suppply mac addr")
    exit()

print("Starting serial...")

ports = serial.tools.list_ports.comports()

if(len(ports) < 1):
	print("Please connect serial device")
	exit()
print("Using comm port: " + ports[0].device)

ser = serial.Serial(
    port=ports[0].device,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

if(not ser.isOpen()):
    print("Could not open serial!")


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
        #print("[%s] Resolved services" % (self.mac_address))
        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))
                if ('2a63' in characteristic.uuid ):
                    characteristic.enable_notifications()
                    print("Enabling power notifications")
                if ('2a19' in characteristic.uuid ):
                   #print('Battery: ' + characteristic.read_value())
                   characteristic.read_value()
                if ('ca31a533-a858-4dc7-a650-fdeb6dad4c14' in characteristic.uuid):
                    #print("Stuff:")
                    #print(characteristic.read_value())
                    characteristic.enable_notifications()


    def characteristic_value_updated(self, characteristic, value):
        if '2a63' in characteristic.uuid:
            power_bytes = value[2:4]
            acc_torque_bytes = value[4:6]
            val = int.from_bytes(power_bytes, byteorder='little')
            print('Power: ' + str(val) + ' watts')
            val_torque = struct.unpack("<H", acc_torque_bytes)
            print('Accumulated torque: ' + str(float(val_torque[0])/32) + ' n*m')
            ser.write(power_bytes)
        elif '2a19' in characteristic.uuid:
            val = int.from_bytes(value, byteorder='little')
            print('Battery level: ' + str(val) + ' %')
        else:
            print("Stuff:")
            print(value)


manager = gatt.DeviceManager(adapter_name='hci0')

device = AnyDevice(mac_address=sys.argv[1], manager=manager)
print("Trying to connect...")
device.connect()

manager.run()
