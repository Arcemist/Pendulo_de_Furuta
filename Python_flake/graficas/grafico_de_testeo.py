import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pd.plotting.register_matplotlib_converters()
datos = pd.read_csv("arduino_data.csv", parse_dates=["Timestamp"])

plt.figure(dpi=100)
plt.plot("Timestamp", "Pendulo", data=datos )

plt.show()
