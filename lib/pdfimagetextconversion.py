from pytesseract import image_to_string
from pdf2image import convert_from_path
import cv2 


def convert_pdf_to_img(pdf_file):
    """
    @desc: this function converts a PDF into Image
    
    @params:
        - pdf_file: the file to be converted
    
    @returns:
        - an interable containing image format of all the pages of the PDF
    """
    return convert_from_path(pdf_file)
def convert_image_to_number(file,myconfig="--psm 11 --oem 3"):
    """
    @desc: this function extracts text from image
    
    @params:
        - file: the image file to extract the content
    
    @returns:
        - the textual content of single image
    """
    # img = cv2.imread("work/2.jpg")
    # myconfig=r"--psm 11 --oem 3"
    myconfig=r"--psm 12"
    # myconfig='--psm 10 --oem 3 -c tessedit_char_whitelist=abcr0123456789'
    text = image_to_string(file,lang='eng',config=myconfig)
    # text = image_to_string(file)

    return text

def convert_image_to_text(file,myconfig="--psm 11 --oem 3"):
    """
    @desc: this function extracts text from image
    
    @params:
        - file: the image file to extract the content
    
    @returns:
        - the textual content of single image
    """
    # img = cv2.imread("work/2.jpg")
    # myconfig=r"--psm 11 --oem 3"
    myconfig=r"--oem 3 --psm 6"
    # myconfig='--psm 10 --oem 3 -c tessedit_char_whitelist=abcr0123456789'
    text = image_to_string(file,lang='eng',config=myconfig)
    # text = image_to_string(file)

    return text

def get_text_from_any_pdf(pdf_file):
    """
    @desc: this function is our final system combining the previous functions
    
    @params:
        - file: the original PDF File
    
    @returns:
        - the textual content of ALL the pages
    """
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    i=0
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        # print(convert_image_to_text(img))
        i=i+1
  
    return final_text

def getDigitonly(data):
    data=data.strip()
    if data.isnumeric() or data=="" or len(data)==1: 
        # print("data.isnumeric()= ",data.isnumeric() )
        if data.isnumeric() !=True:
            return 0
        return data
    if len(data)==2:
        data1=data[0]
        if data1.isnumeric(): 
            return data1
    if len(data)>=3:
        data1=data[0]
        data2=data[1]
        data3=data[2]
        if data1.isnumeric() and  data2.isnumeric() and data3.isnumeric() : 
             return data1+""+data2+""+data3
        if data1.isnumeric() and  data2.isnumeric() : 
             return data1+""+data2
        if data1.isnumeric() : 
             return data1 
  
    return ""

def getpoint(frontname,positionname,orgimage,ouputimagepath,x,y,w,h,printfile):
    result=0

    # print(f"printstatus={print}")
    if printfile==True:
        box=cv2.rectangle(orgimage.copy(), (x, y), (w, h), (255,0,255), 2)
        cv2.imwrite(f"{ouputimagepath}\ {frontname}c_{positionname}.jpg", box)
    cropped_acrimage = orgimage[y:h, x:w]
    result1=convert_image_to_text(cropped_acrimage).strip()
    # print("result1====",result1)
    result=getDigitonly(result1)
    # print("result==",result)
    # if debug:
    #     print(f"==={frontname}c_{positionname}?{result1}=",result)
    if result =="":
        result=0
    return int(result)

