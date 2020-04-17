import dbus
import time
import json

import lxml
from lxml import etree
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

class BT_Manager:
    # Open a connection to the SystemBus
    def __init__(self):
        self.__bus = dbus.SystemBus()
        self.__adapter_proxy = self.get_AdapterProxy()
        self.__adapter_properties = self.get_AdapterProperties()
        self.__device_proxy = None
        self.__devs_info = {}
        self.__UUIDs = self.set_UUIDsDict()
        self.__found_UUIDs = []

    def set_UUIDsDict(self):
        with open('/home/spucis/Desktop/Alessio/Bluetooth/BT_Project/BT_Utils/UUIDs.txt') as UUIDs:
            return json.load(UUIDs)

    def get_AdapterProxy(self):
        # Build a proxy for the Adapter
        return self.__bus.get_object("org.bluez", "/org/bluez/hci0") 

    def get_AdapterProperties(self):
        return self.__adapter_proxy.GetAll("org.bluez.Adapter1", dbus_interface="org.freedesktop.DBus.Properties")
    
    def print_Properties(self, Prop):
        for k, v in Prop.items():
            if(k == 'UUIDs'):
                self.__found_UUIDs = v
            elif (k == 'ManufacturerData'):
                    print("ManufactureData: \n")
                    for kk, vv in Prop[k].items():
                        print("\t" + str(kk))
                        for el in vv:
                            print("\n - " + str(el))
            else:
                print(str(k) + ":\t" + str(v))
        
        print("\nService offered from " + Prop['Alias'] + ": \n")
        print("Service Name\t\t\t\tUUID\n")
        i = 0
        for UUID in self.__found_UUIDs:
            if UUID in self.__UUIDs.keys():
                print("[" + str(i) + "] - " + self.__UUIDs[UUID] + "\t\t\t\t" + UUID)
            else:
                print("[" + str(i) + "] - Unknown" + ":\t\t\t\t" + UUID)
            i = i + 1

        print("\n")

    def show_AdapterProperties(self):
        print("Those are your adapter Properties: \n")
        self.print_Properties(self.__adapter_properties)

    # WorkInProgress
    def test_BTon(self):
        try:
            self.__adapter_proxy.StartDiscovery(dbus_interface="org.bluez.Adapter1")
            self.__adapter_proxy.StopDiscovery(dbus_interface="org.bluez.Adapter1")
            return 0
        except:
            return 1

    def Discovery(self): 
        print("Discovering...")

        # Call the method StartDiscovery from the adapter api
        self.__adapter_proxy.StartDiscovery(dbus_interface="org.bluez.Adapter1")
        time.sleep(10)
        self.__adapter_proxy.StopDiscovery(dbus_interface="org.bluez.Adapter1")

        # Introspect the adapter, print and analyze the xml to find the nearby devices
        introspection = self.__adapter_proxy.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable")

        # Using lxml library, turn the introspection string into a tree and find the xml tags "node"
        # These xml tags nodes will contains the mac addresses of the nearby devices
        tree = etree.fromstring(introspection)

        addresses = []
        for child in tree:
            if child.tag == 'node':
                addresses.append(child.attrib['name'])
        
        for addr in addresses:
            device_path = "/org/bluez/hci0/" + addr
            device_proxy = self.__bus.get_object("org.bluez", device_path)
            info = device_proxy.GetAll("org.bluez.Device1", dbus_interface="org.freedesktop.DBus.Properties")
            self.__devs_info[info['Address']] = info['Alias']
    
    def show_DevsInfo(self):
        if(self.__devs_info != None):
        
            print("I've found some devices! Here they are!:\n")

            i = 0
            for k, v in self.__devs_info.items():
                print("[" + str(i) + "] " + "- Alias: " + v + ", Address: " + k + "\n")
                i = i + 1

            num = input("Type the number of the device you are interested in: ")

            self.set_ChosenDev(int(num))
            self.show_DevProperties()

        else:
            print("Sorry, i've found zero devices!\n")

    def set_ChosenDev(self, num):
        addr = list(self.__devs_info.keys())[num]
        device_path = "/org/bluez/hci0/dev_" + addr.replace(':', '_')
        self.__device_proxy = self.__bus.get_object("org.bluez", device_path)
        
    def show_DevProperties(self):
        info_dict = self.__device_proxy.GetAll("org.bluez.Device1", dbus_interface="org.freedesktop.DBus.Properties")
        self.print_Properties(info_dict)
        
        ans = input("Select the number of the Service you would like to use ---> ")
        self.Connect(ans)

    def Pair(self):
        info_dict = self.__device_proxy.GetAll("org.bluez.Device1", dbus_interface="org.freedesktop.DBus.Properties")
        if(info_dict['Paired'] == 0):
            try:
                self.__device_proxy.Pair(dbus_interface="org.bluez.Device1")
            except:
                print("Pair doesen't needed\n")

    def Connect(self, num):
        # Connect to the Device using org.bluez.Device1.Connect
        UUID = self.__found_UUIDs[int(num)]
        info_dict = self.__device_proxy.GetAll("org.bluez.Device1", dbus_interface="org.freedesktop.DBus.Properties")

        self.Pair()
        
        try:
            self.__device_proxy.ConnectProfile(UUID, dbus_interface="org.bluez.Device1")
            print("Connected to " + info_dict['Alias'] + "with UUID " + UUID + "\n")

        except dbus.DBusException as err:
            print("Something went wrong! The error message is: " + err.get_dbus_message() + "\n")
            show = input("May i show you all the device again? Y-N ---> ")
            if(show == 'Y'):
                self.show_DevsInfo()
            else:
                retry = input("Would you like to try again with the same device? Y-N ---> ")
                if(retry == 'Y'):
                    self.Connect(num)

    def Disconnect(self):
        self.__device_proxy.Disconnect(dbus_interface="org.bluez.Device1")
