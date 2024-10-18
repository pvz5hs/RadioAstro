import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Load the CSV file
data = pd.read_csv('fwb.csv')

# Combine 'Date' and 'Time' columns into a single datetime column
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

# Generate frequency values (3rd column to the second-to-last)
frequencies = data.columns[2:-1].astype(float) /1000000

# Extract intensity values (skip the first row of data)
values = data.iloc[1:, 2:-1].to_numpy()  # This should have shape (2995, 411)

# Extract the datetime values (all rows except the first)
time_values = data['Datetime'][1:].to_numpy()  # This should have shape (2995,)

# Plot the waterfall plot

ylength = len(time_values)/374
fig, ax = plt.subplots(figsize=(12, ylength))

# Create the heatmap with `pcolormesh`
c = ax.pcolormesh(frequencies, time_values, values, cmap='viridis', shading='auto')

# Format the y-axis to display datetime values properly
ax.yaxis_date()  # Ensure the y-axis treats values as dates
ax.yaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%y %H:%M:%S'))

# Rotate x-axis labels for readability
plt.xticks(rotation=45)
plt.gcf().autofmt_xdate()

# Add a colorbar for reference
fig.colorbar(c, ax=ax, label='Intensity')

# Set axis labels and title
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Time')
ax.set_title('Waterfall Plot: Frequency vs Time')

# Show the plot
plt.show()
