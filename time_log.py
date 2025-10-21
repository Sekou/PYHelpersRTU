import time,datetime as dt
frmt_date = dt.datetime.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M")
print(frmt_date)
drone_dist, drone_cx, drone_cy, drone_angx, drone_angy = 0, 0, 0, 0, 0
frmt_date = dt.datetime.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M")
log_file=open(f"log_{frmt_date}.txt", "w")
for i in range(10):
    frmt_date = dt.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S.%f")
    log_file.write(f"{frmt_date}: d {drone_dist} x_pix {drone_cx} y_pix {drone_cy} angx {drone_angx} angy {drone_angy}\n")
    time.sleep(0.1)
log_file.close()