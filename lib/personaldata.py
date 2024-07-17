import lib.pdfimagetextconversion as pdfimagetextconversion


def getpersonaldata(filename,pdfpath):
    # print("start")
    p_data= [str("") for i in range(5)] 
    filepath=f"{pdfpath}\{filename}.pdf"
    try:
        content = pdfimagetextconversion.get_text_from_any_pdf(filepath)
        name =""
        # print("p_data=",p_data)
        # i=1
        # for element in content:
        #     print(i,"=",element)
        #     i=i+1

        # namestartindex=content.find(':')+1
        # # print("namestartindex=",namestartindex)

        # nameendindex=content.find('-')+1
        # print("nameendindex=",nameendindex)

        # lines=content.splitlines()
        i=1
        PATIENT_LINE=""
        # print(content.splitlines(True))
        if content.splitlines(True):
            for line in content.splitlines():
                
                if "PATIENT" in line:
                    PATIENT_LINE=line
                #   print(i,"=",line)
                    break
                i=i+1
        if len(PATIENT_LINE)==0:
            return p_data
        

    

        dateline_LINE=""
        if content.splitlines(True):
            for line in content.splitlines():
                
                if "Pure tone audiometry" in line:
                    dateline_LINE=line
                    #   print(i,"=",dateline_LINE)
                    break
                i=i+1

        # print("dateline_LINE=",dateline_LINE)   
        p_data[0]=getpatientname(PATIENT_LINE)
        p_data[1]=getMRDno(PATIENT_LINE)
        p_data[2]=getage(PATIENT_LINE)
        p_data[3]=getgender(PATIENT_LINE)
        p_data[4]=getdate(dateline_LINE)
        # datet=getdate(dateline_LINE)    
       
        # gender=getgender(PATIENT_LINE)
        # MRDno=getMRDno(PATIENT_LINE)
        # age=getage(PATIENT_LINE)
        # print("date-=",datet)
        # print("MRDno-=",MRDno)
        # print("gender=",gender)
        # print("age=",age)
    except:
        print("invalid pdf file")
        

    return p_data
def getage(PATIENT_LINE):
    age=None
    # print("dateline_LINE=",PATIENT_LINE)
    if "Age" in PATIENT_LINE:
        startindex=PATIENT_LINE.index('Age')
        # print("startindex=",startindex)
        startindex+=4
        age1=PATIENT_LINE[startindex:].strip()
        # print("age1=",age1)
        age1array =age1.split('-')
        age=age1array[0].strip()
        # print("age==",age)
    return age



def getdate(dateline_LINE):
    datet=None
    # print("dateline_LINE=",dateline_LINE)
    
    # id.r
    if "-" in dateline_LINE:
        startindex=dateline_LINE.index('-')
        # print("index-=",startindex)
        
        if startindex>0:
            startindex+=1
            dateline_LINE2=dateline_LINE[startindex:].strip()
            # print("dateline_LINE2=",dateline_LINE2)
            dateline_LINE2_array=dateline_LINE2.split(" ")
            # print("dateline_LINE2_array=",dateline_LINE2_array)
            if len(dateline_LINE2_array)>0:
                datet=dateline_LINE2_array[0].strip()
        # print("MRDno-=",MRDno)
    return datet

def getMRDno(PATIENT_LINE):
    MRDno=None
    # print("PATIENT_LINE=",PATIENT_LINE)
    
    # id.r
    if "-" in PATIENT_LINE:
        startindex=PATIENT_LINE.rindex('-')
        # print("index-=",startindex)
        
        if startindex>0:
            startindex+=1
            MRDno=PATIENT_LINE[startindex:].strip()
    # print("MRDno-=",MRDno)
    return MRDno


def getgender(PATIENT_LINE):
    gender="Male"
    # print("PATIENT_LINE=",PATIENT_LINE)
    if "- F -" in PATIENT_LINE:
        gender="Female"
    
    return gender



    

def getpatientname(PATIENT_LINE):
    namestartindex=PATIENT_LINE.find(':')+1
    # print("namestartindex=",namestartindex)
    nameendindex=PATIENT_LINE.find('-')
    # print("nameendindex=",nameendindex)        
    name=PATIENT_LINE[namestartindex:nameendindex].strip()
    # print("check SLS name=",("SLS" in PATIENT_LINE))
    if ("SLS" in PATIENT_LINE)==True:
        nameline1=str(PATIENT_LINE).strip()
        namelinearray=nameline1.split(" ")
        # print("namel====",namelinearray)
        if len(namelinearray)>1:
             name=namelinearray[1].strip()
            #  print("name_SLS====",name)
    # print("name=",name)
    return name
