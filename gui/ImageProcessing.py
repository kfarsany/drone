from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import cv2 as cv
from math import sqrt


'''Input image is a string that gives the location of the image'''
def process_image(im):

##    image = Image.open('images/prescored.png')
##    image.filter(ImageFilter.EDGE_ENHANCE_MORE).save('images/prescored.png')
##    image.close()
    
    # Read image and do some pre-processing (blur and grayscale
    ##im = cv.imread(image)
    im = cv.medianBlur(im,5)
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    # This part will certainly change depending on
    # what type of pictures we're testing.
    # This iteration only runs ~20 times and stops when
    # exactly two circles are found.
    for test in range(25, 45):
        detected_circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20,
                                           param1 = 300, param2 = test,
                                           minRadius = 1, maxRadius = 100)
        try:
            if len(detected_circles[0]) == 2:
                break
        except TypeError:
            pass

    #This only executes if exactly 2 circles were found
    try:
        if len(detected_circles[0]) == 2: 
          
            detected_circles = np.uint16(np.around(detected_circles))

            #Draw circle 1
            a1, b1, r1 = detected_circles[0,0,0], \
                         detected_circles[0,0,1], \
                         detected_circles[0,0,2] 
            cv.circle(im, (a1, b1), r1, (0, 0, 255), 2)

            #Draw circle 2
            a2, b2, r2 = detected_circles[0,1,0], \
                         detected_circles[0,1,1], \
                         detected_circles[0,1,2] 
            cv.circle(im, (a2, b2), r2, (0, 0, 255), 2)

            #Draw line between the circles
            cv.line(im, (a1,b1), (a2,b2), (0,255,0), 2)

            #Save image to any directory desired
            ##cv.imwrite('images/scored.png', im)

            #This section calculates and returns the score
            dist = sqrt((int(a1)-int(a2))**2 + (int(b1)-int(b2))**2)
            larger_radius = max(r1,r2)
            score = larger_radius - dist
            
            if score < 0:
                return 0
            
            score = 10 * (score/larger_radius)
            if score > 10:
                return 10
            return score
        
        else:
            ##cv.imwrite('images/scored.png', im)
            return "ERROR"
    except TypeError:
        pass

def text_image(score):

    score = str(score)
    
    image = Image.open('images/scored.png')

    width, height = image.size

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('fonts/Gilberto.ttf', size=100)

    color = 'rgb(0, 0, 0)'

    (x, y) = (width * .5 , height * .7)
    
    message = "Score: " + score
    draw.text((x, y), message, fill=color, font=font)
    image.save('images/scored.png')

if __name__ == '__main__':
    text_image(process_image('test_images/image0.jpeg'))
