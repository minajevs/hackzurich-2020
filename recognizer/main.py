import numpy as np
import cv2
import sys
import imutils
from pylsd import lsd
from random import randint
from segment import *
from copy import deepcopy

process_stage = 0
prev_stage = -1
ix,iy = -1,-1
flagx = 0
edit_flag = 0
boxes=[]

def get_hog() :
    winSize = (100,100)
    blockSize = (10,10)
    blockStride = (5,5)
    cellSize = (10,10)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradient = True

    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels, signedGradient)

    return hog

def draw_result_boxes(img,boxes):
    if process_stage == 0:
        for (x,y,w,h),_ in boxes:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
    else:
        text = ['Valve','W.pump','P.sensor','Consumer','V.sensor', 'Generator', 'Mxv-2', 'H.exchanger', 'T.sensor']
        font = cv2.FONT_HERSHEY_SIMPLEX
        for ((x,y,w,h),idx) in boxes:
            cv2.putText(img, text[idx] ,(x-5,y-5),font,0.6,(250,0,0),1,cv2.LINE_AA)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)

def svm_predict(th2,rects,boxes):
    ## HOG+SVM prediction
    svm = cv2.ml.SVM_load("svm_data.dat")
    hog = get_hog();
    for x,y,x2,y2 in rects:
    	region = cv2.resize(th2[y:y2,x:x2],(100,100),interpolation = cv2.INTER_CUBIC)
    	hog_des = hog.compute(region)
    	_,result = svm.predict(np.array(hog_des,np.float32).reshape(-1,3249))
        idx = int(result[0][0]) + 3
        boxes.append([[int(x),int(y),int(x2-x),int(y2-y)],idx])
    return boxes

