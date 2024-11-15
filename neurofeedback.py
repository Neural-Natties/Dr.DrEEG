# -*- coding: utf-8 -*-
"""
Comprehensive Muse S Monitor
Displays EEG, PPG, Accelerometer, and Gyroscope data in real-time
"""

import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop
import utils


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


# Experimental parameters
BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = [1]

if __name__ == "__main__":
    # Connect to EEG stream
    print("Looking for an EEG stream...")
    streams = resolve_byprop("type", "EEG", timeout=2)
    if len(streams) == 0:
        raise RuntimeError("Can't find EEG stream.")

    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get stream info
    info = inlet.info()
    description = info.desc()
    fs = int(info.nominal_srate())

    # Initialize buffers
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    ppg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 5))
    acc_buffer = np.zeros((int(fs * BUFFER_LENGTH), 5))
    gyro_buffer = np.zeros((int(fs * BUFFER_LENGTH), 5))
    filter_state = None

    # Initialize band power buffer
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
    band_buffer = np.zeros((n_win_test, 4))

    # Set up plots
    plt.ion()
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(15, 12))

    times = np.zeros(int(fs * BUFFER_LENGTH))

    # EEG plot
    (eeg_plot,) = ax1.plot(times, eeg_buffer[:, 0], "-b", linewidth=1)
    ax1.set_title("Raw EEG Signal")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("EEG Amplitude")

    # Band power plot
    band_names = ["Delta", "Theta", "Alpha", "Beta"]
    bar_plot = ax2.bar(band_names, np.zeros(4))
    ax2.set_title("Band Powers")
    ax2.set_ylabel("Power")

    # PPG plot
    ppg_labels = ["PPG1", "PPG2", "PPG3", "PPG4", "PPG5"]
    ppg_plot = []
    for i in range(5):
        (line,) = ax3.plot(times, ppg_buffer[:, i], label=ppg_labels[i])
    ppg_plot.append(line)
    ax3.set_title("PPG Signals")
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("PPG Amplitude")
    ax3.legend()

    # Accelerometer plot
    acc_labels = ["ACC1", "ACC2", "ACC3", "ACC4", "ACC5"]
    acc_plot = []
    for i in range(5):
        (line,) = ax4.plot(times, acc_buffer[:, i], label=f"Acc {acc_labels[i]}")
        acc_plot.append(line)
    ax4.set_title("Accelerometer")
    ax4.set_xlabel("Time (s)")
    ax4.set_ylabel("Acceleration (g)")
    ax4.legend()

    # Gyroscope plot
    gyro_plot = []
    for i in range(3):
        (line,) = ax5.plot(times, gyro_buffer[:, i], label=f"Gyro {acc_labels[i]}")
        gyro_plot.append(line)
    ax5.set_title("Gyroscope")
    ax5.set_xlabel("Time (s)")
    ax5.set_ylabel("Angular Velocity (deg/s)")
    ax5.legend()

    fig.tight_layout()

    print("Press Ctrl-C in the console to break the while loop.")

    try:
        while True:
            # Get EEG data
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs)
            )
            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True, filter_state=filter_state
            )

            # Get additional sensor data
            ppg_data, ppg_timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs)
            )
            acc_data, acc_timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs)
            )
            gyro_data, gyro_timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs)
            )

            # Compute band powers
            data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer, np.asarray([band_powers]))
            smooth_band_powers = np.mean(band_buffer, axis=0)

            # Update plots
            times = np.linspace(0, BUFFER_LENGTH, int(fs * BUFFER_LENGTH))

            # Update EEG plot
            eeg_plot.set_ydata(eeg_buffer[:, 0])
            eeg_plot.set_xdata(times)

            # Update band power plot
            for rect, val in zip(bar_plot, smooth_band_powers):
                rect.set_height(val)

            # Update PPG plot
            if ppg_data:
                ppg_buffer = np.roll(ppg_buffer, -len(ppg_data), axis=0)
                ppg_buffer[-len(ppg_data) :] = ppg_data
                for i, line in enumerate(ppg_plot):
                    line.set_ydata(ppg_buffer[:, i])
                    line.set_xdata(times)

            # Update accelerometer plot
            if acc_data:
                acc_buffer = np.roll(acc_buffer, -len(acc_data), axis=0)
                acc_buffer[-len(acc_data) :] = acc_data
                for i, line in enumerate(acc_plot):
                    line.set_ydata(acc_buffer[:, i])
                    line.set_xdata(times)

            # Update gyroscope plot
            if gyro_data:
                gyro_buffer = np.roll(gyro_buffer, -len(gyro_data), axis=0)
                gyro_buffer[-len(gyro_data) :] = gyro_data
                for i, line in enumerate(gyro_plot):
                    line.set_ydata(gyro_buffer[:, i])
                    line.set_xdata(times)

            # Update plot limits
            for ax in [ax1, ax2, ax3, ax4, ax5]:
                ax.relim()
                ax.autoscale_view()

            plt.pause(0.1)

            # Print metrics
            print(
                f"Delta: {band_powers[Band.Delta]:.4f} Theta: {band_powers[Band.Theta]:.4f}"
            )
            print(
                f"Alpha: {band_powers[Band.Alpha]:.4f} Beta: {band_powers[Band.Beta]:.4f}"
            )

            # Compute neurofeedback metrics
            alpha_metric = (
                smooth_band_powers[Band.Alpha] / smooth_band_powers[Band.Delta]
            )
            beta_metric = smooth_band_powers[Band.Beta] / smooth_band_powers[Band.Theta]
            theta_metric = (
                smooth_band_powers[Band.Theta] / smooth_band_powers[Band.Alpha]
            )

            print(f"Alpha Relaxation: {alpha_metric:.4f}")
            print(f"Beta Concentration: {beta_metric:.4f}")
            print(f"Theta Relaxation: {theta_metric:.4f}")

            if ppg_data:
                print(f"PPG Values: {np.mean(ppg_buffer[-len(ppg_data):], axis=0)}")
            if acc_data:
                print(f"Accelerometer: {np.mean(acc_buffer[-len(acc_data):], axis=0)}")
            if gyro_data:
                print(f"Gyroscope: {np.mean(gyro_buffer[-len(gyro_data):], axis=0)}")
            print("\n")

    except KeyboardInterrupt:
        print("Closing!")
        plt.close("all")
