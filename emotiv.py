import os
import platform
system_platform = platform.system()
import socket
import pywinusb.hid as hid
import gevent
from Crypto.Cipher import AES
from Crypto import Random
from gevent.queue import Queue
from subprocess import check_output
import binascii
import sys
import random

sensor_bits = {
    'F3': [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    'FC5': [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9],
    'AF3': [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27],
    'F7': [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45],
    'T7': [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63],
    'P7': [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65],
    'O1': [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83],
    'O2': [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121],
    'P8': [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139],
    'T8': [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157],
    'F8': [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175],
    'AF4': [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177],
    'FC6': [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195],
    'F4': [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
}
quality_bits = [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]

battery_values = {
    255: [100], 254: [100], 253: [100],252: [100],251: [100],250: [100],249: [100],248: [100],247: [99],246: [97],245: [93],244: [89],243: [85],242: [82],241: [77],240: [72],239: [66],238: [62],237: [55],236: [46],235: [32],234: [20],233: [12],232: [6],231: [4],230: [3],229: [2],228: [2],227: [2],226: [1],225: [0],224: [0]
}



g_battery = 0
tasks = gevent.queue.Queue()



# =========================================== GET_LEVEL
def get_level(data, bits):
    level = 0
    for i in range(13, -1, -1):
        level <<= 1
        b = (bits[i] // 8) + 1
        o = bits[i] % 8
        level |= (data[b] >> o) & 1
    return level

# =========================================== IS_OLD_MODEL
def is_old_model(serial_number):
        if "GM" in serial_number[-2:]:
                return False
        return True


# =========================================== EmotivPacket
class EmotivPacket(object):
    def __init__(self, data, sensors, model):
        try:
            global g_battery

            self.counter = data[0]
            self.raw_data = data

            #print(str(self.counter))
            self.battery = g_battery

            if self.counter > 127:
                self.battery = self.counter
                if self.battery > 224:
                     g_battery = battery_values[self.battery]
                     #g_battery = 100
                     self.counter = 128

            self.sync = self.counter == 0xe9
            self.gyro_x = data[29] - 106
            self.gyro_y = data[30] - 105
            sensors['X']['value'] = self.gyro_x
            sensors['Y']['value'] = self.gyro_y

            for name, bits in list(sensor_bits.items()):
                #Get Level for sensors subtract 8192 to get signed value
                value = get_level(self.raw_data, bits) - 8192
                setattr(self, name, (value,))
                sensors[name]['value'] = value
            self.old_model = model
            self.handle_quality(sensors)
            self.sensors = sensors
        except Exception as e:
             print("EmotivPacket Error ", sys.exc_info()[0],  sys.exc_info()[1],  sys.exc_info()[2], " : ",  e)



    # ================================================== HANDLE_QUALITY
    def handle_quality(self, sensors):
        if self.old_model:
            current_contact_quality = get_level(self.raw_data, quality_bits) // 540
        else:
            current_contact_quality = get_level(self.raw_data, quality_bits) // 1024
        sensor = self.raw_data[0]
        if sensor == 0 or sensor == 64:
            sensors['F3']['quality'] = current_contact_quality
        elif sensor == 1 or sensor == 65:
            sensors['FC5']['quality'] = current_contact_quality
        elif sensor == 2 or sensor == 66:
            sensors['AF3']['quality'] = current_contact_quality
        elif sensor == 3 or sensor == 67:
            sensors['F7']['quality'] = current_contact_quality
        elif sensor == 4 or sensor == 68:
            sensors['T7']['quality'] = current_contact_quality
        elif sensor == 5 or sensor == 69:
            sensors['P7']['quality'] = current_contact_quality
        elif sensor == 6 or sensor == 70:
            sensors['O1']['quality'] = current_contact_quality
        elif sensor == 7 or sensor == 71:
            sensors['O2']['quality'] = current_contact_quality
        elif sensor == 8 or sensor == 72:
            sensors['P8']['quality'] = current_contact_quality
        elif sensor == 9 or sensor == 73:
            sensors['T8']['quality'] = current_contact_quality
        elif sensor == 10 or sensor == 74:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 11 or sensor == 75:
            sensors['AF4']['quality'] = current_contact_quality
        elif sensor == 12 or sensor == 76 or sensor == 80:
            sensors['FC6']['quality'] = current_contact_quality
        elif sensor == 13 or sensor == 77:
            sensors['F4']['quality'] = current_contact_quality
        elif sensor == 14 or sensor == 78:
            sensors['F8']['quality'] = current_contact_quality
        elif sensor == 15 or sensor == 79:
            sensors['AF4']['quality'] = current_contact_quality
        else:
            sensors['Unknown']['quality'] = current_contact_quality
            sensors['Unknown']['value'] = sensor
        return current_contact_quality

# ============================================== EMOTIV
class Emotiv(object):
    def __init__(self, display_output=True, serial_number="", is_research=False):
        self.running = True
        self.packets = gevent.queue.Queue()
        self.packets_received = 0
        self.packets_processed = 0
        self.battery = 0
        self.display_output = display_output
        self.is_research = is_research
        self.sensors = {
            'F3': {'value': 0, 'quality': 0},
            'FC6': {'value': 0, 'quality': 0},
            'P7': {'value': 0, 'quality': 0},
            'T8': {'value': 0, 'quality': 0},
            'F7': {'value': 0, 'quality': 0},
            'F8': {'value': 0, 'quality': 0},
            'T7': {'value': 0, 'quality': 0},
            'P8': {'value': 0, 'quality': 0},
            'AF4': {'value': 0, 'quality': 0},
            'F4': {'value': 0, 'quality': 0},
            'AF3': {'value': 0, 'quality': 0},
            'O2': {'value': 0, 'quality': 0},
            'O1': {'value': 0, 'quality': 0},
            'FC5': {'value': 0, 'quality': 0},
            'X': {'value': 0, 'quality': 0},
            'Y': {'value': 0, 'quality': 0},
            'Unknown': {'value': 0, 'quality': 0}
        }

        self.serial_number = serial_number  # You will need to set this manually for OS X.
        self.old_model = False

    # =========================================================== SETUP WINDOWS
    def setup_windows(self):
        devices = []
        try:
            devicesUsed = 0
            for device in hid.find_all_hid_devices():
                print("Product name ",device.product_name)
                print("device path ", device.device_path)
                print("instance id ", device.instance_id)
                print("\r\n")
                useDevice = ""
                
                if device.vendor_id != 0x21A1 and device.vendor_id != 0xED02:
                    continue
                if device.product_name == 'Brain Waves':
                    
                    print("\n", device.product_name, " Found!\n")
                    useDevice = input("Use this device? [Y]es? ")
                   
                    if useDevice.upper() == "Y":                   
                         devicesUsed += 1             
                         devices.append(device)
                         device.open()
                         self.serial_number = device.serial_number
                         device.set_raw_data_handler(self.handler)
                elif device.product_name == 'EPOC BCI':
                    
                    print("\n", device.product_name, " Found!\n")
                    useDevice = input("Use this device? [Y]es? ")
                    if useDevice.upper() == "Y":                   
                         devicesUsed += 1
                         devices.append(device)
                         device.open()
                         self.serial_number = device.serial_number
                         device.set_raw_data_handler(self.handler)
                elif device.product_name == '00000000000':
                    
                    print("\n", device.product_name, " Found!\n")
                    useDevice = input("Use this device? [Y]es? ")

                    if useDevice.upper() == "Y":
                         devicesUsed += 1
                         devices.append(device)
                         device.open()
                         self.serial_number = device.serial_number
                         device.set_raw_data_handler(self.handler)
                elif device.product_name == 'Emotiv RAW DATA':
                    
                    print("\n", device.product_name, " Found!\n")
                    useDevice = input("Use this device? [Y]es? ")

                    if useDevice.upper() == "Y":
                         devicesUsed += 1
                         devices.append(device)
                         device.open()
                         self.serial_number = device.serial_number
                         device.set_raw_data_handler(self.handler)
                         
            print("\n\n Devices Selected: ", devicesUsed) 
            crypto = gevent.spawn(self.setup_crypto, self.serial_number)
            console_updater = gevent.spawn(self.update_console)
            input("Press Enter to continue...")
            while self.running:
                try:
                    gevent.sleep(0)

                except KeyboardInterrupt:
                    self.running = False
        finally:
            for device in devices:
                device.close()
            gevent.kill(crypto, KeyboardInterrupt)
            gevent.kill(console_updater, KeyboardInterrupt)

    # ================================================================ DATA HANDLER
    def handler(self, data):
        assert data[0] == 0
        tasks.put_nowait(''.join(map(chr, data[1:])))
        self.packets_received += 1
        return True

    # ================================================================ SETUP CRYPTO
    def setup_crypto(self, sn):

        if is_old_model(sn):
            self.old_model = True

        k = ['\0'] * 16
        k[0] = sn[-1]
        k[1] = '\0'
        k[2] = sn[-2]
        if self.is_research:
            k[3] = 'H'
            k[4] = sn[-1]
            k[5] = '\0'
            k[6] = sn[-2]
            k[7] = 'T'
            k[8] = sn[-3]
            k[9] = '\x10'
            k[10] = sn[-4]
            k[11] = 'B'
        else:
            k[3] = 'T'
            k[4] = sn[-3]
            k[5] = '\x10'
            k[6] = sn[-4]
            k[7] = 'B'
            k[8] = sn[-1]
            k[9] = '\0'
            k[10] = sn[-2]
            k[11] = 'H'
        k[12] = sn[-3]
        k[13] = '\0'
        k[14] = sn[-4]
        k[15] = 'P'

        mykey = ''.join(k)
        key = str.encode(mykey,'utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_ECB)

        while self.running:

            while not tasks.empty():
                task = tasks.get()
                data_block = bytes(task, encoding='latin-1')
                mydata = cipher.decrypt(data_block[0:16]) + cipher.decrypt(data_block[16:32])
                self.packets.put_nowait(EmotivPacket(mydata, self.sensors, self.old_model))
                self.packets_processed += 1
                gevent.sleep(0)
            gevent.sleep(0)

    input("Press Enter to continue...")

    # ====================================================== DEQUEUE
    def dequeue(self):
        return self.packets.get()

    # ====================================================== CLOSE GREENLETS
    def close(self):
        self.running = False
    # ====================================================== UPDATE CONSOLE
    def update_console(self):
        if self.display_output:
            while self.running:

                os.system('cls')
                print("Data in Queue: ", str(tasks.qsize()))
                print("Packets Received: ", self.packets_received, "Packets Processed:", self.packets_processed)
                print('\n'.join("%s Reading: %s Quality: %s" %
                                (k[1], self.sensors[k[1]]['value'],
                                 self.sensors[k[1]]['quality']) for k in enumerate(self.sensors)))
                print("Battery: ", g_battery)
                gevent.sleep(.001)

# ============================================================ __MAIN__
if __name__ == "__main__":
    a = Emotiv()
    #a = Emotiv()
    try:
        a.setup_windows()
    except KeyboardInterrupt:
        a.close()
