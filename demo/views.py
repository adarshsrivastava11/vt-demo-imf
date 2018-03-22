# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import matplotlib.pyplot as plt
import mpld3

fig = plt.figure(figsize=(10,5))
f = open('omni_min201801.asc','r')
min_1_omni_list = []
for lines in f:
    columns = lines.split()
    min_1_omni_dict = {
        'Year':int(columns[0]),
        'Day':int(columns[1]),
        'Hour':int(columns[2]),
        'Minute':int(columns[3]),
        'Percent_Interp':columns[7],
        'Time_Shift':columns[8],
        'Time_Between_Observation':columns[11],
        'Fixed_Magnitude_Average':columns[12],
        'Bx_GSE':float(columns[13]),
        'By_GSE':float(columns[14]),
        'Bz_GSE':float(columns[15]),
        'B':float(columns[18]),
        'Flow_Speed':float(columns[20]),
        'Vx':float(columns[21]),
        'Vy':float(columns[22]), 
        'Vz':float(columns[23]), 
        'Proton_Density':columns[24]
    }
    min_1_omni_list.append(min_1_omni_dict)
    
print min_1_omni_list[1]
f.close()
max_val_dict = {
    'Percent_Interp':999,
    'Time_Shift':999,
    'Time_Between_Observation':99.99,
    'Fixed_Magnitude_Average':999999,
    'Bx_GSE':9999.99,
    'By_GSE':9999.99,
    'Bz_GSE':9999.99,
    'B':9999.99,
    'Flow_Speed':9999.99,
    'Vx':99999.9,
    'Vy':99999.9,
    'Vz':99999.9,
    'Proton_Density':99999.9
}

def plot_day(value_y,day):
    x_axis = []
    y_axis = []
    k = 0
    for elements in min_1_omni_list:
        if(elements["Day"] == day):
            k = k+1


            if(elements[value_y] != max_val_dict[value_y]):
                y_axis.append(elements[value_y])
                x_axis.append(k)
    plt.xlabel("Minutes")
    plt.ylabel(value_y)
    plt.plot(x_axis, y_axis)
    g = mpld3.fig_to_html(fig)
    return g
    # plt.show()
# plot_day("Bz_GSE",max_val_dict["Bz_GSE"],5)
# plot_day("B",max_val_dict["B"],5)
def plot_B(component_B,day):
    N = 1400
    area = []
    x_axis = []
    y_axis = []
    k = 0
    for elements in min_1_omni_list:
        if(elements["Day"] == day):
            k = k+1
            if(elements["B"] != 9999.99 and elements[component_B] != 9999.99):
                y_axis.append(elements[component_B])
                x_axis.append(k)
                if (elements["B"] < 0):
                    b_val = -elements["B"]
                else:
                    b_val = elements["B"]
                area.append(b_val*50.0)
    plt.xlabel("Minute")
    plt.ylabel(component_B+" nT")
    plt.scatter(x_axis, y_axis, s=area, alpha=0.5)
    g = mpld3.fig_to_html(fig)
    return g
    # plt.show()
# plot_B("Bx_GSE",1)
# plot_B("Bz_GSE",1)
# plt.figure(figsize=(20,10))
def plot_xy(value_x,value_y,day):
    x_axis = []
    y_axis = []
    for elements in min_1_omni_list:
        if(elements["Day"] == day):
            if(elements[value_y] != max_val_dict[value_y] and elements[value_x] != max_val_dict[value_x]):
                y_axis.append(elements[value_y])
                x_axis.append(elements[value_x])
    plt.xlabel(value_x)
    plt.ylabel(value_y)
    plt.plot(x_axis, y_axis, 'ro')
    g = mpld3.fig_to_html(fig)
    return g
    # plt.show()
# plot_xy("B","Proton_Density",1)
# plot_xy("B","Bz_GSE",1)
# Create your views here.
def main_page(request):
    g = ""
    type_of_plot = request.POST.get('type_of_graph', False)
    day = request.POST.get('day',False)
    val_x = request.POST.get('val_x', False)
    val_y = request.POST.get('val_y', False)
    if type_of_plot != False and day != False:
        if (val_x != False and type_of_plot == "plot_day"):
            g = plot_day(val_x,int(day))
        if (val_x != False and val_y != False and type_of_plot == "plot_xy"):
            g = plot_xy(val_x,val_y,int(day))
        if (val_x != False and type_of_plot == "plot_B"):
            g = plot_B(val_x,int(day))
    return render(request,'demo.html',{'graph_code':g})
def output_page(request,code):
    return render(request,'demo.html',{'graph_code':code})