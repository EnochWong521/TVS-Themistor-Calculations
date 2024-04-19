import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# csv file of temperature vs. resistance from the manufacturer of the TVS transistor
tvs_data = pd.read_csv("calcResult.csv", delimiter=';')
temp = tvs_data["T[C]"].to_list()
resistance = tvs_data["R nom[Ohm]"].to_list()

# polynomial fit for temperature vs. resistance
tvs_fit = np.polynomial.polynomial.Polynomial.fit(temp, resistance, 7)
new_temp_list = [x / 4 for x in range(0, 500)]
new_resistance_list = [tvs_fit(t) for t in new_temp_list]

# find voltage across the ADC reader
voltage = [(r / (10000 + r)) * 5 for r in new_resistance_list]

# convert voltage to adc value
adc_const = 5.0 / int(str(780000), 16)
adc = [x / adc_const for x in voltage]

shifted_adc = [x - adc[-1] for x in adc]

temp_fit = np.polynomial.polynomial.Polynomial.fit(shifted_adc, new_temp_list, 3)

step_size = int(pow(2, 23) / 124)
new_adc = [shifted_adc[i] for i in range(0, len(shifted_adc) - 1, step_size)]
new_temp = [temp_fit(adc) for adc in new_adc]

print(len(shifted_adc))
print(new_adc)
print(new_temp)

# plot graph for visualization
'''plt.figure()
plt.plot(shifted_adc, new_temp_list)
plt.title("Temperature graph")
plt.show()'''
