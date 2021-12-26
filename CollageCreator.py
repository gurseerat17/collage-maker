
import numpy as np
from skimage import io
from skimage import feature
from skimage.filters import *  
from skimage.color import *
from skimage.transform import resize
from matplotlib import pyplot as plt
import math

def CollageCreate(videoFramesAddress):

    heightImage = 400
    widthImage = 640
    images = []
    n_images = 6

    for i in range(1, n_images+1):
        image = io.imread(videoFramesAddress+'/frame_'+str(i)+'.png')
        images.append(resize(image, (heightImage, widthImage))) 
    
    sortedFrames = sortFrames(images, heightImage, widthImage)
    collage = makeCollage(sortedFrames, heightImage, widthImage)
    
    io.imsave("collage.png", (collage*255).astype(np.uint8), check_contrast=False)
    io.imshow(collage) 
    plt.axis('off')
    plt.show()

    return collage

def sortFrames (images, heightImage, widthImage):
    
    totalPixels = heightImage*widthImage
    frameValues = []

    print("Processing Input Images ...")

    for image in images:

        #edges
        edgeMap = feature.canny(rgb2gray(image),sigma = 1)
        
        edgePixels = 0
        for i in range(edgeMap.shape[0]):
            for j in range(edgeMap.shape[1]):
                if(edgeMap[i,j]):
                    edgePixels+=1
                    
        edgePixelFraction = edgePixels/totalPixels

        #brightness
        redPixels, bluePixels, greenPixels = 0, 0, 0

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                redPixels += image[i,j,0]
                bluePixels += image[i,j,1]
                greenPixels += image[i,j,2]

        red_mean, blue_mean, green_mean = redPixels/totalPixels, bluePixels/totalPixels, greenPixels/totalPixels
        brightness= (red_mean + blue_mean + green_mean)/3
        brightnessFraction = brightness/255

        #contrast/colour variation
        red_pixel_dev_square, blue_pixel_dev_square, green_pixel_dev_square = 0, 0, 0

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                red_pixel_dev_square += (image[i,j,0] - red_mean)**2
                blue_pixel_dev_square += (image[i,j,1] - blue_mean)**2
                green_pixel_dev_square += (image[i,j,2] - green_mean)**2

        red_std_dev = math.sqrt(red_pixel_dev_square/ totalPixels)
        blue_std_dev = math.sqrt(blue_pixel_dev_square/ totalPixels)
        green_std_dev = math.sqrt(green_pixel_dev_square/ totalPixels)

        contrast = (red_std_dev + blue_std_dev + green_std_dev)/3
        # max contrast : sqrt(N x (128)**2 / N) N: total pixels ; pixelIntensity-mean = 128 (pixelIntensity = 0 or 255)
        max_contrast = 128 
        contrastFraction = contrast/max_contrast

        frameInformationValue = (edgePixelFraction*100)*(brightnessFraction*100)*(contrastFraction*100)
        # print(frameInformationValue)

        frameValues.append({"Frame":image,"Value":frameInformationValue})

    frameValues.sort(reverse = True, key = lambda frameValue : frameValue['Value'] )
    # print(frameValues)
    return frameValues

def makeCollage(sortedFrames, heightImage, widthImage):

    print("Creating the collage ...")

    collage_small_height = heightImage
    collage_small_width = widthImage
    collage_large_height = collage_small_height*2 + 10 
    collage_large_width = int(collage_large_height*(collage_small_width/collage_small_height)) 

    sortedFrames[0]['Frame'] = resize(sortedFrames[0]['Frame'], (collage_large_height, collage_large_width))

    heightCollage = collage_large_height + collage_small_height + 20*3
    widthCollage = collage_large_width + collage_small_width + 20*3

    collage = np.zeros( [heightCollage, widthCollage,3])

    collage[21 : 21 + collage_large_height, 
            21 : 21 + collage_large_width] = sortedFrames[0]['Frame']

    nextStartWidth = 21 + collage_large_width
    collage[21 : 21 + collage_small_height, 
            nextStartWidth + 20 : nextStartWidth + 20 + collage_small_width] = sortedFrames[1]['Frame']
    
    nextStartHeight = 21 + collage_small_height
    collage[nextStartHeight + 20 : nextStartHeight + 20 + collage_small_height, 
            nextStartWidth + 20 : nextStartWidth + 20 + collage_small_width] = sortedFrames[2]['Frame']

    
    nextStartHeight = 21 + collage_large_height
    collage[nextStartHeight + 20 : nextStartHeight + 20 + collage_small_height, 
            nextStartWidth + 20 : nextStartWidth + 20 + collage_small_width] = sortedFrames[3]['Frame']
    
    nextStartWidth = nextStartWidth - 20 - collage_small_width
    collage[nextStartHeight + 20 : nextStartHeight + 20 + collage_small_height, 
            nextStartWidth + 20 : nextStartWidth + 20 + collage_small_width] = sortedFrames[4]['Frame']

    nextStartWidth = nextStartWidth - 20 - collage_small_width
    collage[nextStartHeight + 20 : nextStartHeight + 20 + collage_small_height, 
            nextStartWidth + 20 : nextStartWidth + 20 + collage_small_width] = sortedFrames[5]['Frame']

    return collage
    

if __name__ == '__main__':
    CollageCreate("frame_set1")