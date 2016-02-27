#!/usr/bin/env python
'''
        Non Intrusive device identification - characteristics extraction and identification
        Smart Devices group-Solarillion Foundation
'''

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

from openpyxl import load_workbook
from random import randrange
from statistics import mean
from math import sqrt

#constant(s) set after empirically observing the data
minimum_jump_magnitude=3
t=[]
devices=['D1','D2','D3','D4','D5']

class C1:
    jump_magnitude=0
    first_maxima=0

class C2:
    avg_transient_ipeaks=0
    settling_time=0

class C3:
    avg_steadystate=0

class template_library(C1,C2,C3):
    device=''
    def print_val(self):
        print '_'*80
        print self.device
        print "jump_magnitude={0} first_maxima={1} ".format(self.jump_magnitude,self.first_maxima)
        print " avg_transient_ipeaks={0} settling_time={0}ms".format(self.avg_transient_ipeaks,self.settling_time*20)
        print " avg_steadystate={0}".format(self.avg_steadystate)
        print '_'*80

def extract_characteristics(data,device=""):                                    #for extracting characteristics
    ptr=data
    t=template_library()                                                        #for storing the characteristics
    t.device=device
    previous_steadystate=data[0]                                                #Assuming first value of data to be SS value
    i=1                                                                         #setting index count of data to be 1
    #c1
    while(data[i]-previous_steadystate<minimum_jump_magnitude):                 #traverse the array till a jump is detected
        i+=1
    data=data[(i-1):]                                                           #truncating the Ipeak Data
    i=2                                                                         #considering the second Ipeak value
    t.jump_magnitude=data[i]-previous_steadystate                               #storing jump_magnitude
    i+=1
    #c2
    while(data[i]<data[i+1]):                                                   #finding first maxima
        i+=1
    t.first_maxima=data[i]-previous_steadystate                                 #storing first maxima magnitude
    i+=1
    #transient and steady state average, settling time
    temp=[]
    while( data[i] - data[i+1] > 1 ):                                           #transient average calculation
        temp.append(data[i]-previous_steadystate)
        i+=1
    t.settling_time=i
    if(len(temp)!=0):
        t.avg_transient_ipeaks=mean(temp)
    del temp
    data=data[i:]
    i=0
    while(i<len(data) and i<10):
        t.avg_steadystate+=(data[i]-previous_steadystate);
        i+=1
    t.avg_steadystate/=i
    del ptr
    return t

#reads data from given excel sheet (name of excel file and sheet should be same)
def read_excelsheet(device,c=0):
    wb = load_workbook('/home/aashish/DI/data/1/'+device+'.xlsx')               #create instance of load_workbook
    work_sheet=wb['Sheet1']                                                     #select the required worksheet
    c=randrange(65,85) if c==0 else c+64                                        #if no trial specified choose any random trail
    data=[]                                                                     #list to store Ipeak values
    for i in xrange(2,202):                                                      #copy values from cells and store it in data list
        data.append(work_sheet[chr(c)+str(i)].value)
    return extract_characteristics(data,device)                                 #return the extracted chracterisitcs from data

def euclidean_distance_list(on_device):
    d=[]
    for i in xrange(0,len(t)):
        temp=[]
        temp.append((t[i].jump_magnitude - on_device.jump_magnitude)**2)
        temp.append((t[i].first_maxima - on_device.first_maxima)**2)
        temp.append((t[i].avg_transient_ipeaks - on_device.avg_transient_ipeaks)**2)
        temp.append((t[i].settling_time - on_device.settling_time)**2)
        temp.append((t[i].avg_steadystate - on_device.avg_steadystate)**2)
        # print i+1,' Temp= ',
        # for i in xrange(0,len(temp)):
        #     print (str(round(sqrt(temp[i]),2))).ljust(6),
        # print
        d.append(sqrt(abs(sum(temp))))
        del temp
    return d

def identify_device():
    for device in devices:
        print '_'*80
        print 'Actual Device : ',device,' '
        for i in xrange(1,21):
            distance=euclidean_distance_list(read_excelsheet(device,i))
            # for i in xrange(0,len(devices)):
            #     print (str(round(distance[i],2))).ljust(6),
            min_index=0
            for i in xrange(1,len(distance)):
                if(distance[min_index]>distance[i]):
                    min_index=i
            print devices[min_index]

#Main code exectution starts here
trial_number=int(raw_input('Enter the trail number :'))
print "trial_number ",trial_number
for device in devices:
    t.append(read_excelsheet(device,trial_number))
# for i in xrange(0,len(t)):
#     t[i].print_val()
identify_device()