# mouse callback function
def mouse_event(event,x,y,flags,param):
    global process_stage,prev_stage,ix,iy,boxes,edit_flag
    boxes_t = []
    del_list = []
    edit = 0
    if event == cv2.EVENT_LBUTTONDBLCLK:
        prev_stage = process_stage
        process_stage = process_stage+1

    elif event == cv2.EVENT_RBUTTONDOWN:
        if process_stage == 0:
            ix,iy = x,y
        elif process_stage == 1:
            i = 0
            for (x0,y0,w,h),_ in boxes:
                if(x>x0 and y>y0 and x<x0+w and y<y0+h):
                    edit = i
                i = i+1

            cv2.namedWindow("edit")
            cv2.moveWindow("edit",960,100)
            cv2.setMouseCallback('edit',mouse_event_edit,edit)

            text = ['Valve','W.pump','P.sensor','Consumer','V.sensor', 'Generator', 'Mxv-2', 'H.exchanger', 'T.sensor']
            edit = np.zeros((400,150,3),dtype=np.uint8)
            cv2.rectangle(edit,(0,0),(150,500),(255,255,255),-1)
            for i in xrange(len(text)):
                cv2.rectangle(edit,(20,i*40+20),(120,i*40+50),(0,0,255),-1)
                cv2.putText(edit, text[i] ,(30,i*40+40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
            while(edit_flag != 1):
                cv2.imshow("edit",edit)
                if(cv2.waitKey(1) & 0xFF == ord('q')):
                    break
            cv2.destroyWindow("edit")
            edit_flag = 0

    elif event == cv2.EVENT_RBUTTONUP:
        if process_stage == 0:
            bw = cv2.imread("data/skel.pgm",0)
            ends = skeleton_points(bw[iy:y,ix:x])
            for i in xrange(ends[0].size):
                ends[1][i] = ends[1][i]+ix
                ends[0][i] = ends[0][i]+iy
            v_pairs,h_pairs = lines_between_ends(ends)
            v_boxes = box_between_ends(v_pairs)
            h_boxes = box_between_ends(h_pairs)
            boxes_t = v_boxes + h_boxes

            if len(boxes_t) == 1:
                boxes.append(boxes_t[0])
            else:
                th = cv2.imread("data/th.pgm",0)
                rects = []
                boxes_t = []
                rects.append([ix,iy,x,y])
                boxes_t = svm_predict(th,rects,boxes_t)
                boxes.append(boxes_t[0])

    elif event == cv2.EVENT_LBUTTONDOWN:
        if process_stage == 0:
            i = 0
            for (x0,y0,w,h),_ in boxes:
                if(x>x0 and y>y0 and x<x0+w and y<y0+h):
                    del_list.append(i)
                i = i+1
            del_list.sort(reverse=True)
            for i in del_list:
                del boxes[i]

def mouse_event_edit(event,x,y,flags,param):
    global edit_flag
    if event == cv2.EVENT_LBUTTONDOWN:
        text = ['Valve','W.pump','P.sensor','Consumer','V.sensor', 'Generator', 'Mxv-2', 'H.exchanger', 'T.sensor']

        for i in xrange(len(text)):
            if(x>20 and y>i*40+20 and x<120 and y<i*40+50):
                boxes[param][1] = i
                edit_flag = 1
                break


if __name__ == "__main__":
    cv2.namedWindow("recognizer")
    cv2.moveWindow("recognizer",200,100)
    cv2.setMouseCallback('recognizer',mouse_event)

    srcf = 'data/Untitled1.jpg'
    src = cv2.imread(srcf)
    src = imutils.resize(src,width=640)
    org = src.copy()
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ## endpoint operations
    img = cv2.GaussianBlur(gray,(9,9),0)
    th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    		cv2.THRESH_BINARY_INV,11,2)
    th2 = th.copy()
    bw  = thinning(th)
    cv2.imwrite("data/skel.pgm",bw)
    cv2.imwrite("data/th.pgm",th2)
    ends = skeleton_points(bw)
    ## detection of ground, capacitor, v_source
    v_pairs,h_pairs = lines_between_ends(ends)
    v_boxes = box_between_ends(v_pairs)
    h_boxes = box_between_ends(h_pairs)
    boxes = v_boxes + h_boxes

    ## segmentation operations
    ## remove founded symbols and connection lines
    for ((x,y,w,h),idx) in boxes:
    	th[y:y+h,x:x+w] = 0

    ## detect vert and hori lines then remove them from binary image
    lsd_lines = lsd(th)
    for line in lsd_lines:
    	x1,y1,x2,y2,w = line
    	angle = np.abs(np.rad2deg(np.arctan2(y1 - y2, x1 - x2)))
    	if (angle<105 and angle>75) or angle>160 or angle<20:
            cv2.line(th,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,0),6)

    kernel = np.ones((11,11),np.uint8)
    closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)

    rects = []
    # Find Blobs on image
    cnts = cv2.findContours(closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    for c in cnts:
        if cv2.contourArea(c)<80:
            continue
        else:
            x,y,w,h = cv2.boundingRect(c)
            maxedge = max(w,h)
            x,y = int(((2*x+w)-maxedge)/2),int(((2*y+h)-maxedge)/2)
            rects.append([x-10,y-10,x+maxedge+10,y+maxedge+10])

    rects = non_max_suppression_fast(np.array(rects,dtype=float),0.1)

    boxes = svm_predict(th2,rects,boxes)

    while (1):
        src = org.copy()

        if process_stage == 2 and prev_stage == 1:
            ## find nodes and nodes end points
            for ((x,y,w,h),idx) in boxes:
            	bw[y:y+h,x:x+w]  = 0
                th2[y:y+h,x:x+w] = 0

            node_closing = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)
            node_temp = cv2.findContours(node_closing.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]

            node_cnts = []
            node_ends = []
            pairs = np.vstack((v_pairs,h_pairs))
            i = 0
            for c in node_temp:
                if cv2.contourArea(c)>50:
                    color = (randint(0,255),randint(0,255),randint(0,255))

                    node_cnts.append((i,c))
                    ## draw each node contour and find ends point of node
                    node_mask = np.zeros(th.shape,np.uint8)
                    cv2.drawContours(node_mask, [c] , 0, (255,255,255), 3)
                    cv2.drawContours(src,[c],0,color,3)

                    node_thin = thinning(node_mask)
                    ends_n = skeleton_points(node_thin)
                    for j in xrange(ends_n[0].size):
                        x,y = (ends_n[1][j],ends_n[0][j])
                        node_ends.append([i,[x,y]])
                        ##cv2.circle(src,(x,y),2,color,-1)

                    cv2.circle(src,(20,20*i+20),7,color,-1)
                    cv2.putText(src, str(i) ,(30,20*i+25),cv2.FONT_HERSHEY_SIMPLEX,0.6,color,1,cv2.LINE_AA)
                    i = i+1

            ## find which comp connected which nodes
            comp_ends = []
            i = 0
            for ((x,y,w,h),idx) in boxes:
                x1,y1 = (int(x+w/2),y)
                x2,y2 = (x,int(y+h/2))
                x3,y3 = (x+w,int(y+h/2))
                x4,y4 = (int(x+w/2),y+h)

                angle = 0
                minDist = [10000, 10000]     ## nearest points distance
                minIdx  = [-1,-1,-1,-1]      ## [first nearest node_id, second ne. node_id,first point index, second p. ind]
                min_edg = [[-1,-1],[-1,-1]]  ## [first point x,y, second point x,y]
                k = 0
                for (j,(xe,ye)) in node_ends:
                    ## 4 point of box
                    dist1 = np.sqrt((xe-x1)**2+(ye-y1)**2)
                    dist2 = np.sqrt((xe-x2)**2+(ye-y2)**2)
                    dist3 = np.sqrt((xe-x3)**2+(ye-y3)**2)
                    dist4 = np.sqrt((xe-x4)**2+(ye-y4)**2)

                    ## find nearest two nodes two box
                    tempDist = sorted([dist1, dist2, dist3, dist4])[0]
                    if(minDist[0]>tempDist):
                        minDist[1] = minDist[0]
                        minIdx [1] = minIdx [0]
                        min_edg[1] = min_edg[0]
                        minDist[0] = tempDist
                        minIdx [0] = j
                        minIdx [2] = k
                        min_edg [0] = [xe,ye]
                    elif(minDist[1]>tempDist):
                        minDist[1] = tempDist
                        minIdx [1] = j
                        minIdx [3] = k
                        min_edg [1] = [xe,ye]
                    k = k+1

                if idx == 2:    # if ground comp
                    comp_ends.append([i,idx,minIdx[0],minIdx[0],min_edg[0],min_edg[0],0])
                    continue
                ## if box wire is horizontal else vertical
                if abs(min_edg[0][0]-min_edg[1][0]) > abs(min_edg[0][1]-min_edg[1][1]):
                    angle = 270
                    ## replace point with smallest x as first point
                    if min_edg[1][0] < min_edg[0][0]:
                        temp_edg   = [min_edg[0][0],min_edg[0][1],minIdx[0],minIdx[2]]
                        min_edg[0] = min_edg[1]
                        min_edg[1] = [temp_edg[0],temp_edg[1]]
                        minIdx[0]  = minIdx[1]
                        minIdx[2]  = minIdx[3]
                        minIdx[1]  = temp_edg[2]
                        minIdx[3]  = temp_edg[3]

                    ## make distance between point suitable for ltspice
                    if (idx == 1) or (idx == 3):    ## if box is diode or capacitor
                        min_edg[0][0] = min_edg[0][0] - 16
                        min_edg[1][0] = min_edg[0][0] + 64
                        min_edg[1][1] = min_edg[0][1]
                    elif (idx == 0) or (idx == 4) or (idx == 5):  ## if box is res, v_source, ind
                        min_edg[0][0] = min_edg[0][0] - 20
                        min_edg[1][0] = min_edg[0][0] + 80
                        min_edg[1][1] = min_edg[0][1]

                else:
                    angle = 0
                    ## replace point with smallest y as first point
                    if min_edg[1][1] < min_edg[0][1]:
                        temp_edg   = [min_edg[0][0],min_edg[0][1],minIdx[0],minIdx[2]]
                        min_edg[0] = min_edg[1]
                        min_edg[1] = [temp_edg[0],temp_edg[1]]
                        minIdx[0]  = minIdx[1]
                        minIdx[2]  = minIdx[3]
                        minIdx[1]  = temp_edg[2]
                        minIdx[3]  = temp_edg[3]

                    ## make distance between point suitable for ltspice
                    if (idx == 1) or (idx == 3):    ## if box is diode or capacitor
                        min_edg[1][0] = min_edg[0][0]
                        min_edg[0][1] = min_edg[0][1] - 16
                        min_edg[1][1] = min_edg[0][1] + 64
                    elif (idx == 0) or (idx == 4) or (idx == 5):  ## if box is res, v_source, ind
                        min_edg[1][0] = min_edg[0][0]
                        min_edg[0][1] = min_edg[0][1] - 20
                        min_edg[1][1] = min_edg[0][1] + 80

                ## (box_id,type_id,node1_id,node2_id,(x,y) of node1 end, (x,y) of node2 end,angle)
                comp_ends.append([i,idx,minIdx[0],minIdx[1],min_edg[0],min_edg[1],angle])
                i = i+1

            tempnodes = []
            for  (box_id,type_id,n1_id,n2_id,(x1,y1),(x2,y2),_) in comp_ends:
                tempnodes.append([n1_id,[x1,y1]])
                tempnodes.append([n2_id,[x2,y2]])

            node_ends = deepcopy(tempnodes)

            ## find node wires and dominant wire of all nodes
            wires = []
            refs  = []
            for (i,c) in node_cnts:
                node_mask = np.zeros(th.shape,np.uint8)
                cv2.drawContours(node_mask,[c]  , 0, (255,255,255), 3)
                temp_lines = lsd(node_mask)
                tv_lines  =  remove_parallel_lines(temp_lines,2)
                th_lines  =  remove_parallel_lines(temp_lines,1)
                all_lines =  tv_lines + th_lines
                big = 0
                j = -1
                for (x1,y1,x2,y2,_),k in zip(all_lines,xrange(len(all_lines))):
                    dist = np.sqrt((x2-x1)**2+(y2-y1)**2)
                    if dist> big:
                        big = dist
                        j = k

                ## adjust ref according to nodes
                ref = np.array([[all_lines[j][0],all_lines[j][1]],[all_lines[j][2],all_lines[j][3]]])
                nodes = []
                for (j,(xe,ye)) in node_ends:
                    if j == i:
                        nodes.append([xe,ye])

                if len(nodes)>0:
                    nodes = np.array(nodes)
                    ## if ref wire is horizontal
                    if abs(ref[0][0]-ref[1][0]) > abs(ref[0][1]-ref[1][1]):
                        nodes = nodes[nodes[:,0].argsort()]
                        ref = ref[ref[:,0].argsort()]
                        ref[0][0] = nodes[0][0]
                        ref[1][0] = nodes[-1][0]

                        dist1 = np.sqrt((ref[0][1]-nodes[0][1])**2)
                        dist2 = np.sqrt((ref[1][1]-nodes[-1][1])**2)
                        if dist1<10:
                            ref[0][1] = nodes[0][1]
                            ref[1][1] = nodes[0][1]
                        elif dist2<10:
                            ref[0][1] = nodes[-1][1]
                            ref[1][1] = nodes[-1][1]
                        else:
                            ref[0][1] = ref[1][1]

                    else:
                        nodes = nodes[nodes[:,1].argsort()]
                        ref = ref[ref[:,1].argsort()]
                        ref[0][1] = nodes[0][1]
                        ref[1][1] = nodes[-1][1]

                        dist1 = np.sqrt((ref[0][0]-nodes[0][0])**2)
                        dist2 = np.sqrt((ref[1][0]-nodes[-1][0])**2)
                        if dist1<10:
                            ref[0][0] = nodes[0][0]
                            ref[1][0] = nodes[0][0]
                        elif dist2<10:
                            ref[0][0] = nodes[-1][0]
                            ref[1][0] = nodes[-1][0]
                        else:
                            ref[0][0] = ref[1][0]

                refs.append([ref[0][0],ref[0][1],ref[1][0],ref[1][1],1])

            ## optimize reference components
            for (box_id,type_id,n1_id,n2_id,(x1,y1),(x2,y2),_) in comp_ends:

                ## if ref wire is horizontal else vertical
                if abs(refs[n1_id][0]-refs[n1_id][2]) > abs(refs[n1_id][1]-refs[n1_id][3]):
                    x = x1
                    y = refs[n1_id][1]
                else:
                    x = refs[n1_id][0]
                    y = y1

                wires.append([x1,y1,x,y,1])
                ## if ref wire is horizontal else vertical
                if abs(refs[n2_id][0]-refs[n2_id][2]) > abs(refs[n2_id][1]-refs[n2_id][3]):
                    x = x2
                    y = refs[n2_id][1]
                else:
                    x = refs[n2_id][0]
                    y = y2

                wires.append([x2,y2,x,y,1])

            wires = wires + refs
            flagx = 1

        draw_result_boxes(src,boxes)
        cv2.imshow("recognizer", src)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or flagx ==1:
            break

    while (process_stage <3):
        cv2.imshow("recognizer", src)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cv2.destroyAllWindows()
