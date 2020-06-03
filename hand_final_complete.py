import cv2 as cv
import numpy as np
import sys
import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 0

spi2 = spidev.SpiDev()
spi2.open(1,1)
spi2.max_speed_hz = 1000000
spi2.mode = 0

#Performs required image processing to get ball coordinated in the video
class ProcessImage:

    def DetectObject(self):

        vid = cv.VideoCapture(0)

        if(vid.isOpened() == False):
            print('Cannot open input video')
            return

        while(vid.isOpened()):
            rc, frame = vid.read()
            frame1 = frame.copy()

            if(rc == True):
  
                [refX, refY] = self.contourArea(frame,frame1)
                rotationAngle = self.rotationFunction(frame, frame1, 3, 115, 87, 15, 192, 140)
                self.rotationSendSPI(rotationAngle)

                frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

                [pinkyX, pinkyY] = self.DetectObject(frame_HSV, 153, 76, 0, 167, 246, 255)
                pinkyDist = self.CalculateDistance(pinkyX,pinkyY,refX,refY)
                self.pinkySendSPI(pinkyDist)
                
                
                [ringX, ringY] = self.DetectObject(frame_HSV, 62, 20, 78, 93, 116, 147)
                ringDist = self.CalculateDistance(ringX,ringY,refX,refY)
                self.ringSendSPI(ringDist)

                
                [middleX, middleY] = self.DetectObject(frame_HSV, 172, 137, 89, 180, 197, 186)
                middleDist = self.CalculateDistance(middleX,middleY,refX,refY)
                self.middleSendSPI(middleDist)
                

                [indexX, indexY] = self.DetectObject(frame_HSV, 88, 102, 61, 122, 165, 160)
                indexDist = self.CalculateDistance(indexX,indexY,refX,refY)
                self.indexSendSPI(indexDist)
                

                [thumbX, thumbY] = self.DetectObject(frame, 10, 68, 175, 24, 154, 213)
                thumbDist = self.CalculateDistance(thumbX,thumbY,refX,refY)
                self.thumbSendSPI(thumbDist)
                
                
                #Pinky Actual
                cv.circle(frame1, (int(pinkyX), int(pinkyY)), 2, [0,0,255], 2, 8)
                cv.putText(frame1, "Pinky", (int(pinkyX + 50), int(pinkyY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                

                #Ring Actual  
                cv.circle(frame1, (int(ringX), int(ringY)), 2, [0,0,255], 2, 8)
                #cv.line(frame1,(int(ringX), int(ringY + 20)), (int(ringX + 50), int(ringY + 20)), [100,100,255], 2,8)
                cv.putText(frame1, "Ring", (int(ringX + 50), int(ringY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
    

                #Middle Actual
                cv.circle(frame1, (int(middleX), int(middleY)), 2, [0,0,255], 2, 8)
                cv.putText(frame1, "Middle", (int(middleX + 50), int(middleY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                

                #Index Actual
                cv.circle(frame1, (int(indexX), int(indexY)), 2, [0,0,255], 2, 8)
                cv.putText(frame1, "Index", (int(indexX + 50), int(indexY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                

                #Thumb Actual
                cv.circle(frame1, (int(thumbX), int(thumbY)), 2, [0,0,255], 2, 8)
                cv.putText(frame1, "Thumb", (int(thumbX + 50), int(thumbY + 20)), cv.FONT_HERSHEY_SIMPLEX,0.5, [50,200,250])
                
                cv.imshow('Input', frame1)

                if (cv.waitKey(1) & 0xFF == ord('q')):
                    break

            else:
                break

        vid.release()
        cv.destroyAllWindows()

    # Segment the green ball in a given frame
    def DetectObject(self, frame_HSV, loH, loS, loV, hiH, hiS, hiV):

        #Apply mask
        greenMask = cv.inRange(frame_HSV,(loH, loS, loV),(hiH, hiS, hiV)) #This is the line being tested
        
        # Dilate
        kernel = np.ones((5, 5), np.uint8)
        greenMaskDilated = cv.dilate(greenMask, kernel)

        # Find object as it is the biggest blob in the frame
        [nLabels, labels, stats, centroids] = cv.connectedComponentsWithStats(greenMaskDilated, 8, cv.CV_32S)

        # First biggest contour is image border always, Remove it
        stats = np.delete(stats, (0), axis = 0)
        try:
            maxBlobIdx_i, maxBlobIdx_j = np.unravel_index(stats.argmax(), stats.shape)

        # This is our ball coords that needs to be tracked
            objX = stats[maxBlobIdx_i, 0] + (stats[maxBlobIdx_i, 2]/2)
            objY = stats[maxBlobIdx_i, 1] + (stats[maxBlobIdx_i, 3]/2)
            return [objX, objY]
        except:
               pass

        return [0,0]

    def CalculateDistance(self, fingerX,fingerY, referenceX,referenceY):
        dist = np.sqrt(np.square(fingerX-referenceX) + np.square(fingerY-referenceY))
        return dist
    
    def pinkySendSPI(self,dist):
        if(dist<40):
            spi.xfer2([0])
            #print("Pinky 0")
            time.sleep(0.01)
        elif((dist>=40) & (dist<100)):
            y = np.interp(dist, (40, 100), (0, 31))
            y = int(y)
            #print("Pinky ",y)
            spi.xfer2([y])
            time.sleep(0.01)
        else:
            #print("Pinky 31")
            spi.xfer2([31])
            time.sleep(0.01)
            
    def middleSendSPI(self,dist):
        if(dist<40):
            spi2.xfer2([64])
            time.sleep(0.01)
            #print("Middle 64")
        elif((dist>=40) & (dist<120)):
            y = np.interp(dist, (40, 120), (0, 31))
            y = int(y)
            y = y + 64
            #print("Index ",y)
            spi2.xfer2([y])
            time.sleep(0.01)
        else:
            #print("Middle 95")
            spi2.xfer2([95])
            time.sleep(0.01)
            
    def indexSendSPI(self,dist):
        if(dist<50):
            spi2.xfer2([128])
            time.sleep(0.01)
            #print("Index 128")
        elif((dist>=50) & (dist<110)):
            y = np.interp(dist, (50, 110), (0, 31))
            y = int(y)
            y = y + 128
            #print("Index ",y)
            spi2.xfer2([y])
            time.sleep(0.01)
        else:
            #print("Index 159")
            spi2.xfer2([159])
            time.sleep(0.01)
                
    def ringSendSPI(self,dist):
        if(dist<40):
            spi.xfer2([32])
            time.sleep(0.01)
            #print("Ring 32")
        elif((dist>=40) & (dist<105)):
            y = np.interp(dist, (40, 105), (0, 31))
            y = int(y)
            y = y + 32
            #print("Ring ",y)
            spi.xfer2([y])
            time.sleep(0.01)
        else:
            #print("Ring 63")
            spi.xfer2([63])
            time.sleep(0.01)

            
    def thumbSendSPI(self,dist):
        if(dist<30):
            spi2.xfer2([224])
            time.sleep(0.01)
            #print("Thumb 255")
        elif((dist>=30) & (dist<85)):
            y = np.interp(dist, (30, 85), (0, 31))
            y = int(y)
            y = y + 224
            #print("Thumb  ",y)
            spi2.xfer2([y])
            time.sleep(0.01)
        else:
            #print("Thumb 224")
            spi2.xfer2([255])
            time.sleep(0.01)
            
    def rotationSendSPI(self, rotationAngle):  
        ID = 96
        spi.xfer2([ID + rotationAngle])
        #time.sleep(0.01)
    
        
    def contourArea(self, img, img2):
        
        grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        value = (31, 31)
        blurred = cv.GaussianBlur(grey, value, 0)
        retVal,thresh = cv.threshold(blurred,60,255,cv.THRESH_BINARY_INV)
        
        contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        highestY = -100000
        highMostContour = 0
        
        if len(contours)!=0:
            
            for contour in contours:
                #cv.drawContours(img2, contour, -1, (255, 255, 255), 3)
                (x,y),radius = cv.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = int(radius)
                
                #print("Y of contour: ", int(y))
                
                if int(y) > highestY:
                    highestY = int(y)
                    highMostContour = contour
            
            if len(highMostContour) != 0:
    #             handContour = contours[index] 
                cv.drawContours(img2, highMostContour, -1, (255, 255, 255), 3) 
                handContour = highMostContour
                hullHandContour = cv.convexHull(handContour, returnPoints = False)
                handMoments = cv.moments(handContour)
                if handMoments["m00"] != 0:
                    handXCenterMoment = int(handMoments["m10"]/handMoments["m00"])
                    handYCenterMoment = int(handMoments["m01"]/handMoments["m00"])
                
                    
                    centroidX = handXCenterMoment
                    centroidY = handYCenterMoment + 10 
                    
                    #cv.circle(img2, (centroidX, centroidY), 3, (255, 255, 255), -2)
                    
                    palmRadius = cv.pointPolygonTest(handContour,(centroidX,handYCenterMoment), True)
                    print("palmRadius: ",palmRadius)
                    
                    if palmRadius > 0:
                        cv.circle(img2, (handXCenterMoment, handYCenterMoment), int(palmRadius), (255, 255, 255), 2)
                    
                    #print("Palm radius ",palmRadius)
                    hullPoints = []
                    for i in hullHandContour:
                        hullPoints.append(handContour[i[0]])
                    hullPoints = np.array(hullPoints, dtype = np.int32)
                    #cv.drawContours(img2, [hullPoints], 0, (0, 0, 255), 2)
                    return [centroidX, centroidY]
            
                else:
                    return [0,0]
            else:
                return [0,0]
        else:
            return [0,0]
        
    def rotationFunction(self, img, img2, loH, loS, loV, hiH, hiS, hiV):
        
        frame_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        rectMask = cv.inRange(frame_HSV,(loH, loS, loV),(hiH, hiS, hiV)) #This is the line being tested
        
        # Dilate
        kernel = np.ones((5, 5), np.uint8)
        rectMaskDilated = cv.dilate(rectMask, kernel)
        
        contours, hierarchy = cv.findContours(rectMaskDilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        maxArea, index = 0, 0
        rotationAngle = 1
        
        if len(contours)!=0:
            
        
            for i in range(len(contours)):
                area = cv.contourArea(contours[i])
                if area > maxArea:
                    maxArea = area
                    index = i
                else:
                    index = 255
            
            
            if index != 255:
                
                rectContour = contours[index]
                cv.drawContours(img2, rectContour, -1, (0, 255, 255), 3)
                #print("area of rect: ", maxArea)
                
                if maxArea >= 1100:
                    rotationAngle = 1
                    
                    
                elif maxArea >= 700 and maxArea < 1100:
                    rotationAngle = 10
                    
                    
                elif maxArea >= 300 and maxArea < 700:
                    rotationAngle = 20
                
                elif maxArea < 300:
                    rotationAngle = 30                    
                
                else:
                    rotationAngle = 1                       
                
                return rotationAngle
            
                
            else:
                return rotationAngle
        
        else:
            return rotationAngle
        

#Main Function
def main():

    processImg = ProcessImage()
    processImg.DetectObject()


if __name__ == "__main__":
    main()

