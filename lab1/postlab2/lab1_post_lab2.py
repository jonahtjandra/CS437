from sense_hat import SenseHat
import time
import numpy as np
import matplotlib.pyplot as plt

sense = SenseHat()
sense.clear()
temp_data = []

AVG_INTERVAL = 5 # unit: data points, doubles (forward and backward)
INTERVAL = 0.1
while True:
    temp_data.append(sense.get_temperature())
    time.sleep(INTERVAL)
    print(f'collecting: {len(temp_data)}')
    if len(temp_data) > 100:
        break
new_temp_data = []
for i in range(len(temp_data)):
    z1 = i+AVG_INTERVAL - len(temp_data)
    z1 = z1 if z1 >= 0 else 0
    z2 = i-AVG_INTERVAL
    z2 = z2 if z2 < 0 else 0
    if z2:
        new_temp_data.append(np.average(temp_data[0:i+AVG_INTERVAL+z2+1]))
    elif z1:
        new_temp_data.append(np.average(temp_data[i-AVG_INTERVAL+z1:len(temp_data)]))
    else:
        new_temp_data.append(np.average(temp_data[i-AVG_INTERVAL:i+AVG_INTERVAL+1]))
    
plt.plot(np.array(temp_data), label="raw")
plt.plot(np.array(new_temp_data), label="average")
plt.legend()
plt.show()