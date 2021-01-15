from plyfile import PlyData
import matplotlib.pyplot as plt
import PIL.Image as pil
import numpy as np
import loadTXT

plydata = PlyData.read('data/fused_backup.ply')
images, ims = loadTXT.loadData(0,10) #offset, amount : start at 0, load 10
density = 100 # increase this number to make renders more sparse. renders 1/density points


def map(imageID): #move all the points relative to the camera position and rotation

    width,height = images[imageID].width, images[imageID].height
    focalLength = images[imageID].focal_x

    rotation =  images[imageID].R()
    camera = images[imageID].C()

    imData = ims[imageID]
    points = []
    for i in range(0,plydata.elements[0].count):#plydata.elements[0].count
        if(i%density==0):
            x_cross = plydata.elements[0][i][0]
            y_cross = plydata.elements[0][i][1]
            depth = plydata.elements[0][i][2] 
            rgb = np.array([plydata.elements[0][i][3],plydata.elements[0][i][4],plydata.elements[0][i][5]])
            
            coords = np.array([x_cross,y_cross,depth])

            coords[0]=coords[0]-camera[0] 
            coords[1]=coords[1]-camera[1]
            coords[2]=coords[2]-camera[2]
            coords = rotation.dot(coords) #rotate

            points.append([coords[0],coords[1],coords[2],rgb]) 

    return render(points,images[imageID].focal_x,images[imageID].width,images[imageID].height)


def render(points,focalLength,width,height): #splat points onto a buffer
    buffer = np.zeros((height,width,3))
    zbuffer = np.empty(shape=(height,width))
    zbuffer.fill(100000)

    for p in points:

        x_cross = p[0]
        y_cross = p[1] 
        depth = p[2]
        if(depth > 0):
            xDist = x_cross*(focalLength/depth) 
            yDist = y_cross*(focalLength/depth) 
            if(xDist < ((width/2)) and xDist > -((width/2)) and yDist < ((height/2)) and yDist > -((height/2))):
                if(depth > 0 and depth < zbuffer[int((yDist+(height/2)))][int((xDist+(width/2)))] ):
                    buffer[int((yDist+height/(2)))][int((xDist+(width/2)))] = p[3]
                    zbuffer[int((yDist+height/(2)))][int((xDist+(width/2)))] = depth

    return buffer.astype(np.uint8) ,zbuffer

namingID = 0 

print("Loaded",len(images))
for i in range(len(images)):
    if(images[i].width>512 and images[i].height>512):
        namingID +=1
        print("Rendering",i)
        buff,zbuff= map(i)
        
        plt.imsave("out/"+str(namingID).zfill(4)+"_color.png",buff)
        zbuff= np.where(zbuff == 100000,0, zbuff) # replace max val with 0
        im = pil.fromarray(np.uint8(zbuff/15*256), 'L') #apply threshold of 15
        im.save("out/"+str(namingID).zfill(4)+"_depth.png")
        plt.imsave("out/"+str(namingID).zfill(4)+"_reference.png",ims[i])
    

