#!/usr/bin/env python
'''    Non Intrusive device identification - characteristics extraction and identification
       Smart Devices group-Solarillion Foundation
'''

from openpyxl import load_workbook
from random import randrange
from statistics import mean
from math import sqrt
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
    c3(avg_steadystate_ipeaks,settling_time,avg_transient_ipeaks)

    template_library.extract_characteristics->extracts and stores information about c1,c2,c3
    runtime-> device identification
'''


#constant(s) set after empirically observing the data
minimum_jump_magnitude=5
t=[]
devices=['Bulb','Fan','Heater','Cooler','Soldering Iron']

class C1:
    jump_magnitude=0
    jump_instance=0

class C2:
    first_maxima=0
    first_maxima_index=0

class C3:
    settling_time=0
    avg_transient_ipeaks=0
    avg_steadystate_ipeaks=0.0


class template_library(C1,C2,C3):
    device=''
    def print_val(self):
        print '_'*80
        print self.device
        print "jump_magnitude={0} jump_instance={1} ".format(self.jump_magnitude,self.jump_instance)
        print "first_maxima={0} first_maxima_index={1} ".format(self.first_maxima,self.first_maxima_index)
        print "avg_steadystate_ipeaks={0} settling_time={1} avg_transient_ipeaks={2}".format(self.avg_steadystate_ipeaks,self.settling_time,self.avg_transient_ipeaks)
        print '_'*80

def extract_characteristics(data,device=""):                                    #for extracting characteristics
    t=template_library()                                                        #for storing the characteristics
    t.device=device
    i=1                                                                         #setting index count of data to be 1
    #c1
    previous_steadystate=data[0]                                                #Assuming first value of data to be SS value
    while(data[i]-previous_steadystate<minimum_jump_magnitude):                 #traverse the array till a jump is detected
        i+=1
    reference=i
    i+=1                                                                        #considering the second instantaneous Ipeak value
    t.jump_instance=2
    t.jump_magnitude=data[i]-previous_steadystate                               #storing jump_magnitude
    i+=1
    #c2
    while(data[i]<data[i+1]):                                                   #finding first maxima
        i+=1
    t.first_maxima=data[i]-previous_steadystate                                 #storing first maxima magnitude
    t.first_maxima_index=i                                                      #storing first maxima index
    i+=1
    #c3
    temp=[]
    i+=2
    while(data[i]-data[i+5]>3):
        temp.append(data[i]-data[i+1])
        i+=1
    t.settling_time=i-reference
    if(len(temp)!=0):
        t.avg_transient_ipeaks=mean(temp)
    j=i
    while(i<len(data) and i-j<11):                                               #Ipeak average is calculated for 5 rises
        t.avg_steadystate_ipeaks+=(data[i]-previous_steadystate);
        i+=1

    t.avg_steadystate_ipeaks/=(i-j)
    return t

#reads data from given excel sheet (name of excel file and sheet should be same)
def read_excelsheet(device,c=0):
    wb = load_workbook('/home/aashish/DI/data/'+device+'.xlsx')                 #create instance of load_workbook
    work_sheet=wb['Sheet']                                                       #select the required worksheet
    c=randrange(65,85) if c==0 else c+64                                        #if no trial specified choose any random trail
    data=[]                                                                     #list to store Ipeak values
    for i in range(2,202):                                                      #copy values from cells and store it in data list
        data.append(work_sheet[chr(c)+str(i)].value)
    return extract_characteristics(data,device)                                 #return the extracted chracterisitcs from data

def euclidean_distance_list(on_device):
    d=[]
    for i in range(0,len(t)):
        temp=(t[i].jump_magnitude - on_device.jump_magnitude)**2;
        temp+=(t[i].first_maxima - on_device.first_maxima)**2
        temp+=(t[i].avg_transient_ipeaks - on_device.avg_transient_ipeaks)**2
        temp+=(t[i].settling_time - on_device.settling_time)**2
        temp+=(t[i].avg_steadystate_ipeaks - on_device.avg_steadystate_ipeaks)**2
        d.append(sqrt(abs(temp)))
    return d

def identify_device():
    for device in devices:
        print '_'*80
        print 'Actual Device : '+device
        for i in range(1,21):
            distance=euclidean_distance_list(read_excelsheet(device,i))
            # for i in range(0,len(devices)):
            #     print (str(round(distance[i],2))).ljust(6),
            # print
            min_index=0
            for i in range(0,len(distance)):
                if(distance[min_index]>distance[i]):
                    min_index=i
            try:
                print devices[min_index]
            except:
                print len(distance),' ',min_index
            # max_index=0
            # for j in range(1,len(distance_list)):
            #     if distance_list[max_index]<distance_list[j]:
            #         max_index=j
            # print device[max_index]

#Main code exectution starts here
trial_number=randrange(1,21)
print "trial_number ",trial_number
for device in devices:
    t.append(read_excelsheet(device,trial_number))
for i in range(0,len(t)):
    t[i].print_val()
identify_device()
