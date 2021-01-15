from image import Image
from rotation import Quaternion
import numpy as np
from os import listdir
from os.path import isfile, join
import PIL.Image as pil

imgPath = "data/imgs/"
cameraTXTPath = "data/cameras.txt" 
imageTXTPath = "data/images.txt"

### offset: how far off the start you want to load
### amount: how many do you want to load
def loadData(offset,amount):
    print("Loading Data")
    cameras = loadCameras()
    ims = []
    f = open(imageTXTPath, "r")
    images = []
    count = 0
    for x in f:
        if ".jpg" in x:
            i = x.split(" ")
            if(count< (offset+amount) and count > offset):
                i[9] = i[9][:-1]
                if isfile(imgPath+i[9]):
                    images.append(Image(i[9],
                    int(i[8]),
                    Quaternion(np.array(i[1:5]).astype(np.float)),
                    np.array(i[5:8]).astype(np.float),
                    cameras[np.where(cameras[:,0]==int(i[8]))[0][0]][1],
                    cameras[np.where(cameras[:,0]==int(i[8]))[0][0]][2],
                    cameras[np.where(cameras[:,0]==int(i[8]))[0][0]][3]))
                    ims.append(np.asarray(pil.open(imgPath+i[9])))
            count +=1
    return images, ims

def loadCameras():
    cameras = []
    f = open(cameraTXTPath, "r")
    for x in f:
        if "PINHOLE" in x:
            x = x.split()
            cameras.append([int(x[0]),int(x[2]),int(x[3]),float(x[4])])
    print(len(cameras))
    return np.array(cameras)