def getavgpoint(frontname,positionname,orgimage,ouputimagepath,x,y,w,h,printfile,re_x=2,re_y=2):
    result=0

    # print(f"printstatus={print}")
   
    # box=cv2.rectangle(orgimage.copy(), (x, y), (w, h), (255,0,255), 2)
    # cv2.imwrite(f"{ouputimagepath}\ {frontname}c_{positionname}.jpg", box)
    cropped_acrimage = orgimage[y:h, x:w]
    # re_image = cv2.resize(cropped_acrimage, (0,0), fx=.9, fy=.7)
    re_image = cv2.resize(cropped_acrimage, (0,0), fx=re_x, fy=re_y)
    # import matplotlib.pyplot as plt
    # plt.imshow(re_image)
    # plt.show()
    # cv2.imwrite(f"re_{ouputimagepath}\ {frontname}c_{positionname}.jpg", re_image)
    result1=convert_image_to_number(re_image,myconfig="--psm 12").strip()
    # result1=convert_image_to_text(re_image).strip()
    # print("result1n====",result1)
    result=str(result1).strip()
    # print("result1n==isdecimal()==",is_float(result))   
    # is_float()
    # result=getDigitonly(result1)

    # if debug:
    #     print(f"==={frontname}c_{positionname}?{result1}=",result)
    if is_float(result)!=True or result =="":
        # print("result1n==isdecimal()111==",is_float(result))   
        result=0
    # print("result float==",result)
    return float(result)


def getexactpoint(frontname,positionname,orgimage,orgimage1,ouputimagepath,x,y,w,h,printfile=False):
    result=getpoint(frontname,positionname,orgimage,ouputimagepath,x,y,w,h,printfile)
    # print(f"{result}=result=",result)
    if result%5!=0 or result==0:
        # y=y+buffery-5
        # h=y +h-20+5
        result1=getpoint(frontname,positionname,orgimage1,ouputimagepath,x,y,w,h,printfile)
        # print(f"{result}=result=",result1)
        result=result1
    

    return result
def getexactavgpoint(frontname,positionname,orgimage,orgimage1,ouputimagepath,x,y,w,h,printfile=False):
    result=getavgpoint(frontname,positionname,orgimage,ouputimagepath,x,y,w,h,printfile)
    # print(f"{result}=result???/=",result)
    if result<10 or result>99:
        # y=y+buffery-5
        # h=y +h-20+5
        result1=getavgpoint(frontname,positionname,orgimage1,ouputimagepath,x,y,w,h,printfile)
        # print(f"{result}=result=",result1)
        if result1<10 or result1>99:
            result1=getavgpoint(frontname,positionname,orgimage1,ouputimagepath,x,y,w,h,printfile,.9,.7)
        result=result1
    

    return result
def getdata(frontname,positionname,orgimage,ouputimagepath,x,y,w,h):
    result=0
    # box=cv2.rectangle(orgimage.copy(), (x, y), (w, h), (0,0,255), 2)
    # cv2.imwrite(f"{ouputimagepath}\ {frontname}c_{positionname}.jpg", box)
    cropped_acrimage = orgimage[y:h, x:w]
    result=convert_image_to_text(cropped_acrimage).strip()
    # if debug:
    #  print(f"{frontname}c_{positionname}=",result)
    # result=getDigitonly(result)
    # print(f"==={frontname}c_{positionname}=",result)
    return result

def isidentify4rowstable(frontname,positionname,orgimage,ouputimagepath,x,y,w,h):
    result=False
  
    acrrectx=x
    acrrecty=y+23
    acrrectw=acrrectx + w
    acrrecth=acrrecty +h-20
    acrL_data=getdata("b","r",orgimage.copy(),ouputimagepath,acrrectx,acrrecty,acrrectw,acrrecth)
    # buffery=23
    # if debug:
    #     print("bc_L_data1===",acrL_data)
    if "ACR" in acrL_data:
        # buffery=46
        result=True
        # acrrectx=acrx
        # acrrecty=acry+buffery
        # acrrectw=acrrectx + acrw
        # acrrecth=acrrecty +acrh-20
        # acrL_data=pdfimagetextconversion.getdata("b","R",grayimage.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # if debug:
    #     print("bc_L_data2===",acrL_data)

    # print("isidentify4rowstable===",result)

    return result


