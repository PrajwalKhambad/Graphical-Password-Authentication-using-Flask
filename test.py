import cv2
import numpy as np
img=cv2.imread("static/images/test.jpg")
image=cv2.resize(img,(300,300))

# #For 2X2 Grid
# (h,w)=image.shape[:2]
# (cX,cY)=(w//2,h//2)
# topLeft = image[0:cY, 0:cX]
# topRight = image[0:cY, cX:w]
# bottomLeft = image[cY:h, 0:cX]                                                                                                  
# bottomRight = image[cY:h, cX:w]
# img_list=[topLeft,topRight,bottomLeft,bottomRight]
# # cv2.imshow("1",topLeft)
# # cv2.imshow("2",topRight)
# # cv2.imshow("3",bottomLeft)
# # cv2.imshow("4",bottomRight)
# # if(cv2.imwrite("data1.jpg",img_list[0])):
# #     print("Image saved")

#For 3X3 Grid
h,w=image.shape[:2]

p1=w//3
p2=2*w//3

p3=h//3
p4=2*h//3

img1=image[0:p1,0:p3]
img2=image[p1:p2,0:p3]
img3=image[p2:w,0:p3]

img4=image[0:p1,p3:p4]
img5=image[p1:p2,p3:p4]
img6=image[p2:w,p3:p4]

img7=image[0:p1,p4:h]
img8=image[p1:p2,p4:h]
img9=image[p2:w,p4:h]

img_concat_hori1=np.concatenate((img1,img4,img7),axis=1)
img_concat_hori2=np.concatenate((img2,img5,img8),axis=1)
img_concat_hori3=np.concatenate((img3,img6,img9),axis=1)
cv2.imshow('Horixontal concat:',img_concat_hori2)
# cv2.imshow('A',img8)
cv2.waitKey(0)