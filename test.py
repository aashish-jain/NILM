from statistics import mean
minimum_jump_magnitude=5
class C1:
    jump_magnitude=0

class C2:
    first_maxima=0
    avg_transient_ipeaks=0
    settling_time=0

class C3:
    avg_steadystate=0

class template_library(C1,C2,C3):
    device=''
    def print_val(self):
        print '_'*80
        print self.device
        print "jump_magnitude={0} ".format(self.jump_magnitude)
        print "first_maxima={0} avg_transient_ipeaks={1} ".format(self.first_maxima,self.avg_transient_ipeaks)
        print "settling_time={0} avg_steadystate={1}".format(self.settling_time,self.avg_steadystate)
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
    while( data[i] - data[i+1] != 1 ):
        temp.append(data[i]-previous_steadystate)
        i+=1
    t.settling_time=i
    if(len(temp)!=0):
        t.avg_transient_ipeaks=mean(temp)
    del temp
    data=data[i:]

    while(i<len(data) and i<11):                                                #Ipeak average is calculated for 5 rises
        t.avg_steadystate+=(data[i]-previous_steadystate);
        i+=1
    t.avg_steadystate/=i
    del ptr
    t.print_val()

extract_characteristics(data)
