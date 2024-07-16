import numpy as np
import math
import cv2
import os
import random
import argparse

class Nodes:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.parent_x = []
        self.parent_y = []

# check the collision with obstacle and trim
def check_collision(x1,y1,x2,y2):
    _,theta = dist_and_angle(x2,y2,x1,y1)
    x=x2 + 15*np.cos(theta)
    y=y2 + 15*np.sin(theta)
    
    hy,hx=img.shape
    if y<0 or y>hy or x<0 or x>hx:
        #print("Point out of image bound")
        directCon = False
        nodeCon = False
    else:
        color=[]
        p = list(np.arange(x,end[0],(end[0]-x)/100))
        q = list(((end[1]-y)/(end[0]-x))*(p-x) + y)
        for i in range(len(p)):
            color.append(img[int(q[i]),int(p[i])])
        if (0 in color):
            directCon = False
        else:
            directCon = True

        color=[]
        p = list(np.arange(x,x2,(x2-x)/100))
        q = list(((y2-y)/(x2-x))*(p-x) + y)
        for i in range(len(q)):
            color.append(img[int(q[i]),int(p[i])])
        if (0 in color):
            nodeCon = False
        else:
            nodeCon = True
        
    return(x,y,directCon,nodeCon)

# return dist and angle b/w new point and nearest node
def dist_and_angle(x1,y1,x2,y2):
    dist = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
    angle = math.atan2(y2-y1, x2-x1)
    return(dist,angle)

# return the neaerst node index
def nearest_node(x,y):
    temp_dist=[]
    for i in range(len(node_list)):
        dist,_ = dist_and_angle(x,y,node_list[i].x,node_list[i].y)
        temp_dist.append(dist)
    return temp_dist.index(min(temp_dist))

# generate a random point in the image space
def rnd_point(h,l):
    new_y = random.randint(0, h)
    new_x = random.randint(0, l)
    return (new_x,new_y)


def RRT(img, img2, start, end):
    h,l= img.shape # dim of the loaded image
    # print(img.shape) # (384, 683)
    # print(h,l)

    node_list[0] = Nodes(start[0],start[1])
    node_list[0].parent_x.append(start[0])
    node_list[0].parent_y.append(start[1])

    # display start and end
    cv2.circle(img2, (start[0],start[1]), 5,(0,0,255),thickness=3, lineType=8)
    cv2.circle(img2, (end[0],end[1]), 5,(0,0,255),thickness=3, lineType=8)

    i=1
    pathFound = False
    while pathFound==False:
        nx,ny = rnd_point(h,l)
        #print("Random points:",nx,ny)
        nearest_ind = nearest_node(nx,ny)
        nearest_x = node_list[nearest_ind].x
        nearest_y = node_list[nearest_ind].y
        #print("Nearest node coordinates:",nearest_x,nearest_y)

        #check direct connection
        tx,ty,directCon,nodeCon = check_collision(nx,ny,nearest_x,nearest_y)
        #print("Check collision:",tx,ty,directCon,nodeCon)

        if directCon and nodeCon:
            print("Node can connect directly with end")
            node_list.append(i)
            node_list[i] = Nodes(tx,ty)
            node_list[i].parent_x = node_list[nearest_ind].parent_x.copy()
            node_list[i].parent_y = node_list[nearest_ind].parent_y.copy()
            node_list[i].parent_x.append(tx)
            node_list[i].parent_y.append(ty)

            cv2.circle(img2, (int(tx),int(ty)), 2,(0,0,255),thickness=3, lineType=8)
            cv2.line(img2, (int(tx),int(ty)), (int(node_list[nearest_ind].x),int(node_list[nearest_ind].y)), (0,255,0), thickness=1, lineType=8)
            cv2.line(img2, (int(tx),int(ty)), (end[0],end[1]), (255,0,0), thickness=2, lineType=8)

            for j in range(len(node_list[i].parent_x)-1):
                cv2.line(img2, (int(node_list[i].parent_x[j]),int(node_list[i].parent_y[j])), (int(node_list[i].parent_x[j+1]),int(node_list[i].parent_y[j+1])), (255,0,0), thickness=2, lineType=8)
            cv2.imwrite("out.jpg",img2)
            break

        elif nodeCon:
            #print("Nodes connected")
            node_list.append(i)
            node_list[i] = Nodes(tx,ty)
            node_list[i].parent_x = node_list[nearest_ind].parent_x.copy()
            node_list[i].parent_y = node_list[nearest_ind].parent_y.copy()
            # print(i)
            # print(node_list[nearest_ind].parent_y)
            node_list[i].parent_x.append(tx)
            node_list[i].parent_y.append(ty)
            i=i+1
            # display
            cv2.circle(img2, (int(tx),int(ty)), 2,(0,0,255),thickness=3, lineType=8)
            cv2.line(img2, (int(tx),int(ty)), (int(node_list[nearest_ind].x),int(node_list[nearest_ind].y)), (0,255,0), thickness=1, lineType=8)
            cv2.imshow("sdc",img2)
            cv2.waitKey(1)
            continue

        else:
            #print("No direct con. and no node con. :( Generating new rnd numbers")
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, default='world2.png',metavar='ImagePath', action='store', dest='imagePath')
    parser.add_argument('-start', type=int, default=[50,50], metavar='startCoord', dest='start', nargs='+')
    parser.add_argument('-stop', type=int, default=[600,400], metavar='stopCoord', dest='stop', nargs='+')
    
    args = parser.parse_args()

    img = cv2.imread(args.imagePath,0) 
    img2 = cv2.imread(args.imagePath) 
    start = tuple(args.start) 
    end = tuple(args.stop) 
    node_list = [0] 
    coordinates=[]
    
    print('start is ', start)
    print('end is ', end)
    RRT(img, img2, start, end)

