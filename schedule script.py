from datetime import datetime, timedelta

# Start time and end time
start_time = datetime(2024, 10, 11, 14, 50)  # Starting at 2:50 PM EST today
end_time = datetime(2024, 10, 15, 17, 0)     # Ending at 5:00 PM EST Tuesday

# Parameters that stay the same across all observations
channels = 300
offset = 175
colorgain = 1.0
observation_duration = timedelta(minutes=5)
pause_between_observations = timedelta(seconds=10)

# Maximum frequency for RSP1A
max_hif = 2000000000  # 2 GHz
min_lof = 1000000000  # 1 GHz

# Generate file
with open("rss_schedule_1ghz.skd", "w") as f:
    # Add the 'daily' keyword
    f.write("daily\n")

    current_time = start_time
    lof = 1000000000  # Starting lowest frequency in Hz (1 gHz)
    hif = lof + 10000000   # Starting highest frequency in Hz (1.001 Ghz)

    while current_time < end_time:
        stop_time = current_time + observation_duration

        f.write(f"start={current_time.strftime('%H:%M:%S')};\n")
        f.write(f"channels={channels};\n")
        f.write(f"offset={offset};\n")
        f.write(f"colorgain={colorgain};\n")
        f.write(f"LOF={lof};\n")
        f.write(f"HIF={hif};\n")
        f.write(f"stop={stop_time.strftime('%H:%M:%S')};\n")
        #f.write("\n")  # Add a newline between observations

        # Update times and frequencies for the next observation
        current_time = stop_time + pause_between_observations
        lof += 10000000  # Increase LOF by 10 MHz
        hif += 10000000  # Increase HIF by 10 MHz

        # Reset frequencies if HIF exceeds 2 GHz
        if hif > max_hif:
            lof = min_lof  # Reset LOF to 1 GHz
            hif = lof + 10000000  # Reset HIF to LOF + 10 MHz

print("RSS schedule file generated: rss_schedule.skd")
