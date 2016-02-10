#!/usr/bin/env python
'''    Non Intrusive device identification - characteristics extraction and identification
       Smart Devices group-Solarillion Foundation
'''

from openpyxl import load_workbook
from statistics import stdev
from random import randrange

'''
    PIP-> pyhton library manager
    to install library commmand is:
        pip install <Package_name>
    statistics.stdev library used for calculating standard devaition
    openpyxl.load_workbook for reading data from excel
    random.randrange for genrating random numbers within a range
'''

'''
    c1(jump_magnitude,jump_instance)
    c2(first_maxima,first_maxima_index)
    c3(average_Ipeaks,c3_cycles,c3_tolerance)

    template_library.extract_characteristics->extracts and stores information about c1,c2,c3
    runtime-> device identification
'''


#constant(s) set after empirically observing the data
minimum_jump_magnitude=5
t=[]
devices=['Bulb','Fan','Heater','Cooler','Soldering Iron']
trial_number=1

class C1:
    jump_magnitude=0
    jump_instance=0

class C2:
    first_maxima=0
    first_maxima_index=0

class C3:
    average_Ipeaks=0.0
    c3_cycles=0
    c3_tolerance=0


class template_library(C1,C2,C3):
    def print_val(self):
        print '_'*80
        print "jump_magnitude={0} jump_instance={1} ".format(self.jump_magnitude,self.jump_instance)
        print "first_maxima={0} first_maxima_index={1} ".format(self.first_maxima,self.first_maxima_index)
        print "average_Ipeaks={1} c3_cycles={1} tolerance={2}".format(self.average_Ipeaks,self.c3_cycles,self.c3_tolerance)
        print '_'*80


def extract_characteristics(data):                                              #for extracting characteristics
    t=template_library()                                                        #for storing the characteristics
    i=1                                                                         #setting index count of data to be 1
    #c1
    previous_steadystate=data[0]                                                #Assuming first value of data to be SS value
    while(data[i]-previous_steadystate<minimum_jump_magnitude):                 #traverse the array till a jump is detected
        i+=1
    i+=1                                                                        #considering the second instantaneous Ipeak value
    t.jump_instance=2
    t.jump_magnitude=data[i]-previous_steadystate                               #storing jump_magnitude
    i+=1
    #c2
    while(data[i]<data[i+1]):                                                   #finding first maxima
        i+=1
    t.first_maxima=data[i]-data[0]                                                      #storing first maxima magnitude
    t.first_maxima_index=i                                                      #storing first maxima index
    i+=1
    #c3
    t.c3_cycles=0
    temp=[]
    rise_count=0
    while(i<len(data) and rise_count!=5):                                       #Ipeak average is calculated for 5 rises
        if(data[i+1]>data[i]):
            rise_count+=1
        t.c3_cycles+=1
        t.average_Ipeaks+=(data[i]-data[0]);
        temp.append(data[i])
        i+=1
    temp.append(data[i]-data[0])
    t.average_Ipeaks/=t.c3_cycles
    t.c3_tolerance=stdev(temp)                                                  #calculates the tolerance for average_Ipeaks
    return t

#reads data from given excel sheet (name of excel file and sheet should be same)
def read_excelsheet(device,c=0):
    wb = load_workbook('/home/aashish/Desktop/data/'+device+'.xlsx')            #create instance of load_workbook
    work_sheet=wb[device]                                                       #select the required worksheet
    c=randrange(65,85) if c==0 else c+64                                        #if no trial specified choose any random trail
    data=[]                                                                     #list to store Ipeak values
    for i in range(2,202):                                                      #copy values from cells and store it in data list
        data.append(work_sheet[chr(c)+str(i)].value)
    return extract_characteristics(data)                                        #return the extracted chracterisitcs from data

def device_identification(on_device):
    #finding closest matches for c1,c2,c3
    i=0
    min1,min2,min3 = 1023,1023,1023                                             #variable for initial comaparison
    closest_match=[-1,-1,-1]                                                    #Stores the closes device match (c1,c2,c3)
    while i<len(devices):
        #c1
        d1=abs(t[i].jump_magnitude - on_device.jump_magnitude)
        # print d1
        if(d1<min1):
            min1=d1
            closest_match[0]=i
        #c2
        d2=abs(t[i].first_maxima - on_device.first_maxima)
        # print d2
        if(d2<min2):
            min2=d2
            closest_match[1]=i
        #c3
        d3=abs(t[i].average_Ipeaks - on_device.average_Ipeaks)
        # print d3
        if(d3<min3):
            min3=d3
            closest_match[2]=i
        i+=1
    print closest_match

#
# def identify_device(closest_match):
#     d=[0]*len(template)
#     for i in range(0,2):
#         for j in range(0,4):
#             if(closest_match[i]==j):
#                 d[i]+=1


#Main code exectution starts here
for device in devices:
    t.append(read_excelsheet(device,trial_number))
for i in range(0,len(t)):
    t[i].print_val()
for sheet_name in devices:
    #sheet_name=raw_input("Enter the name of device: ")
    for tno in range(1,21):
        print sheet_name,' trailno =',tno,' ',
        device_identification(read_excelsheet(sheet_name,tno))
