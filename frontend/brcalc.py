import matplotlib as mpl
import matplotlib.pyplot as plt, mpld3
import numpy as np
from datetime import datetime

def calcBR(birthday, date):
    fig, ax = plt.subplots()
    x = date #date
    k = birthday # birthdate
    
    phase = int((x - k).days)

    t = np.arange(phase-1, phase+1, 0.1)

    green_br = np.sin((np.pi*2*t)/16.5)
    green_br_dot = np.sin((np.pi*2*phase)/16.5)

    red_br = np.sin((np.pi*2*t)/14)
    red_br_dot = np.sin((np.pi*2*phase)/14)

    blue_br = np.sin((np.pi*2*t)/11.5)
    blue_br_dot = np.sin((np.pi*2*phase)/11.5)

    line, = ax.plot(t, green_br, 'g', label=f"Intellectual: {round(green_br_dot,4)*100}%")
    today1, = ax.plot(phase, green_br_dot, 'go')
    line2, = ax.plot(t, red_br, 'r', label=f"Emotional: {round(red_br_dot,4)*100}%")
    today2, = ax.plot(phase, red_br_dot, 'ro')
    line3, = ax.plot(t, blue_br, 'b', label=f"Physical: {round(blue_br_dot,4)*100}%")
    today3, = ax.plot(phase, blue_br_dot, 'bo')
    
    plt.ylabel('Biorhythm Status', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    
    leg = ax.legend(handles=[line,line2,line3], loc='upper right')
    ax.add_artist(leg)
    
    ax.set_title('Biorhythm', size=20)
    plt.ylim(-1, 1)
    plt.grid(True,axis='y')

    return mpld3.fig_to_html(fig)
    #return mpld3.fig_to_dict(fig)


def calcBRFC(birthday, date):
    fig, ax = plt.subplots()
    x = date #date
    k = birthday # birthdate
    

    phase = int((x - k).days)

    t = np.arange(phase-10, phase+10, 0.1)
    t_days = np.arange(phase-10, phase+10, 1.0)

    green_br = np.sin((np.pi*2*t)/16.5)
    green_br_dots = np.sin((np.pi*2*t_days)/16.5)
    green_br_today = np.sin((np.pi*2*phase)/16.5)

    red_br = np.sin((np.pi*2*t)/14)
    red_br_dots = np.sin((np.pi*2*t_days)/14)
    red_br_today = np.sin((np.pi*2*phase)/14)

    blue_br = np.sin((np.pi*2*t)/11.5)
    blue_br_dots = np.sin((np.pi*2*t_days)/11.5)
    blue_br_today = np.sin((np.pi*2*phase)/11.5)

    line, = ax.plot(t, green_br, 'g', label=f"Intellectual: {round(green_br_today,4)*100}%")
    today1, = ax.plot(t_days, green_br_dots, 'go')
    line2, = ax.plot(t, red_br, 'r', label=f"Emotional: {round(red_br_today,4)*100}%")
    today2, = ax.plot(t_days, red_br_dots, 'ro')
    line3, = ax.plot(t, blue_br, 'b', label=f"Physical: {round(blue_br_today,4)*100}%")
    today3, = ax.plot(t_days, blue_br_dots, 'bo')
    
    plt.ylabel('Biorhythm Status', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    
    leg = ax.legend(handles=[line,line2,line3], loc='upper right')
    ax.add_artist(leg)
    
    ax.set_title('Biorhythm', size=20)
    plt.ylim(-1, 1)
    plt.grid(True,axis='y')

    return mpld3.fig_to_html(fig)