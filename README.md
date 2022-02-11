# Canny-Edge-Detector
The Canny’s Edge Detector consists of four steps: Gaussian smoothing, gradient operation, non-maxima suppression and thresholding.

The input to the program is a grayscale image of size 𝑁𝑁 × 𝑀𝑀 (rows × cols.) 
Using the 7 × 7 Gaussian mask below for smoothing the input image with the center of the mask as the reference center. If part of the Gaussian mask goes outside of the image
border, the output image is undefined at the location of the reference center. 


<img src="https://user-images.githubusercontent.com/55443909/153614974-fdc80d31-bb6b-498e-ad99-06bf8ce968f9.png" width="300">

After performing convolution (or cross-correlation), normalization was performed by dividing the results by the sum of the entries (= 140 for the given mask) at each pixel location. Instead of using the Robert’s operator, the Prewitt’s operator was used to compute horizontal and vertical gradients. If part of the 3 × 3 mask of the operator goes
outside of the image border or lies in the undefined region of the image after Gaussian filtering, the output value is undefined. 


<img src="https://user-images.githubusercontent.com/55443909/153617591-09955830-a144-4aa3-bce3-c3175b5b95f0.png" width="300">


The third step is nonmaxima suppression. At locations with undefined gradient values and when the center pixel has a neighbor with undefined gradient value, the output is kept zero (i.e., no edge.) 

For the fourth step, using simple thresholding, three binary edge maps were produced by using three thresholds chosen at the 25th, 50th and 75th percentiles of the gradient magnitudes after non-maxima suppression (excluding pixels with zero gradient magnitude when determining the percentiles.)

Test Image:

![image](https://user-images.githubusercontent.com/55443909/153620027-798216e9-cdb5-4e5a-b196-5b1e6b5aea43.png)

Output images:

![image](https://user-images.githubusercontent.com/55443909/153619822-b1782db3-0587-4442-b37a-6bea4ea54396.png)

![image](https://user-images.githubusercontent.com/55443909/153619619-a8b3ee28-863b-4d7d-8991-fec41896346e.png)

![image](https://user-images.githubusercontent.com/55443909/153619657-76f15b06-7064-47f7-afb9-fe506432637e.png)

![image](https://user-images.githubusercontent.com/55443909/153619715-918f31b6-8ec2-436d-8ad1-553e47899959.png)

