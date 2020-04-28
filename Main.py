import BT_Utils
from BT_Utils import BT_Manager
from BT_Utils import BT_GUI

BM = BT_Manager.BT_Manager()

win = BT_GUI.myGUI()


print("Hello BT User!\n")

while(BM.test_BTon()):
    input("Turn your BT on! Then click enter!")


BM.show_AdapterProperties()

input("If you are ready to start the discovery of Bluetooth device, click Enter!")

ans = True

while(ans):
    BM.Discovery()
    BM.show_DevsInfo()

    ans = input("Press 'D' to disconnect from this Device ---> ")
    BM.Disconnect()
    ans = input("Press 'C' to continue with Discovery, Q for quit ---> ")

    if(ans == 'C'):
        ans = True
    else:
        ans = False



