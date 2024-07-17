import cv2
import lib.pdfimagetextconversion as pdfimagetextconversion
import numpy

def getavgdata(img,outputpoint,wpath,avgtonerecttablepath,iavgtonerecttablepath,igavgtonerecttablepath,ciavgtonerecttablepath):
    data=None
    # img = cv2.imread("org.jpg")
    # print("getavgdata===start")
    crop_img = img[711:762,740:980]
    cv2.imwrite(avgtonerecttablepath, crop_img)
    img = cv2.imread(avgtonerecttablepath)
    grayimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
    thresholdcropped_image= cv2.threshold(grayimage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # cv2.imwrite(iavgtonerecttablepath, thresholdcropped_image)
    
    invertcropped_image = cv2.bitwise_not(thresholdcropped_image)
    cv2.imwrite(iavgtonerecttablepath, invertcropped_image)

    invertimgrectblack = cv2.imread(iavgtonerecttablepath)
    ignvertcropped_image = cv2.bitwise_not(grayimage)

    cv2.imwrite(igavgtonerecttablepath, ignvertcropped_image)
    # print("igavgtonerecttablepath=",igavgtonerecttablepath)
    igninvertimgrectblack = cv2.imread(igavgtonerecttablepath)
    idilatecropped_image = cv2.dilate(invertcropped_image, None, iterations=5)
    # cv2.imwrite(ciavgtonerecttablepath, idilatecropped_image)
    contours,hierarchy = cv2.findContours(idilatecropped_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contoursimage=cv2.drawContours(grayimage.copy(),contours, -1, (0, 255, 0), 3)
    cv2.imwrite(ciavgtonerecttablepath, contoursimage)

    acrx=0
    acry=0
    acrw=0
    acrh=0
    count=0
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        # print("area=",area)
        x, y, w, h = cv2.boundingRect(contour) 
        cropped_image = img[y:y+h, x:x+w]
        data=str(pdfimagetextconversion.convert_image_to_text(cropped_image)).strip()
        
        if area> 2000:
            continue
        if "AC" in data:       
            acrx=x
            acry=y
            acrw=w
            acrh=h
            # print("data111231=",data)
    grayimage1 = cv2.cvtColor(igninvertimgrectblack, cv2.COLOR_BGR2GRAY)   
    grayimage2 = cv2.cvtColor(invertimgrectblack, cv2.COLOR_BGR2GRAY) 
    outputpoint= get4avgpoint(grayimage1,grayimage2,wpath,acrx,acry,acrw,acrh,outputpoint) 
    return outputpoint
        


def get4avgpoint(grayimage1,grayimage2,wpath,acrx,acry,acrw,acrh,outputpoint):
    # avg_ AC R
    acrrectx=acrx+52
    acrrecty=acry
    acrrectw=acrrectx + acrw+26
    acrrecth=acry + acrh+3

    outputpoint[0][0] =d0=pdfimagetextconversion.getexactavgpoint("avg","ac_R",grayimage1.copy(),grayimage2.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth,True)
    # print("d0000=====",d0)

    # avg_ AC L
    acrrectx=acrx+148
    acrrecty=acry-4
    acrrectw=acrrectx + acrw+35
    acrrecth=acry + acrh+4

    outputpoint[0][1]=d1=pdfimagetextconversion.getexactavgpoint("avg","ac_L",grayimage1.copy(),grayimage2.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth,True)
    # print("d11=====",d1)

    # avg_ BC L
    acrrectx=acrx+52
    acrrecty=acry+19
    acrrectw=acrrectx + acrw+35
    acrrecth=acry + acrh+3+22

    outputpoint[0][2]= d2=pdfimagetextconversion.getexactavgpoint("avg","bc_R",grayimage1.copy(),grayimage2.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth,True)
    # print("d2=====",d2)


    # avg_ BC L
    acrrectx=acrx+148
    acrrecty=acry+19
    acrrectw=acrrectx + acrw+35
    acrrecth=acry + acrh+3+22

    outputpoint[0][3]= d3=pdfimagetextconversion.getexactavgpoint("avg","bc_L",grayimage1.copy(),grayimage2.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth,True)
    # print("d3=====",d3)







    # myconfig="--psm 11 --oem 3"
    # result1=str(pdfimagetextconversion.convert_image_to_number(igninvertimgrectblack).strip()).strip()
    # if len(result1)>1:
    #     data=result1.replace("\n"," ")
    #     print("data0=",data)
    #     data=data.split(" ")
    #     if len(data)==4:
    #         if(data[0].isnumeric()):
    #           output[8][0]=float(data[0])
    #         if(data[1].isnumeric()):  
    #             output[8][1]=float(data[1])
    #         if(data[2].isnumeric() ):     
    #             output[8][2]=float(data[2])
    #         if(data[3].isnumeric()): 
    #             output[8][3]=float(data[3])


    # data1=numpy.arrayas(data)
    # if len(data1)==4:
    #     result=pdfimagetextconversion.getDigitonly(data[0])



    # print("data=")
    return outputpoint



