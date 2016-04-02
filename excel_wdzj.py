# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from pylab import plot,show
from scipy.cluster.vq import kmeans,vq
wb=load_workbook('sepwdzj.xlsx')
di={}
data_list=[]
ws = wb.active
c_item=0;

for cell in ws:
    for i in cell:
        data_list.append(i.value)
#print data_list
data_list1=np.array(data_list)
data=data_list1.reshape((101,12))
print
index=data[0]
data1=pd.DataFrame(data[1:,1:],dtype="float").as_matrix()
print data1
#print data1.mean(0)
n=2
data1[:,1]*=0.07
data1[:,2]*=0.06
data1[:,3]*=0.15
data1[:,4]*=0.4
data1[:,5]*=0.14
data1[:,6]*=0.05
data1[:,7]*=0.15
data1[:,8]*=0.15
data1[:, 9]*=0.19

centroids,_ = kmeans(data1[:,1:-1],n)
print centroids
print _
# assign each sample to a cluster
idx,_ = vq(data1[:,1:-1],centroids)
print data1
print idx
color=['r','g','b','c','m','y','k','w']
for i in range(n):
    print i, color[i]
    print data1[idx==i,0]
    plot(data1[idx==i,0],data1[idx==i,10],'o'+color[i])
# some plotting using numpy's logical indexing
show()