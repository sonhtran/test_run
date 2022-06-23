import math
import time
import pathlib
import os
import serial
import signalenum
import BKLib
import matplotlib.pyplot as plt
from canlib import canlib, Frame

#set_up powersupply
myport = serial.Serial()
myport.baudrate = 57600
myport.port = 'COM3'
myport.timeout= 10
myport.write_timeout = 10
myport.open()

BK = BKLib.BK_XLN60026(myport)

#input
channel_number = 0
slaveid= 97
masterid= 96

control_level_test1 = 2
control_level_test2 = 0

speed_input_1=500
torque_input_1=1
pow_input_1=1000

speed_input_2=1000
torque_input_2=0.05
pow_input_2=1000

V_test1=48
V_test2=400

signal_selected_1= 30
signal_selected_2= 8200

#parameter motor
motor_off = 16
motor_on = 18
motor_drive = 20
#parameter data request
num_signal_select = 82
num_sample = 84

#create folder for ouput graph
path = os.path.join(pathlib.Path(__file__).parent.absolute(), "output")
try: 
    os.mkdir(path) 
except OSError as error: 
    None 
    
#function
def id_slave_to_master(opcode):
    b='{0:02b}'.format(1)+'{0:08b}'.format(slaveid)+'{0:08b}'.format(masterid)+'{0:02b}'.format(0)+'{0:09b}'.format(opcode)
    return int(b, 2)

def id_master_to_slave(opcode):
    b='{0:02b}'.format(1)+'{0:08b}'.format(masterid)+'{0:08b}'.format(slaveid)+'{0:02b}'.format(1)+'{0:09b}'.format(opcode)
    return int(b, 2)

def id_master_request_slave(opcode):
    b='{0:02b}'.format(1)+'{0:08b}'.format(masterid)+'{0:08b}'.format(slaveid)+'{0:02b}'.format(2)+'{0:09b}'.format(opcode)
    return int(b, 2)

