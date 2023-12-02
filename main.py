import cv2 as cv
import numpy as np

class Line:
    def __init__(self) -> None:
        frameWidth = 640
        frameHeight = 480
        self.capture = cv.VideoCapture(r'Duburi_Task\resource\background.mp4')
        self.image = cv.imread(r'Duburi_Task\resource\black_L.jpg')
        self.capture.set(3, frameWidth)
        self.capture.set(4, frameHeight)
        self.slider() # For Adjusting the Threshold for canny edge detection


    def slider(self):
        def empty(a): pass 
        cv.namedWindow("Parameters")
        cv.resizeWindow('Parameters', 640, 100)
        cv.createTrackbar('Threshold1','Parameters', 150,250, empty )
        cv.createTrackbar('Threshold2','Parameters', 255,250, empty )
        cv.createTrackbar('Area','Parameters', 500,3000, empty )

    def getContour(self, img, imgContour):
        contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)   

        for cnt in contours:
            area = cv.contourArea(cnt)
            areaMin= cv.getTrackbarPos('Area', 'Parameters') # Area slider
            # areaMin = 10
            
            if area > areaMin:
                cv.drawContours(imgContour, cnt, -1, (255, 0, 255), 2)
                perl = cv.arcLength(cnt, True)
                approx = cv.approxPolyDP(cnt, 0.02*perl, True)
                if len(approx) <=20:
                    x, y, w, h = cv.boundingRect(approx)
                    # print(x,y)
                    if self.is_black_color((x+10,y+10)):
                        # print("True")
                        cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                        cv.putText(imgContour, f'Points: {len(approx)}', (x+w-20, y-20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)                    
    
    def is_black_color(self, coordinates):
        image = self.img
        if image is None:
            print("Error: Unable to load the image.")
            return False

        x, y = map(int, coordinates)

        if x >= 640: x = 640-4
        if y >= 480: y = 480-4

        pixel_color = image[y, x]

        hsv_color = cv.cvtColor(np.uint8([[pixel_color]]), cv.COLOR_BGR2HSV)

        lower_black = np.array([0, 0, 0])
        upper_black = np.array([10, 255, 30])

        is_black = cv.inRange(hsv_color, lower_black, upper_black).all()

        return is_black

    def getVideo(self):
        size = (640, 480) 
        result = cv.VideoWriter('output.avi', -1, 20.0, (640,480))
        while True:
            success, self.img = self.capture.read()
            if success == True:
                imgContour = self.img.copy()

                imgBlur = cv.GaussianBlur(self.img, (7,7), 1)
                imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

                threshold1 = cv.getTrackbarPos('Threshold1', 'Parameters') # Threshold1 Adjust Bar
                threshold2 = cv.getTrackbarPos('Threshold2', 'Parameters') # Threshold1 Adjust Bar

                imgCanny = cv.Canny(imgGray, threshold1, threshold2) 

                kernel = np.ones((5,5))
                imgDil = cv.dilate(imgCanny, kernel, iterations=1)

                self.getContour(imgDil, imgContour)

                imgStack = imgContour
                cv.imshow('Blur', imgStack)
                # cv.imshow('Canny', imgCanny)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        self.capture.release()
        result.release()
        cv.destroyAllWindows()

    def getImage(self):
            
            imgContour = self.image.copy()
            self.img = self.image
            self.imgBlur = cv.GaussianBlur(self.image, (7,7), 1)
            imgGray = cv.cvtColor(self.imgBlur, cv.COLOR_BGR2GRAY)

            imgCanny = cv.Canny(imgGray, 40, 0)

            kernel = np.ones((5,5))
            imgDil = cv.dilate(imgCanny, kernel, iterations=1)

            self.getContour(imgDil, imgContour)

            imgStack = imgContour 
            cv.imshow('Blur', imgStack)
            
            cv.waitKey(0)       
            
# x = Line().getImage()
x = Line().getVideo()