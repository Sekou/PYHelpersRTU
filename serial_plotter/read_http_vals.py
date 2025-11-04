#2025, S.Diane, script for reading multi-valued serial data from Arduino, ESP32, etc.

import sys, pygame
import time, threading
import real_time_plotter #2025, S.Diane
import requests, re

# Define the URL you want to request
url = "http://192.168.0.164/"

def get_vals():
    # Send a GET request
    response = requests.get(url)
    # Access the response content as a Unicode string
    response_text = response.text
    matches = re.findall("\<p\>[\d-].+?\</p>", response_text)
    s=", ".join(matches).replace("<p>", "").replace("</p>", "")
    # Print the text content
    # print(s)
    return s

NUM_VALS=18

class Data: #data for plotting
    def __init__(self):
        self.x_data, self.y_data = [], []
    def get_zero_shifted_x_data(self):
        return [x-self.x_data[0] for x in self.x_data]
    def get_x_inds(self):
        return list(range(len(self.x_data)))
    def add_val(self, t, v):
        self.x_data.append(t)
        self.y_data.append(v)
        if len(self.x_data) > 100:  # Keep last N points
            for data in [self.x_data, self.y_data]: data.pop(0)

datas=[Data() for j in range(3) for i in range(6)]

lock = threading.Lock()

ii, hreal, mode=[], 0, "0"
ii1=[0,1,2, 6,7,8, 12,13,14, 18,19,20] #accelerometers
hreal1=40000
ii2=[i+3 for i in ii1] #gyroscopes
hreal2=2000

running=True

def user_key_callback(key): #switching scaling modes
    global ii, hreal, mode, t0, iter
    if key==pygame.K_0: mode, ii, hreal="0", list(range(NUM_VALS)), 40000
    if key==pygame.K_1: mode, ii, hreal="1", ii1, hreal1
    elif key==pygame.K_2: mode, ii, hreal="2", ii2, hreal2
    elif key==pygame.K_s:
        with open("data.txt", "w") as f:
            ll=[]
            for t,vv in all_data:
                vv_=[f"{v:.2f}" for v in vv]
                ll.append(f"{t:.3f}, {', '.join(vv_)}\n")
            f.writelines(ll)
    elif key==pygame.K_c:
        all_data.clear()
        t0=time.time()
        iter=0

user_key_callback(pygame.K_0)

def user_exit_callback():
    global running
    running=False

real_time_plotter.user_key_callback=user_key_callback
real_time_plotter.user_exit_callback=user_exit_callback

# --- Real-time Plotting Loop ---
iter=0
t0 = time.time()
all_data=[]

while running:
    try:
        # Read and parse data from HTTP
        data_str = get_vals()
        ss=data_str.split(", ")
        if len(ss)!=len(datas): continue
        vals = [float(s) for s in ss]

        t=time.time()-t0
        all_data.append([t, vals])
        print(vals)
        # Update data for plot
        with lock:
            real_time_plotter.hreal=hreal
            real_time_plotter.info=f"Iter = {iter}, mode = {mode}"
            real_time_plotter.clear_plots()
            for i, (d, v) in enumerate(zip(datas, vals)):
                if not i in ii: continue
                d.add_val(t, v)
                real_time_plotter.add_plot(d.get_x_inds(), d.y_data)
        iter+=1

    except:
        print("Error while reading serial data")

