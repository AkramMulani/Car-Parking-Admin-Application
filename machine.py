import serial

try:
    ser = serial.Serial(port="COM10",baudrate=9600)
    connected=True
except:
    connected=False

def isConnected():
    return connected

def read():
    try:
        data = ser.readline().decode('Ascii')
        return data
    except:
        return None

def write(data:str):
    ser.write(data.encode('Ascii'))
