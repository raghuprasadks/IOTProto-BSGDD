# -*- coding: utf-8 -*-
#https://www.youtube.com/watch?v=90YK59maJeQ

from Adafruit_IO import Client 


def isMotionDetected():
    aio = Client("kaushalya","0707ccd5345744edb15999c21cb5db27") 
    #aio.send('motiondetector', 1) 
    isDetected = aio.receive("motiondetector").value 
    print (isDetected) 
    print(type(isDetected))
    print("done")
    if (int(isDetected) == 1):
        print('in true')
        return True
    else:
        print('in false')
        return False
    
isMotionDetected()    
    
