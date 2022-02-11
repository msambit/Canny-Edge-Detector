import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

# Loading Images from gdrive
from google.colab import drive
drive.mount('/content/drive')

# Reading Images from gdrive
img1=cv2.imread('/content/drive/MyDrive/CED/House.bmp',cv2.COLOR_BGR2GRAY)
img2=cv2.imread(r"/content/drive/MyDrive/CED/Test patterns.bmp", cv2.COLOR_BGR2GRAY)

def gradient_smoothing(img):

    # Setting NxM matrix Output to 0
    smoothed_img = np.zeros(img.shape)
    size = img.shape

    # kernel for smoothing
    kernel = np.array([[1,1,2,2,2,1,1],[1,2,2,4,2,2,1],[2,2,4,8,4,2,2],[2,4,8,16,8,4,2],[2,2,4,8,4,2,2],[1,2,2,4,2,2,1],[1,1,2,2,2,1,1]])

    # Performing Smoothing Operation
    for i in range(3, size[0] - 3):
        for j in range(3, size[1] - 3):
            smoothed_img[i, j] = np.sum(np.multiply(img[i - 3 : i + 4, j - 3 : j + 4], kernel))
    
    # Perform Normalization
    smoothed_img = smoothed_img / 140

    return smoothed_img

def gradient(img):

    # Setting NxM matrices of Gradient Magnitude, Horizontal and Vertical Gradient to 0
    grad_mag = np.zeros(img.shape)
    Gx = np.zeros(img.shape)
    Gy = np.zeros(img.shape)

    size = img.shape

    # Prewitt's Operator
    kernelx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])

    # Calculating Horizontal and Vertical Gradients for all pixel values
    for i in range(1, size[0] - 1):
        for j in range(1, size[1] - 1):
            Gx[i, j] = np.sum(np.multiply(img[i - 1 : i + 2, j - 1 : j + 2], kernelx))
            Gy[i, j] = np.sum(np.multiply(img[i - 1 : i + 2, j - 1 : j + 2], kernely))

    #Calculating gradient magnitude
    grad_mag=np.absolute(Gx)+np.absolute(Gy)

    #Calculating gradient angles
    angles = np.rad2deg(np.arctan2(Gy, Gx))
    theta= np.arctan2(Gy, Gx)
    thetaQ=(np.round(theta*(5.0/np.pi))+5)%5
    #angles[angles < 0] += 180
    #grad_mag = grad_mag.astype('uint8')

    return Gx, Gy, grad_mag, thetaQ

def non_ms(img,angles):

    size = img.shape

    # Setting NxM matrix Output to 0
    nms = np.zeros(size)

    # Perform Non-Maxima Suppression based on gradient direction
    for i in range(1, size[0] - 1):
        for j in range(1, size[1] - 1):

            if (0 <= angles[i, j] < 22.5) or (157.5 <= angles[i, j] <= 180): # W-E (horizontal)
                value_to_compare = max(img[i, j - 1], img[i, j + 1])
            elif (22.5 <= angles[i, j] < 67.5): # SW-NE
                value_to_compare = max(img[i + 1, j - 1], img[i - 1, j + 1])
            elif (67.5 <= angles[i, j] < 112.5): # N-S (vertical)
                value_to_compare = max(img[i - 1, j], img[i + 1, j])
            else: # NW-SE (vertical) 
                value_to_compare = max(img[i - 1, j - 1], img[i + 1, j + 1])
            
            if img[i, j] > value_to_compare:
                nms[i, j] = img[i, j]
            else:
                nms[i,j]=0
    return nms

def produceBinaryEdgeMaps(grad):

    # Removing zeros from gradient array
    grad_no_zeros = grad[grad != 0]

    # Thresholds based on 25th, 50th and 75th percentile
    T1 = np.percentile(grad_no_zeros, 25)
    T2 = np.percentile(grad_no_zeros, 50)
    T3 = np.percentile(grad_no_zeros, 75)

    bmapT1 = grad.copy()
    bmapT2 = grad.copy()
    bmapT3 = grad.copy()

    size = grad.shape

    # Binary Edge Maps based on Thresholds
    for i in range(0, size[0]):
        for j in range(0, size[1]):
          if ( bmapT1[i, j] < T1 ):
              bmapT1[i, j] = 0
          else:
              bmapT1[i, j] = 255
          if ( bmapT2[i, j] < T2 ):
              bmapT2[i, j] = 0
          else:
              bmapT2[i, j] = 255
          if ( bmapT3[i, j] < T3 ):
              bmapT3[i, j] = 0
          else:
              bmapT3[i, j] = 255
        
    return bmapT1, bmapT2, bmapT3

if __name__ == '__main__':

  # Gaussian Smoothing - Change Image based on input - img1 or img2
  smoothed_img = gradient_smoothing(img1)
  
  # Gradient Calculation
  Gx, Gy, grad, angles=gradient(smoothed_img)
  
  # Non-maxima Suppression
  grad_afternms = non_ms(grad,angles)

  #Binary Edge Maps based on the three thresholds
  bmapT1, bmapT2, bmapT3 = produceBinaryEdgeMaps(grad_afternms.copy())

# Writing output images into gdrive
directory = r'/content/drive/MyDrive/CED/'
os.chdir(directory)
cv2.imwrite('Gaussian Blurring.bmp', smoothed_img)
cv2.imwrite('NormalizedGx.bmp', np.absolute(Gx) / 3.0)
cv2.imwrite('NormalizedGy.bmp', np.absolute(Gy) / 3.0)
cv2.imwrite('NormalizedGMag.bmp', (grad/grad.max())*255)
cv2.imwrite('NormalizedNMS.bmp', (grad_afternms/grad_afternms.max())*255)
cv2.imwrite('BEM25.bmp', bmapT1)
cv2.imwrite('BEM50.bmp', bmapT2)
cv2.imwrite('BEM75.bmp', bmapT3)