#Author: Zico Da silva and Best Nkhumeleni
#Date: 23 November 2022
#import h5py
import pandas as pd
import numpy as np
import csv
from io import StringIO

numberofframes = 100
csvfile = r'C:\Users\Best Nkhumeleni\Desktop\Deeplabcut\acinoset-test\labeled-data\2019_03_07_phantom_run_cam4\CollectedData_UCT.csv'
hdf5file = r'C:\Users\Best Nkhumeleni\Desktop\Deeplabcut\acinoset-test\labeled-data\2019_03_07_phantom_run_cam4\CollectedData_UCT.h5'
#df = pd.read_hdf(hdf5file)

def linefind(filename,numberofframes):
    df = pd.read_hdf(filename)
    for i in range (1,numberofframes+1):
        x = 0   
        for name, values in df[i-1:i].iteritems():
                if(values[0].astype('str') != 'nan'):
                    x=x+1
        if x==0:
            return i

def linefixer(xf,i):
    linewewannacopy = xf[i-2:i-1]
    temp = linewewannacopy.copy() 
    num = i-1
    newindex =''
    if i<10:
        newindex = ['labeled-data\\2019_03_07_phantom_run_cam3\img10'+str(num)+'.png']
    else:
        newindex = ['labeled-data\\2019_03_07_phantom_run_cam3\img1'+str(num)+'.png']
    #temp.set_index(newindex)
    temp.index = newindex
    return temp

#print(linefixer(df,linefind(hdf5file,numberofframes)))

def combines(filename,numberofframes): #idea number 15, break our orignal dataset in to multiple sets and isolate the one you wanna edit, then concat them back together.
    xf = pd.read_hdf(hdf5file) 
    i = linefind(filename,numberofframes)
    tophalf = xf[:i-1].copy()
    bottomhalf= xf[i:].copy()
    #temp = pd.DataFrame()
    lineofinterest = linefixer(xf,i)
    df = pd.concat([tophalf,lineofinterest], ignore_index=False) # this breaks it apart and recombines it with the row having been copied but the key does change
    df = pd.concat([df,bottomhalf], ignore_index=False)
    return df

df = combines(hdf5file,numberofframes)
df.to_hdf(hdf5file,key = "df",mode="w")
print(df)




















#df = pd.read_csv(csvfile)
#print(df.to_string())



def linefindcsv(filename):
     with open(filename) as x:
        i = 0
        for line in x:
            i+=1
            if not (any(char.isdigit() for char in line[51:])):
                if i>4:
                    return i-1
   

#print(linefindcsv(csvfile,numberofframes))

def linefixercsv(xf,i):
    linewewannacopy = xf[i-1:i]
    temp = linewewannacopy.copy() 
    num = i
    newindex = [str(num)]
    temp.index = newindex
    return temp

#print(linefixer(df,linefind(hdf5file,numberofframes)))

def writecsv(filename,file):
    x = open(filename,"w")
    x.close()
    for row in file:
        s = StringIO(row)
        with open(filename, 'a') as f:
            for line in s:
                f.write(line)


def meth2csv(filename):
    i = linefindcsv(filename)
    with open(filename) as f:
         file = f.readlines()
         #file[i:i+1] = file[i-1:i]
         linepos = i
         edit = file[i-1]
         end = edit.find("png")
         tophalf = edit[:end-3]
         bottomhalf = edit[end-1:]
         if (i-3)<10:
            edited = tophalf+"0"+str(i-3)+bottomhalf
         else:
            edited = tophalf+str(i-3)+bottomhalf
         file[linepos] = edited
         #print(edit,"\n",edited)
         writecsv(filename,file)
    


#print(combinecsv(csvfile,numberofframes))
meth2csv(csvfile)
#df.to_csv(csvfile.split(".")[0] + ".csv")