def getdata_AC_BC_R_L_Thr_4row(grayimage,grayimage1,wpath,acrx,acry,acrw,acrh,outputpoint):
     # acrR 250 data
    acrrectx=acrx+190
    acrrecty=acry-5
    acrrectw=acrrectx + acrw-10
    acrrecth=acry + acrh-24
    # box250=cv2.rectangle(grayimage.copy(), (acrrectx, acrrecty), (acrrectw, acrrecth), (0,0,255), 2)
    # cv2.imwrite(f"{acr250path}", box250)
    # cropped_acrimage = grayimage[acrrecty:acrrecth, acrrectx:acrrectw]
    # acr_250=convert_image_to_text(cropped_acrimage).strip()
    # print("acr_250=",acr_250)
    outputpoint[0][0]=getexactpoint("a","R_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr=",outputpoint[0][0])

    # acrR 500 data
    acrrectx=acrx+235
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-20
    outputpoint[0][1]=getexactpoint("a","R_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # acrR 1k data
    acrrectx=acrx+323
    acrrecty=acry-1
    acrrectw=acrrectx + acrw+2
    acrrecth=acry + acrh-21
    outputpoint[0][2]=getexactpoint("a","R_1k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr1=",outputpoint[0][2])
    # acrR 2k data
    acrrectx=acrx+415
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24
    outputpoint[0][3]=getexactpoint("a","R_2k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)


    # acrR 4k data
    acrrectx=acrx+505
    acrrecty=acry-5
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24+6
    outputpoint[0][4]=getexactpoint("a","R_4k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr=",outputpoint[0][4])
    # acrR 8k data
    acrrectx=acrx+595
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24+2
    outputpoint[0][5]=getexactpoint("a","R_8k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr=",outputpoint[0][5])
    # acrL 250 data
    acrrectx=acrx+1120
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24
    outputpoint[1][0]=getexactpoint("a","L_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # acrL 500 data
    acrrectx=acrx+1165
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24
    outputpoint[1][1]=getexactpoint("a","L_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # acrL 1k data
    acrrectx=acrx+1255
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24
    outputpoint[1][2]=getexactpoint("a","L_1k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # acrL 2k data
    acrrectx=acrx+1345
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24+2
    outputpoint[1][3]=getexactpoint("a","L_2k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # acrL 4k data
    acrrectx=acrx+1435
    acrrecty=acry
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-24
    outputpoint[1][4]=getexactpoint("a","L_4k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # acrL 8k data
    acrrectx=acrx+1525
    acrrecty=acry-5
    acrrectw=acrrectx + acrw
    acrrecth=acry + acrh-22
    outputpoint[1][5]=getexactpoint("a","L_8k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcL555=",outputpoint[1][5])


    # identify 4row or 2row data
  
    buffery=23
    # acrrectx=acrx
    # acrrecty=acry+23
    # acrrectw=acrrectx + acrw
    # acrrecth=acrrecty +acrh-20
    # acrL_data=pdfimagetextconversion.getdata("b","r",grayimage.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # buffery=23
 
    # if "ACR" in acrL_data:
    #     buffery=46
        
    #     acrrectx=acrx
    #     acrrecty=acry+buffery
    #     acrrectw=acrrectx + acrw
    #     acrrecth=acrrecty +acrh-20
    #     acrL_data=pdfimagetextconversion.getdata("b","R",grayimage.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    row4status=isidentify4rowstable("b","r",grayimage.copy(),wpath,acrx,acry,acrw,acrh)
    if row4status:
        buffery=46
   
    # bcR 250 data
    acrrectx=acrx+180
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw+20
    acrrecth=acrrecty +acrh-18
    outputpoint[2][0]=getexactpoint("b","R_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr=",outputpoint[2][0])
    # bcR 500 data
    acrrectx=acrx+235
    acrrecty=acry+buffery-5
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20+5
    outputpoint[2][1]=getexactpoint("b","R_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr11=",outputpoint[2][1])

    # if (outputpoint[2][1] <10 and outputpoint[2][1]!=5) or outputpoint[2][1]==0 :
    #     acrrecty=acrrecty-3
    #     acrrecth=acrrecth+3
    #     outputpoint[2][1]=pdfimagetextconversion.getpoint("b","R_500",grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    #     print("bcr111=",outputpoint[2][1])
    # bcR 1k data
    acrrectx=acrx+325
    acrrecty=acry+buffery-2
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-18
    outputpoint[2][2]=getexactpoint("b","R_1k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr115=",outputpoint[2][2])
    # if (outputpoint[2][2] <10 and outputpoint[2][2]!=5) or  outputpoint[2][2]==0 or (outputpoint[2][2] %5 !=0 and outputpoint[2][2]>9):
    #         acrrectx=acrx+325
    #         acrrecty=acry+buffery
    #         acrrectw=acrrectx + acrw
    #         acrrecth=acrrecty +acrh-20
    #         outputpoint[2][2]=pdfimagetextconversion.getpoint("b","R_1k",grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    #         print("bcr1115=",outputpoint[2][2])

    # bcR 2k data
    acrrectx=acrx+415
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20
    outputpoint[2][3]=getexactpoint("b","R_2k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # bcR 4k data
    acrrectx=acrx+505
    acrrecty=acry+buffery-3
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20
    outputpoint[2][4]=getexactpoint("b","R_4k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr114=",outputpoint[2][4])
    # bcR 8k data
    acrrectx=acrx+595
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-24
    outputpoint[2][5]=getexactpoint("b","R_8k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)


    # bcL 250 data
    acrrectx=acrx+1120
    acrrecty=acry+buffery-2
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20
    outputpoint[3][0]=getexactpoint("b","L_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    # print("bcr300=",outputpoint[3][0])

    # if (outputpoint[3][0] <10 and outputpoint[3][0]!=5) or outputpoint[3][0]==0 :
    #         acrrectx=acrx+1120
    #         acrrecty=acry+buffery-3
    #         acrrectw=acrrectx + acrw
    #         acrrecth=acrrecty +acrh-18
    #         outputpoint[3][0]=pdfimagetextconversion.getpoint("b","L_250",grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    #         print("bcr300=",outputpoint[3][0])

    # bcL 500 dataBG BNUSFD
    
    acrrectx=acrx+1165
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-24
    outputpoint[3][1]=getexactpoint("b","L_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # bcL 1K data
    acrrectx=acrx+1260
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-22
    outputpoint[3][2]=getexactpoint("b","L_1k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # print("buffery=",buffery)
    # bcL 2K data
    acrrectx=acrx+1345
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20
    outputpoint[3][3]=getexactpoint("b","L_2k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # if (outputpoint[3][3] <10 and outputpoint[3][3]!=5) or outputpoint[3][3]==0 :
    #     acrrectx=acrx+1345
    #     acrrecty=acry+buffery
    #     acrrectw=acrrectx + acrw
    #     acrrecth=acrrecty +acrh-20
    #     outputpoint[3][3]=pdfimagetextconversion.getpoint("b","L_2k",grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)


    # bcL 4K data
    acrrectx=acrx+1435
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20
    outputpoint[3][4]=getexactpoint("b","L_4k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)

    # bcL 8K data
    acrrectx=acrx+1525
    acrrecty=acry+buffery
    acrrectw=acrrectx + acrw
    acrrecth=acrrecty +acrh-20
    outputpoint[3][5]=getexactpoint("b","L_8k",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
    
    return row4status,outputpoint


def getdata_AC_BC_R_L_mask_4row(grayimage,grayimage1,wpath,acrx,acry,acrw,acrh,outputpoint):
        
        buffery=20
        # acR_M 250 data
        d0=4
        d1=5
        d2=6
        d3=7
       
           
        acrrectx=acrx+180
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d0][0]=getexactpoint("a","M_R_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint40=",outputpoint[4][0])

        # acR_M 500 data
       
           
        acrrectx=acrx+235
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d0][1]=getexactpoint("a","M_R_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint41=",outputpoint[4][1])

        # acR_M 1K data
       
           
        acrrectx=acrx+325
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d0][2]=getexactpoint("a","M_R_1K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint42=",outputpoint[4][2])


        # acR_M 2K data
       
           
        acrrectx=acrx+415
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d0][3]=getexactpoint("a","M_R_2K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint43=",outputpoint[4][3])


        # acR_M 4K data
       
           
        acrrectx=acrx+505
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d0][4]=getexactpoint("a","M_R_4K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint44=",outputpoint[4][4])


      # acR_M 8K data

        acrrectx=acrx+595
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d0][5]=getexactpoint("a","M_R_8K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint45=",outputpoint[4][5])
        
      # acL_M 250 data
        acrrectx=acrx+1120
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d1][0]=getexactpoint("a","M_L_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint50=",outputpoint[5][0])
      # acL_M 500 data
       
           
        acrrectx=acrx+1165
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d1][1]=getexactpoint("a","M_L_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint51=",outputpoint[5][1])

        # acL_M 1K data
       
           
        acrrectx=acrx+1255
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d1][2]=getexactpoint("a","M_L_1K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint52=",outputpoint[5][2])


        # acL_M 2K data
       
           
        acrrectx=acrx+1345
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d1][3]=getexactpoint("a","M_L_2K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint53=",outputpoint[5][3])


        # acL_M 4K data
       
           
        acrrectx=acrx+1435
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d1][4]=getexactpoint("a","M_L_4K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint54=",outputpoint[5][4])


      # acL_M 8K data

        acrrectx=acrx+1525
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d1][5]=getexactpoint("a","M_L_8K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint55=",outputpoint[5][5])


        buffery+=46 

        # bcR_M 250 data
       
      
        acrrectx=acrx+180
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d2][0]=getexactpoint("b","M_R_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint60=",outputpoint[6][0])

         # bcR_M 500 data
       
           
        acrrectx=acrx+235
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d2][1]=getexactpoint("b","M_R_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint61=",outputpoint[6][1])

        # bcR_M 1K data
       
           
        acrrectx=acrx+325
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d2][2]=getexactpoint("b","M_R_1K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint62=",outputpoint[6][2])


        # bcR_M 2K data
       
           
        acrrectx=acrx+415
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d2][3]=getexactpoint("b","M_R_2K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint63=",outputpoint[6][3])


        # bcR_M 4K data
       
           
        acrrectx=acrx+505
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d2][4]=getexactpoint("b","M_R_4K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint64=",outputpoint[6][4])


      # bcR_M 8K data

        acrrectx=acrx+595
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d2][5]=getexactpoint("b","M_R_8K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint65=",outputpoint[6][5])

        # bcL_M 250 data
        acrrectx=acrx+1120
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d3][0]=getexactpoint("b","M_L_250",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint70=",outputpoint[d3][0])
      # bcL_M 500 data
       
           
        acrrectx=acrx+1165
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+20
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d3][1]=getexactpoint("b","M_L_500",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint71=",outputpoint[7][1])

        # bcL_M 1K data
       
           
        acrrectx=acrx+1255
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d3][2]=getexactpoint("b","M_L_1K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint72=",outputpoint[7][2])


        # bcL_M 2K data
       
           
        acrrectx=acrx+1345
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d3][3]=getexactpoint("b","M_L_2K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint73=",outputpoint[7][3])


        # bcL_M 4K data
       
           
        acrrectx=acrx+1435
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw+10
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d3][4]=getexactpoint("b","M_L_4K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint74=",outputpoint[7][4])


      # bcL_M 8K data

        acrrectx=acrx+1525
        acrrecty=acry+buffery
        acrrectw=acrrectx + acrw
        acrrecth=acrrecty +acrh-18
        
        outputpoint[d3][5]=getexactpoint("b","M_L_8K",grayimage.copy(),grayimage1.copy(),wpath,acrrectx,acrrecty,acrrectw,acrrecth)
        # print("outputpoint75=",outputpoint[7][5])


        return outputpoint
def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False