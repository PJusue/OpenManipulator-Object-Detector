import serial
import time



def scanningObjects(laser,joint2,joint3):
    dec=0
    angle=0
    for index in range(1,1000,1):
        time.sleep(0.3)
        manipulator=serial.Serial("/dev/ttyACM1",57600)
        laser=serial.Serial('/dev/ttyACM0',115200)
	valueRead=laser.readline()
	print(valueRead)
        valueCleaned=cleanData(valueRead)
	print(valueCleaned)
	print(type(valueCleaned))
        if valueCleaned < 25 and valueCleaned is not None:
            if dec==0:
	       return angle-0.15
	    else:
		return angle
        else:
            if dec==0:
                angle+=0.10
            else:
                angle-=0.10
            if abs(-angle-1.6)<0.000001:
                dec=0
            elif abs(angle-1.6)<0.000001:
                dec=1
            else:
                pass
	manipulator.write('joint,{0},{1},{2},0\n'.format(angle,joint2,joint3))
        manipulator.close()
	laser.close()
#	return angle
def pickUpAnObject(angle,joint2,joint3,joint4):
    for index in range(0,7,1):
        ser=serial.Serial('/dev/ttyACM1',57600)
        #joint2-=0.25
        joint3+=0.22
	print(joint3)
        ser.write('joint,{0},{1},{2},{3}\n'.format(angle,joint2,joint3,joint4))
        ser.close()
        time.sleep(0.5)
    ser=serial.Serial('/dev/ttyACM1',57600)
    ser.write('gripper,0.00\n')
    ser.close()
    time.sleep(1)
    ser=serial.Serial('/dev/ttyACM1',57600)
    ser.write('joint,{0},{1},{2},{3}\n'.format(angle,joint2,joint3,joint4-0.5))
    ser.close()
    time.sleep(3)
    ser=serial.Serial('/dev/ttyACM1',57600)
    ser.write('gripper,0.01\n')
    ser.close()

def cleanData(valueRead):
    try:
    	valueClean=int(valueRead.decode('utf-8'))
    	return valueClean
    except:
	pass
    return None
        
def main():
    manipulator=serial.Serial("/dev/ttyACM1",57600)
    print("Manipulator connected")
    laser=serial.Serial('/dev/ttyACM0',115200)
    print("Laser connected)")
    joint1=0
    joint2=1.2
    joint3=-1.4
    manipulator.write('joint,0,{0},{1},0\n'.format(joint2,joint3))
    time.sleep(6)
    manipulator.close()
    angle=scanningObjects(laser,joint2,joint3)
    manipulator.close()
    manipulator=serial.Serial('/dev/ttyACM1',57600)
    joint2=-0.42
    joint3=-0.92
    joint4=1.11
    manipulator.write('joint,{0},{1},{2},{3}\n'.format(angle,joint2,joint3,joint4))
    pickUpAnObject(angle,joint2,joint3,joint4)

if __name__ == '__main__':
    main()
    
   
