import matplotlib as mpl
import matplotlib.pyplot as plt, mpld3
import numpy as np

def calcBR(birthday, date):
    fig, ax = plt.subplots()
    x = date #date
    k = birthday # birthdate
    

    t = np.arange(x-1, x+1, 0.1)

    green_br = np.sin((np.pi*t)/16.5 + (k*np.pi))
    green_br_dot = np.sin((np.pi*x)/16.5 + (k*np.pi))

    red_br = np.sin((np.pi*t)/14 + (k*np.pi))
    red_br_dot = np.sin((np.pi*x)/14 + (k*np.pi))

    blue_br = np.sin((np.pi*t)/11.5 + (k*np.pi))
    blue_br_dot = np.sin((np.pi*x)/11.5 + (k*np.pi))

    line, = ax.plot(t, green_br, 'g', label=f"Intellectual: {round(green_br_dot,4)*100}%")
    today1, = ax.plot(x, green_br_dot, 'go')
    line2, = ax.plot(t, red_br, 'r', label=f"Emotional: {round(red_br_dot,4)*100}%")
    today2, = ax.plot(x, red_br_dot, 'ro')
    line3, = ax.plot(t, blue_br, 'b', label=f"Physical: {round(blue_br_dot,4)*100}%")
    today3, = ax.plot(x, blue_br_dot, 'bo')
    
    plt.ylabel('Biorhythm Status', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    
    leg = ax.legend(handles=[line,line2,line3], loc='upper right')
    ax.add_artist(leg)
    
    ax.set_title('Biorhythm', size=20)
    plt.ylim(-1, 1)

    return mpld3.fig_to_html(fig)
    #return mpld3.fig_to_dict(fig)


def calcBRFC(birthday, date):
    fig, ax = plt.subplots()
    x = date #date
    k = birthday # birthdate
    

    t = np.arange(x-10, x+10, 0.1)
    t_days = np.arange(x-10, x+10, 1.0)

    green_br = np.sin((np.pi*t)/16.5 + (k*np.pi))
    green_br_dot = np.sin((np.pi*t_days)/16.5 + (k*np.pi))
    green_today = np.sin((np.pi*x)/16.5 + (k*np.pi))

    red_br = np.sin((np.pi*t)/14 + (k*np.pi))
    red_br_dot = np.sin((np.pi*t_days)/14 + (k*np.pi))
    red_today = np.sin((np.pi*x)/14 + (k*np.pi))

    blue_br = np.sin((np.pi*t)/11.5 + (k*np.pi))
    blue_br_dot = np.sin((np.pi*t_days)/11.5 + (k*np.pi))
    blue_today = np.sin((np.pi*x)/11.5 + (k*np.pi))

    line, = ax.plot(t, green_br, 'g', label=f"Intellectual: {round(green_today,4)*100}%")
    today1, = ax.plot(t_days, green_br_dot, 'go')
    line2, = ax.plot(t, red_br, 'r', label=f"Emotional: {round(red_today,4)*100}%")
    today2, = ax.plot(t_days, red_br_dot, 'ro')
    line3, = ax.plot(t, blue_br, 'b', label=f"Physical: {round(blue_today,4)*100}%")
    today3, = ax.plot(t_days, blue_br_dot, 'bo')
    
    plt.ylabel('Biorhythm Status', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    
    leg = ax.legend(handles=[line,line2,line3], loc='upper right')
    ax.add_artist(leg)
    
    ax.set_title('Biorhythm', size=20)
    plt.ylim(-1, 1)

    return mpld3.fig_to_html(fig)