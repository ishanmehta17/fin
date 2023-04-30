import requests
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

matplotlib.use('Qt5Agg')  # Set the backend to Qt5Agg


# Alpha Vantage API key
api_key = 'XXXXXXXXX'

# stock symbol
symbol = 'MSFT'

# retrieve earnings per share data
url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}'
response = requests.get(url)
data = json.loads(response.text)
print(data)

# extract earnings per share values
reported_eps_values = []
estimated_eps_values = []
reported_date = []
for item in data['quarterlyEarnings']:
    if item["reportedEPS"] == "None":
        reported_eps_values.append(0)
    else:
        reported_eps_values.append(float(item["reportedEPS"]))
    if item["estimatedEPS"] == "None":
        estimated_eps_values.append(0)
    else:
        estimated_eps_values.append(float(item["estimatedEPS"]))
    reported_date.append(item["reportedDate"])

reported_eps_values.reverse()
estimated_eps_values.reverse()
reported_date.reverse()

# plot smooth curve
x_reported_eps_values = np.arange(len(reported_eps_values))
x_estimated_eps_values = np.arange(len(estimated_eps_values))
x_reported_date = np.array(reported_date)

tick_locations = np.arange(len(x_reported_date))
tick_labels = x_reported_date

spline = make_interp_spline(x_reported_eps_values, reported_eps_values)
x_smooth = np.linspace(x_reported_eps_values.min(), x_reported_eps_values.max(), 1000)
y_smooth = spline(x_smooth)

spline = make_interp_spline(x_estimated_eps_values, estimated_eps_values)
x_smooth_est = np.linspace(x_estimated_eps_values.min(), x_estimated_eps_values.max(), 1000)
y_smooth_est = spline(x_smooth_est)

fig, ax = plt.subplots()
ax.plot(x_reported_eps_values, reported_eps_values, 'o', label='Original data')
ax.plot(x_estimated_eps_values, estimated_eps_values, '*', label='Estimated data')
ax.plot(x_smooth, y_smooth, '-', color='blue')
ax.plot(x_smooth_est, y_smooth_est, '-', color='green')
ax.plot(np.unique(x_reported_eps_values), np.poly1d(np.polyfit(x_reported_eps_values, reported_eps_values, 3))(np.unique(x_reported_eps_values)), color='red')
plt.xlabel('Years')
plt.ylabel('Earnings Per Share')
plt.title(f'Earnings Per Share for {symbol}')

ax.set_xticks(tick_locations)
ax.set_xticklabels(tick_labels, rotation=90)

plt.show()
