from pydicom import dcmread
from pydicom.data import get_testdata_files
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Read DCM
filename = '012_se_mc/012-001.dcm'
ds = dcmread(filename)

# Show DCM table of data
#print(ds)

# Echo time
print('Echo time: ', ds[0x18,0x81].value)

# Information of image
print('shape: ',ds.pixel_array.shape)
print('data type: ',ds.pixel_array.dtype)

# matplotlib to plot the DCM
plt.imshow(ds.pixel_array,cmap='gray')
plt.savefig("T2A.png")
plt.show()
ds = dcmread('012_se_mc/012-002.dcm')
plt.imshow(ds.pixel_array,cmap='gray')
plt.savefig("T2B.png")
plt.show()

# In the folder, there are two kinds of images.
imgA = np.zeros((256,256,12))
imgB = np.zeros((256,256,12))
echoTime = list()

for i in range(12):
    # Read the DCM
    if i < 5 :
        filenameA=('012_se_mc/012-00'+str(2*i+1)+'.dcm')
    else:
        filenameA=('012_se_mc/012-0'+str(2*i+1)+'.dcm')
    
    if i < 4 :
        filenameB=('012_se_mc/012-00'+str(2*i+2)+'.dcm')
    else:
        filenameB=('012_se_mc/012-0'+str(2*i+2)+'.dcm')
    
    # Save image of DCM
    imgA[:,:,i]=dcmread(filenameA).pixel_array
    imgB[:,:,i]=dcmread(filenameB).pixel_array
    print('File Name: ',filenameA,filenameB)
    # Save echo time of DMC
    echoTime.append(dcmread(filenameA)[0x18,0x81].value)
    print('Echo Time: ',dcmread(filenameA)[0x18,0x81].value, dcmread(filenameB)[0x18,0x81].value)
# T2-Mapping
T2mapA = np.zeros((256,256,2))
T2mapB = np.zeros((256,256,2))

def Mapping(img, echoTime, T2map,outputFile):
    for row in range(256):
        for colum in range(256):
            # if value of image < 270, to skip
            if img[row,colum,0] < 270: continue 
            coef=curve_fit(lambda t,a,b: a*np.exp(-t/b),  echoTime,  (img[row,colum,:]), p0=(img[row,colum,0],echoTime[5]))
            #coef = [M0, TE]
            T2map[row,colum,:] = coef[0]
            #print(TE)

    plt.imshow(T2map[:,:,1],cmap='gray')
    plt.savefig("images/"+outputFile)
    plt.show()

Mapping(imgA, echoTime, T2mapA, "T2A_Mapping.png")
Mapping(imgB, echoTime, T2mapB, "T2B_Mapping.png")

# Show the result by plot
def T2_plot(img, T2map, echoTime, pixel, outputFile):
    row = pixel[0]
    colum = pixel[1]
    plt.plot(echoTime, img[row,colum,:])
    plt.title("T2 Image in pixel"+str(pixel))
    plt.xlabel("TE") 
    plt.ylabel("M")
    plt.savefig("images/"+outputFile)
    plt.show()    
    

    T2 = [T2map[row,colum,0]*np.exp(-x/T2map[row,colum,1]) for x in echoTime]
    plt.plot(echoTime, img[row,colum,:])
    plt.plot(echoTime, T2)

    plt.title("T2 Image in pixel"+str(pixel))
    plt.xlabel("TE") 
    plt.ylabel("M")
    plt.legend(['Orignal','Curve fitting'])
    plt.savefig("images/curve-"+outputFile) 
    plt.show()

print("ImageA & T2mapA")
T2_plot(imgA, T2mapA, echoTime, [150,50], "imageA-150.50.png")
T2_plot(imgA, T2mapA, echoTime, [150,200], "imageA-150.200.png")

print("ImageB & T2mapB")
T2_plot(imgB, T2mapB, echoTime, [150,50], "imageB-150.50.png")
T2_plot(imgB, T2mapB, echoTime, [150,100], "imageB-150.100.png")
