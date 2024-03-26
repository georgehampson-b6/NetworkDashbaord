import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def parse_iperf_tcp_results(json_data):
    # Extract interval data for average bandwidth over time
    interval_times = [interval['sum']['start'] for interval in json_data['intervals']]

    # Prepare a dictionary to hold the bandwidths of each stream
    stream_bandwidths = {}
    average_bandwidths = []

    # Iterate over each interval
    for interval in json_data['intervals']:
        interval_stream_bandwidths = []

        # Iterate over each stream within the interval
        for stream in interval['streams']:
            # Convert bits per second to Mbps for each stream
            stream_bandwidth = stream['bits_per_second'] / 1e6
            socket = stream['socket']

            # Add the stream bandwidth to the list for this interval
            interval_stream_bandwidths.append(stream_bandwidth)

            # If this stream is not yet in the dictionary, add it
            if socket not in stream_bandwidths:
                stream_bandwidths[socket] = []

            # Append the bandwidth to this stream's list
            stream_bandwidths[socket].append(stream_bandwidth)

        # Calculate the average bandwidth for this interval
        average_bandwidth = sum(interval_stream_bandwidths) / len(interval_stream_bandwidths)
        average_bandwidths.append(average_bandwidth)

    # Extract end data for total sent and received bandwidth
    streams_end_data = json_data['end']['streams']
    sent_bandwidths = {stream['sender']['socket']: stream['sender']['bits_per_second'] / 1e6 for stream in streams_end_data}
    received_bandwidths = {stream['receiver']['socket']: stream['receiver']['bits_per_second'] / 1e6 for stream in streams_end_data}

    return interval_times, stream_bandwidths, average_bandwidths, sent_bandwidths, received_bandwidths




# Function to plot the data
def plot_iperf_tcp_results(interval_times, stream_bandwidths, average_bandwidths, sent_bandwidths, received_bandwidths, desired_bandwidth, numCams):
    fig, axs = plt.subplots(2, figsize=(10, 10))
    red_patch = mpatches.Patch(color='red', alpha=0.3, label='Average Below Total Desired Bandwidth')

    # Subplot 1: Individual and Average Bandwidth per Stream Over Time
    for index, (socket, bandwidths) in enumerate(stream_bandwidths.items()):
        if index == 0:
            # Label only the first stream in the legend
            axs[0].plot(interval_times, bandwidths, marker='o', linestyle='-', label=f"Individual Streams' Bandwidths", linewidth=0.5)
        else:
            # Do not label the other streams
            axs[0].plot(interval_times, bandwidths, marker='o', linestyle='-', linewidth=0.5)

    axs[0].plot(interval_times, average_bandwidths, marker='o', linestyle='-', linewidth=3, color='b', label='Average Bandwidth')
    axs[0].set_xlim(left=0)
    axs[0].axhline(y=desired_bandwidth, color='r', linestyle='--', label='Desired Bandwidth')
    axs[0].fill_between(interval_times, average_bandwidths, desired_bandwidth, where=[bw < desired_bandwidth for bw in average_bandwidths], color='red', alpha=0.3, interpolate=True)
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Bandwidth (Mbps)')
    axs[0].set_title('Bandwidth Over Time per Stream - TCP iPerf')
    handles, labels = axs[0].get_legend_handles_labels()
    handles.append(red_patch)
    axs[0].legend(handles=handles)
    axs[0].grid(True)
    axs[0].set_ylim(bottom=0)

    
    # Subplot 2: Sent and Received Bandwidth vs Stream
    # Get common stream IDs and sort them
    stream_ids = sorted(set(sent_bandwidths) | set(received_bandwidths))
    sent_values = [sent_bandwidths.get(stream_id) for stream_id in stream_ids]
    received_values = [received_bandwidths.get(stream_id) for stream_id in stream_ids]

    bar_width = 0.35
    indices = np.arange(1, len(sent_bandwidths) + 1)
    sent_values = [sent_bandwidths[stream_id] for stream_id in sorted(sent_bandwidths.keys())]
    received_values = [received_bandwidths[stream_id] for stream_id in sorted(received_bandwidths.keys())]
    
    axs[1].bar(indices - bar_width/2, sent_values, width=bar_width, label='Sent Bandwidth')
    axs[1].bar(indices + bar_width/2, received_values, width=bar_width, label='Received Bandwidth')
    axs[1].axhline(y=desired_bandwidth, color='r', linestyle='--', label='Desired Bandwidth')
    axs[1].set_xticks(indices)
    axs[1].set_ylim(bottom=0)
    axs[1].set_xlabel('Stream')
    axs[1].set_ylabel('Bandwidth (Mbps)')
    handles, labels = axs[1].get_legend_handles_labels()
    axs[1].legend(handles=handles)
    axs[1].grid(True)
    # Rest of subplot 2 remains unchanged

    # Update legend and layout adjustments as necessary
    plt.tight_layout()
    return fig