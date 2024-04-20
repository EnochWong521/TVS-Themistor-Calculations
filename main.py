import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# csv file of temperature vs. resistance from the manufacturer of the TVS transistor
tvs_data = pd.read_csv("calcResult.csv", delimiter=';')
temp = tvs_data["T[C]"].to_list()
resistance = tvs_data["R nom[Ohm]"].to_list()

# find voltage across the ADC reader
voltage = [(r / (10000 + r)) * 5 for r in resistance]

# convert voltage to adc value
adc_const = 5.0 / int(str(780000), 16)
adc = [x / adc_const for x in voltage]

plt.figure()
plt.plot(adc, temp)
plt.title("Temperature vs. ADC fitted graph")
plt.xlabel("ADC")
plt.ylabel("Temperature")
plt.show()

# shift adc to start at 0
shifted_adc = [a - adc[-1] for a in adc]

adc_fit = np.polynomial.polynomial.Polynomial.fit(shifted_adc, temp, 7)

plt.figure()
# plot the original ocv graph
plt.plot(shifted_adc, temp, label="Original graph")
# plot the fitted ocv graph
plt.plot(shifted_adc, adc_fit(np.array(shifted_adc)), label="Fitted graph")
plt.legend(loc="upper right")
plt.title("Temperature vs. Shifted fitted graph")
plt.xlabel("ADC")
plt.ylabel("Temperature")
plt.show()

step_size = int((adc[0] - adc[-1]) / 1023)
final_adc = [i for i in range(int(shifted_adc[0]), int(shifted_adc[-1]), -1 * step_size)]
final_temp = [adc_fit(a) for a in final_adc]

plt.figure()
plt.plot(final_adc, final_temp)
plt.title("Temperature vs. ADC graph (final)")
plt.xlabel("ADC")
plt.ylabel("Temperature")
plt.show()

print(len(final_adc))
print(final_adc)
print(final_temp)

data = {
    "ADC": final_adc,
    "Temperature (C)": final_temp
}

df = pd.DataFrame(data)

df.to_csv("adc_to_temp_table", index=False)
