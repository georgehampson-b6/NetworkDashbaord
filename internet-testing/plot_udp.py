import pandas as pd
import matplotlib.pyplot as plt


def plot_iperf_udp_results(iperf_data, desired_bitrate_mbps, numCams):
    timestamps = []
    bandwidths_mbps = []
    lost_percentages = []

    # Assume the lost percentages are collected for each stream in the 'end' section
    end_streams = iperf_data['end']['streams']

    # Collect the lost percentages for each stream
    for stream in end_streams:
        udp_summary = stream['udp']
        lost_percentages.append(udp_summary['lost_percent'])

    for interval in iperf_data['intervals']:
        interval_bandwidths_mbps = []
        for stream in interval['streams']:
            bandwidth_mbps = stream['bits_per_second'] / 1e6
            interval_bandwidths_mbps.append(bandwidth_mbps)
        avg_bandwidth_mbps = sum(interval_bandwidths_mbps) / len(interval_bandwidths_mbps)
        timestamps.append((interval['sum']['start'] + interval['sum']['end']) / 2)
        bandwidths_mbps.append(avg_bandwidth_mbps)

    df_intervals = pd.DataFrame({
        'Timestamp': timestamps,
        'Average Bandwidth (Mbps)': bandwidths_mbps,
    })

    fig, axs = plt.subplots(2, 1, figsize=(10, 15))

    axs[0].plot(df_intervals['Timestamp'], df_intervals['Average Bandwidth (Mbps)'],
                marker='o', linestyle='-', color='blue', label='Actual Bandwidth Over Time')
    axs[0].axhline(y=desired_bitrate_mbps, color='r', linestyle='--', label='Desired Bandwidth per Cam')
    axs[0].fill_between(df_intervals['Timestamp'], desired_bitrate_mbps, df_intervals['Average Bandwidth (Mbps)'],
                        where=(df_intervals['Average Bandwidth (Mbps)'] < desired_bitrate_mbps),
                        color='red', alpha=0.3, interpolate=True)
    axs[0].set_title('Average Bandwidth Over Time per ' + str(numCams) + ' Streams - ' + 'UDP iPerf')
    axs[0].set_xlabel('Time (seconds)')
    axs[0].set_ylabel('Average Bandwidth (Mbps)')
    axs[0].legend()
    axs[0].grid(True)

    bars = axs[1].bar(range(len(lost_percentages)), lost_percentages, color='orange', label='Lost Percentage')
    axs[1].set_title('Lost Percentage per Stream')
    axs[1].set_xlabel('Stream ID')
    axs[1].set_ylabel('Lost Percentage (%)')

    for bar in bars:
        height = bar.get_height()
        axs[1].text(bar.get_x() + bar.get_width() / 2., 1.05*height, f'{height:.2f}%', ha='center', va='bottom')


    axs[1].legend()
    axs[1].set_ylim(top=100)
    axs[1].grid(True)

    plt.tight_layout()

    return fig