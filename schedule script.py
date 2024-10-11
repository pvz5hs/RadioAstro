from datetime import datetime, timedelta

# Define start and end times
start_time = datetime(2024, 10, 11, 14, 40)  # Starting at 2:40 PM EST today
end_time = datetime(2024, 10, 15, 17, 0)     # Ending at 5:00 PM EST Tuesday

# Time increment settings
observation_duration = timedelta(minutes=5)  # 5-minute observation duration
gap_duration = timedelta(seconds=10)         # 10 seconds between observations

# Frequency and bandwidth settings (adjust these as needed)
center_frequency = "88.5 MHz"
bandwidth = "2 MHz"

# Output filename
schedule_filename = "rss_schedule_time_only.skd"

# Generate schedule entries
with open(schedule_filename, "w") as f:
    current_time = start_time
    count = 1

    while current_time <= end_time:
        observation_start = current_time.strftime("%Y-%m-%d %H:%M:%S")
        output_filename = f"test_observation_{count}.sps"

        # Write entry to the file
        f.write(f"{observation_start},{observation_duration},{output_filename}\n")

        # Move to next observation (add duration + gap)
        current_time += observation_duration + gap_duration
        count += 1

schedule_filename  # Output the filename of the generated schedule file