def zero_position():
    frame = Frame(id_= id_master_to_slave(106),
                  data=[0, 0, 0, 0, 0, 0, 0, 0],
                  dlc=8,
                  flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def change_motor_mode(motor_mode):
    frame = Frame(id_= id_master_to_slave(2),
                  data=[00,00,2,motor_mode,00,00,00,00],
                  dlc=8,
                  flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def convert_motor_cmd(s_input,t_input,p_input):
    speed= int(float(s_input)*4096/10000)
    torque = int(float(t_input)*4096/10)
    pow = int(float(p_input)*4096/4000)

    speed= speed.to_bytes(2, 'big',signed=True)
    torque = torque.to_bytes(2, 'big',signed=True)
    pow = pow.to_bytes(2, 'big',signed=True)
    return (speed + torque + pow + b'\x00\x00')

def set_motor_command(in_data):
    frame = Frame(id_= id_master_to_slave(102),
            data=in_data,
            dlc=8,
            flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def set_motor_level(control_level):
    frame = Frame(id_= id_master_to_slave(9),
          data=[00,00,00,control_level,00,00,00,00],
          dlc=8,
          flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def select_signal_to_record(signalselect):
    signalcontrol =  b'\x00\x52' + (signalselect).to_bytes(4,'big',signed=False) + b'\x00\x00'
    frame = Frame(id_= id_master_to_slave(110),
                data= signalcontrol,
                dlc=8,
                flags=canlib.MessageFlag.EXT)
    ch.write(frame)   

def request_data(data_name):
    frame = Frame(id_= id_master_request_slave(110),
                data=[0, data_name, 0, 0, 0, 0, 0, 0],
                dlc=8,
                flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def trigger_record():
    frame = Frame(id_= id_master_to_slave(112),
              data=[0, 0, 0, 0, 0, 0, 0, 0],
              dlc=8,
              flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def download_record():
    frame = Frame(id_= id_master_request_slave(112),
                data=[0, 0, 0, 0, 0, 0, 0, 0],
                dlc=8,
                flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def read_record():
    i=1
    record_id = id_slave_to_master(112)
    oops=[]
    while i<a:
        try:
            frame = ch.readSpecificSkip(record_id)
            byte_val=[frame.data[i:i+2] for i in range(2, len(frame.data), 2)]
            # 3 since first word is just dummy data
            for x in range(3):
                byte_string = int.from_bytes(byte_val[x], "big",signed=True)
                oops.append(byte_string)
            i += 1
        except(canlib.canNoMsg) as ex:
            None
        except (canlib.canError) as ex:
            print(ex)
            i = a  

    new = [x*10/4096 for x in oops] 
    return new

def calrms(array):
    ms = 0
    for i in range(len(array)):
        ms = ms + array[i]**2
    ms = ms / len(array)
    rms = math.sqrt(ms)    
    return rms

BK.turn_on()
BK.set_volt(V_test1)

#create folder for ouput graph
path = os.path.join(pathlib.Path(__file__).parent.absolute(), "output")
try: 
    os.mkdir(path) 
except OSError as error: 
    None 
    
#function
def id_slave_to_master(opcode):
    b='{0:02b}'.format(1)+'{0:08b}'.format(slaveid)+'{0:08b}'.format(masterid)+'{0:02b}'.format(0)+'{0:09b}'.format(opcode)
    return int(b, 2)

def id_master_to_slave(opcode):
    b='{0:02b}'.format(1)+'{0:08b}'.format(masterid)+'{0:08b}'.format(slaveid)+'{0:02b}'.format(1)+'{0:09b}'.format(opcode)
    return int(b, 2)

def id_master_request_slave(opcode):
    b='{0:02b}'.format(1)+'{0:08b}'.format(masterid)+'{0:08b}'.format(slaveid)+'{0:02b}'.format(2)+'{0:09b}'.format(opcode)
    return int(b, 2)

def zero_position():
    frame = Frame(id_= id_master_to_slave(106),
                  data=[0, 0, 0, 0, 0, 0, 0, 0],
                  dlc=8,
                  flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def change_motor_mode(motor_mode):
    frame = Frame(id_= id_master_to_slave(2),
                  data=[00,00,2,motor_mode,00,00,00,00],
                  dlc=8,
                  flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def convert_motor_cmd(s_input,t_input,p_input):
    speed= int(float(s_input)*4096/10000)
    torque = int(float(t_input)*4096/10)
    pow = int(float(p_input)*4096/4000)

    speed= speed.to_bytes(2, 'big',signed=True)
    torque = torque.to_bytes(2, 'big',signed=True)
    pow = pow.to_bytes(2, 'big',signed=True)
    return (speed + torque + pow + b'\x00\x00')

def set_motor_command(in_data):
    frame = Frame(id_= id_master_to_slave(102),
            data=in_data,
            dlc=8,
            flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def set_motor_level(control_level):
    frame = Frame(id_= id_master_to_slave(9),
          data=[00,00,00,control_level,00,00,00,00],
          dlc=8,
          flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def select_signal_to_record(signalselect):
    signalcontrol =  b'\x00\x52' + (signalselect).to_bytes(4,'big',signed=False) + b'\x00\x00'
    frame = Frame(id_= id_master_to_slave(110),
                data= signalcontrol,
                dlc=8,
                flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def request_data(data_name):
    frame = Frame(id_= id_master_request_slave(110),
                data=[0, data_name, 0, 0, 0, 0, 0, 0],
                dlc=8,
                flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def trigger_record():
    frame = Frame(id_= id_master_to_slave(112),
              data=[0, 0, 0, 0, 0, 0, 0, 0],
              dlc=8,
              flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def download_record():
    frame = Frame(id_= id_master_request_slave(112),
                data=[0, 0, 0, 0, 0, 0, 0, 0],
                dlc=8,
                flags=canlib.MessageFlag.EXT)
    ch.write(frame)

def read_record():
    i=1
    record_id = id_slave_to_master(112)
    oops=[]
    while i<a:
        try:
            frame = ch.readSpecificSkip(record_id)
            byte_val=[frame.data[i:i+2] for i in range(2, len(frame.data), 2)]
            # 3 since first word is just dummy data
            for x in range(3):
                byte_string = int.from_bytes(byte_val[x], "big",signed=True)
                oops.append(byte_string)
            i += 1
        except(canlib.canNoMsg) as ex:
            None
        except (canlib.canError) as ex:
            print(ex)
            i = a  

    new = [x*10/4096 for x in oops] 
    return new

def calrms(array):
    ms = 0
    for i in range(len(array)):
        ms = ms + array[i]**2
    ms = ms / len(array)
    rms = math.sqrt(ms)    
    return rms

print("")
#turn on bus
ch = canlib.openChannel(channel_number)
ch.setBusParams(canlib.canBITRATE_1M)
ch.busOn()

#test1_forward
change_motor_mode(motor_off)
zero_position()
set_motor_command(convert_motor_cmd(speed_input_1, torque_input_1, pow_input_1))
set_motor_level(control_level_test1)
select_signal_to_record(signal_selected_1)
request_data(num_signal_select)

#read & decode answer
data_id=id_slave_to_master(110)
ch.readSyncSpecific(data_id, timeout=1000)
frame = ch.readSpecificSkip(data_id)
y = int(frame.data.hex()[4:12],16)
count =0
while y:
    count += y & 1
    y >>= 1

change_motor_mode(motor_on)
change_motor_mode(motor_drive)
time.sleep(1.5)
trigger_record()
request_data(num_sample)

#read & decode answer
ch.readSyncSpecific(data_id, timeout=1000)
frame = ch.readSpecificSkip(data_id)
hexstring=frame.data.hex()
a = math.ceil(int(hexstring[4:8],16)/3)

#request download record
download_record()
graph_data= read_record()
rms=[]
for i in range(count):
    sl=graph_data[i::count]
    plt.plot(sl)
    rms.append(calrms(sl))

signal_name= signalenum.signalname(signal_selected_1)
plt.savefig(path +'/test1_forward.png',dpi=200)
time.sleep(1)
plt.clf()
change_motor_mode(motor_on)
f = open(path +'/test1_forward.txt', 'w')
print ("Test 1 Forward RMS value: ")
f.write ("Test 1 Forward RMS value: \n")
for i in range(len(signal_name)):
    the_str = signal_name[len(signal_name)-1-i] + " = " + str(rms[i])
    print (the_str)
    f.write(the_str)
    f.write("\n")
print("\n")
time.sleep(1)



#test1_backward
change_motor_mode(motor_off)
set_motor_command(convert_motor_cmd(-speed_input_1, torque_input_1, pow_input_1))
select_signal_to_record(signal_selected_1)
request_data(num_signal_select)
change_motor_mode(motor_on)
#read & decode answer
data_id=id_slave_to_master(110)
ch.readSyncSpecific(data_id, timeout=1000)
frame = ch.readSpecificSkip(data_id)
y = int(frame.data.hex()[4:12],16)
count =0
while y:
    count += y & 1
    y >>= 1

change_motor_mode(motor_drive)
time.sleep(1.5)
trigger_record()
request_data(num_sample)

#read & decode answer
ch.readSyncSpecific(data_id, timeout=1000)
frame = ch.readSpecificSkip(data_id)
hexstring=frame.data.hex()
a = math.ceil(int(hexstring[4:8],16)/3)

#request download record
download_record()
graph_data= read_record()
rms=[]
for i in range(count):
    sl=graph_data[i::count]
    plt.plot(sl)
    rms.append(calrms(sl))

signal_name= signalenum.signalname(signal_selected_1)
plt.savefig(path +'/test1_backward.png',dpi=200)
time.sleep(1)
plt.clf()
change_motor_mode(motor_on)
f = open(path +'/test1_backward.txt', 'w')
print ("Test 1 Backward RMS value: ")
f.write ("Test 1 Backward RMS value: \n")
for i in range(len(signal_name)):
    the_str = signal_name[len(signal_name)-1-i] + " = " + str(rms[i])
    print (the_str)
    f.write(the_str)
    f.write("\n")
print("")
time.sleep(1)

BK.set_volt(0)


#test2_forward
BK.set_volt(V_test2)
change_motor_mode(motor_off)
set_motor_command(convert_motor_cmd(speed_input_2, torque_input_2, pow_input_2))
set_motor_level(control_level_test2)
select_signal_to_record(signal_selected_2)
request_data(num_signal_select)

#read & decode answer
data_id=id_slave_to_master(110)
ch.readSyncSpecific(data_id, timeout=1000)
frame = ch.readSpecificSkip(data_id)
y = int(frame.data.hex()[4:12],16)
count =0
while y:
    count += y & 1
    y >>= 1

change_motor_mode(motor_on)
change_motor_mode(motor_drive)
time.sleep(1.5)
trigger_record()
request_data(num_sample)

#read & decode answer
ch.readSyncSpecific(data_id, timeout=1000)
frame = ch.readSpecificSkip(data_id)
hexstring=frame.data.hex()
a = math.ceil(int(hexstring[4:8],16)/3)

#request download record
download_record()
graph_data= read_record()
rms=[]
for i in range(count):
    sl=graph_data[i::count]
    plt.plot(sl)
    rms.append(calrms(sl))

signal_name= signalenum.signalname(signal_selected_1)
plt.savefig(path +'/test2.png',dpi=200)
time.sleep(1)
plt.clf()
change_motor_mode(motor_on)

time.sleep(1)
change_motor_mode(motor_off)
BK.turn_off()
ch.busOff()
ch.close()
input("Press enter to exit !")