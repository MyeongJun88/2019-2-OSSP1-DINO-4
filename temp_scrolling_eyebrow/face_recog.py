import sys
import os
import dlib
import glob
from skimage import io
import numpy as np
import cv2
from scipy.spatial import distance as dist #입술 사이 거리 계산 위해
import math
import pygame
from game import *

from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time

class face():
    def __init__(self,game):
        super().__init__()
        self.game=game

        self.cap = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #self.out = cv2.VideoWriter('output.avi',self.fourcc, 20.0, (1280, 720))
        self.predictor_path = 'shape_predictor_81_face_landmarks.dat'
        self.detector = dlib.get_frontal_face_detector() #INITIALIZE FACE PROTECTOR
        self.predictor = dlib.shape_predictor(self.predictor_path) #LANDMARK PREDICTOR

        self.ret,self.frame = self.cap.read() #영상 읽어들임
        self.frame = cv2.flip(self.frame, 1)
        self.dets = self.detector(self.frame, 0) #rects
        self.rects=self.detector(self.frame, 0) #rects
        (self.mStart,self.mEnd)=(48,54) #mouth의 시작점, 끝점 번호
        self.MOUTH_AR_THRESH = 0.1

        self.direction = 0 #눈썹 방향
        # grab the indexes of the facial landmarks for the left and
        # right eyebrows, respectively
        (self.lbStart, self.lbEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
        (self.rbStart, self.rbEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

        #Get the indexes of the nose line
        (self.nStart, self.nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]

        #Get the mid indexes of the facial landmarks
        self.lbMid = int((self.lbStart + self.lbEnd)/2)
        self.rbMid = int((self.rbStart +self.rbEnd)/2)
        self.nMid = int((self.nStart + self.nEnd)/2)

        # Define variables that will contain the euclidean distances
        self.rightEyebrowToNose = 0
        self.leftEyebrowToNose = 0

    def __call__(self):
        print (" ")

    def getDirection(self):
        return self.direction

    def defineDirection(self,direction):
        self.direction = direction

    def face_recognition(self,screen):
        self.ret,self.frame = self.cap.read() #영상 읽어들임
        self.frame = cv2.flip(self.frame, 1)
        #self.dets = self.detector(self.frame, 0) #rects

        for k, d in enumerate(self.dets):
            shape = self.predictor(self.frame, d)
            landmarks = np.matrix([[p.x, p.y] for p in shape.parts()])
            for num in range(shape.num_parts):
                cv2.circle(self.frame, (shape.parts()[num].x, shape.parts()[num].y), 3, (0,255,0), -1)
            A=dist.euclidean((shape.parts()[61].x,shape.parts()[61].y),(shape.parts()[67].x,shape.parts()[67].y))
            B=dist.euclidean((shape.parts()[63].x,shape.parts()[63].y),(shape.parts()[65].x,shape.parts()[65].y))
            C=dist.euclidean((shape.parts()[48].x,shape.parts()[48].y),(shape.parts()[54].x,shape.parts()[54].y))
            mar=(A+B)/(2.0*C)
            mar=round(mar,5)

            if mar>self.MOUTH_AR_THRESH:
                #cv2.putText(self.frame,"MOUTH IS OPEN!",(30,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                print("mouth is open")
                return True
            else:
                print("closed")
                return False

        #cv2.imshow("Frame", self.frame)
        self.cap.release()
        #self.out.release()
        cv2.destroyAllWindows()

    def distance(A, B):
        (ax,ay) = A
        (bx,by) = B
        return math.sqrt((ax-bx)**2 + (ay-by)**2)

    def eyebrowDetection(self,screen):
        global lbMid, rbMid, nMid, rightEyebrowToNose, leftEyebrowToNose, oldNosePosition, currentNosePosition
        for k, d in enumerate(self.dets):
            shape = self.predictor(self.frame, d)
            shape = face_utils.shape_to_np(shape)
            # Get the positions of the
            leftEyebrowCoordinates = shape[self.lbMid]
            rightEyebrowCoordinates = shape[self.rbMid]
            currentNosePosition = midPointNoseCoordinates = shape[self.nMid]
            midPointNoseCoordinates = shape[self.nMid]

            currentRightEyebrowDistance = dist.euclidean(rightEyebrowCoordinates,midPointNoseCoordinates)
            currentLeftEyebrowDistance =dist.euclidean(leftEyebrowCoordinates,midPointNoseCoordinates)

            if (self.rightEyebrowToNose == 0) or (self.leftEyebrowToNose == 0):
                self.rightEyebrowToNose =dist.euclidean(rightEyebrowCoordinates,midPointNoseCoordinates)
                self.leftEyebrowToNose = dist.euclidean(leftEyebrowCoordinates,midPointNoseCoordinates)
            elif (currentRightEyebrowDistance > self.rightEyebrowToNose) or (currentLeftEyebrowDistance >  self.leftEyebrowToNose):
                self.defineDirection(1)
                print ("[RESULT] UP")
                return True
            else:
                self.defineDirection(-1)
                print ("[RESULT] DOWN")
                return False

            # If the person moved(the nose postion moved), calculates the distance between it's old postion
            # and the new one. If it's bigger than '8' define the new standard positions
            # the smaller the number the more precise the algorithm gets
            #movementDistanceOfNose = distance(currentNosePosition , oldNosePosition)



            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            #for (x, y) in leftEyebrowCoordinates,rightEyebrowCoordinates,midPointNoseCoordinates:
            #    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

    		# show the frame
    		#cv2.imshow("Frame", frame)
    		#key = cv2.waitKey(1) & 0xFF

    		# if the `q` key was pressed, break from the loop
    		#if key == ord("q"):
    		#	closeDetectionWindows()
    		#	break
