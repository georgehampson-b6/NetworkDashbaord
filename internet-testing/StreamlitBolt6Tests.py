import json
import os
import streamlit as st
import subprocess
import threading
import time
import pandas as pd
import pandas as pd
import ipaddress
from info_page import *
from plot_udp import *
from plot_tcp import *
from plot_tcp import *
from nmap_test import *
from kubernetes_test import *

# Need to install nmap and also import nmap after finished

# Ensure the Results directory exists
os.makedirs("Results", exist_ok=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Info","iPerf Testing","Speed Testing","Trace Route Testing","Nmap Testing"])



# Function to run iperf command in a separate thread
def run_iperf_command(iperf_command, filename):
    with open(filename, "w") as file:
        process = subprocess.Popen(iperf_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            file.write(line)
            file.flush()

def user_inputs():
    # User inputs for `iperf` command
    st.title("iPerf Testing")
    with st.popover("Clear iPerf Results Folder"):
        if st.button("Are you Sure?"):
            folder_path = "Results"
            # Loop through each item in the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):  # Ensure it's a file or a symlink to a file
                        os.remove(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            st.markdown("Folder Cleared!")
            

    st.subheader('Protocol and Output Options')
    col1, col2 = st.columns(2)
    with col1:
        protocol = st.selectbox("Test TCP or UDP:", ["TCP", "UDP"])
    with col2:
        outputFormat = st.radio("Enter the Output Format of your Tests:", ["JSON + Plotting", "Text File"])

    st.divider()
    st.subheader('Server Options')
    st.markdown("**Would you like to auto-Scan your Kubernetes Config File to get IP and Port Details?**")
    auto_scan = st.toggle('Auto-Scan On')

    if auto_scan:
        st.markdown("Note: Make sure you've started your cluster!")
        # server_ip = st.text_input("Enter Server IP:")
        # port = st.number_input("Enter Port i.e. 5201:", step=1)
        cluster_name = st.text_input("Enter Your Cluster Name (i.e. pvf-us-east-2):")
        namespace = st.text_input("Enter your namespace:")
        external_dns_input = None
        port_input = None
    
    else:
        cluster_name = None
        namespace = None
        external_dns_input = st.text_input("Enter the External DNS of the node your iperf-server pod is running on (i.e.  ec2-3-137-180-100.us-east-2.compute.amazonaws.com):")
        port_input = st.text_input("Enter the NodePort of your iperf-server Service (i.e. 30565):")
        

    st.divider()
    st.subheader('Test Options')
    test_duration = st.number_input("Enter Test Duration in seconds (i.e. 60):", value=60, step=1)
    numCams = st.number_input("Enter the number of simulated camera (i.e. 12):", value=12, step=1)
    bitrate = st.number_input("Enter the bitrate of each simulated camera in Mbps (i.e. 15):", value=15, step=1)
    interval = st.number_input("Enter the interval in which to report data in seconds (i.e. 1):", value=1, step=1)

    st.divider()

    return(external_dns_input, port_input, cluster_name,namespace,protocol, outputFormat, test_duration, numCams, bitrate, interval)

def iperf_command_generator(protocol,numCams,bitrate,test_duration,server_ip, port, namespace):
        
        # Start iperf command in a separate 
        protocol_option = "-u" if protocol == "UDP" else ""
        if outputFormat == "JSON + Plotting":
            outputFormat_option = "-J"
            filename = f"Results/{namespace}_iPerf_{protocol}_TEST_{numCams}Cams_{bitrate}Mbps_{test_duration}sec.json"
        else:
            outputFormat_option = ""
            filename = f"Results/{namespace}_iPerf_{protocol}_TEST_{numCams}Cams_{bitrate}Mbps_{test_duration}sec.txt"

        iperf_command = f"iperf3 -c {server_ip} -p {port} {protocol_option} -t {test_duration} -b {bitrate}M -P {numCams} -i {interval} {outputFormat_option}"

        with st.expander("Command Line script for your reference if needed"):
            st.code(body=iperf_command,language = "batch")
        
        ui_text = f"Running {protocol} iperf Test. Simulating {numCams} CCams uploading data at {bitrate} Mbps. The test will run for {test_duration} seconds and will output the results as {outputFormat}."
        st.markdown(ui_text)
        st.divider()

        return(filename, iperf_command)


def generate_progress_bar(test_duration):
    # Initialize progress bar and time left text
    my_bar = st.progress(0)
    time_left_text = st.empty()  # Create an empty placeholder for the time left text

    # Create a placeholder for the cancel button
    cancel_button_container = st.empty()

    # Add a cancel button and store its return value in a variable
    cancel = cancel_button_container.button("Cancel Test")

    # Use a control variable to determine when the test is running
    test_running = True

    # Update progress bar and time left based on the duration of the test
    for second in range(test_duration):
        # Check if the cancel button was pressed
        if cancel:
            test_running = False
            st.stop()

        # Only execute the loop if the test is still running
        if test_running:
            time.sleep(1)  # Sleep for 1 second
            progress = int((second + 1) / test_duration * 100)
            my_bar.progress(progress)

            # Calculate and display the time left
            time_left = test_duration - (second + 1)
            time_left_text.text(f"Time left: {time_left} seconds")

    if test_running:
        # Final update to ensure progress bar reaches 100% and clear the time left text
        my_bar.progress(100)
        time.sleep(1)  # Ensure final progress and message are visible
        my_bar.empty()
        time_left_text.empty()  # Clear the time left text
        cancel_button_container.empty()  # Clear the cancel button


# Define a function to perform the trace
def trace_ip(ip_address):
    with subprocess.Popen(['tracert', ip_address], stdout=subprocess.PIPE, bufsize=1, text=True, universal_newlines=True) as proc:
        if st.button("Stop Traceroute"):
            st.stop()
        with st.spinner(f"Tracing..."):
            for line in proc.stdout:
                st.text(line)  # Use Streamlit's text function to print the line to the app


def run_iperf_test(protocol, filename, outputFormat, test_duration, bitrate, numCams):

    generate_progress_bar(test_duration)
    time.sleep(1.5)

    with st.expander("See Results"):

        # Display a button to download the result file and other related code...

        # Display a button to download the result file
        with open(filename, "rb") as file:
                # Extracting streams data
            
            st.download_button(
                label="Download "+protocol+" iperf Test Results",
                data=file,
                file_name=os.path.basename(filename),
                mime="text/plain"
            )
            st.markdown('WARNING: Once you press "Download", all plots and info displayed below will disapper!')

        match protocol:            
            case "UDP":
                match outputFormat:
                    case "JSON + Plotting":
                        try:
                            with open(filename, "r") as file:
                                udp_data = json.load(file)

                                fig = plot_iperf_udp_results(udp_data, bitrate, numCams)
                                st.pyplot(fig)


                        except json.JSONDecodeError:
                            st.error("Failed to load JSON data from the file. The file may be empty or corrupted.")

                    case "Text File":
                        
                        with open(filename, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                            # Displaying the content in the app
                            st.text(file_content)
            
            case "TCP":
                match outputFormat:
                    case "JSON + Plotting":
                        try:
                            with open(filename, "r") as file:

                                tcp_data = json.load(file)
                                interval_times, stream_bandwidths, average_bandwidths, sent_bandwidths, received_bandwidths = parse_iperf_tcp_results(tcp_data)
                                fig = plot_iperf_tcp_results(interval_times, stream_bandwidths, average_bandwidths, sent_bandwidths, received_bandwidths, bitrate, numCams)
                                st.pyplot(fig)


                        except json.JSONDecodeError:
                            st.error("Failed to load JSON data from the file. The file may be empty or corrupted.")

                    case "Text File":

                        with open(filename, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                            # Displaying the content in the app
                            st.text(file_content)
            case _:
                st.text("NONE SELECTED?")



if __name__ == "__main__":

    with tab1:
        info_page()

    with tab2:
        (external_dns_input, port_input, cluster_name, namespace, protocol, outputFormat, test_duration, numCams, bitrate, interval) = user_inputs()
        
        if st.button("Run "+protocol+" iperf Test"):
            
            if cluster_name and namespace is not None:
                st.markdown("Identifying Server Details...")
                # Set up everything so it finds the right values from your kubernets config file
                config_path = os.path.expanduser("~/.kube/config")  # Default kubeconfig path
                pod_name_contains = 'iperf-server'
                service_name = 'iperf-node-port'
                context_name = load_kube_config(config_path, cluster_name)

                if context_name:
                    pod_name = find_pod_by_name(context_name, namespace, pod_name_contains)
                    node_port = get_service_node_port(context_name, namespace, service_name)

                    with st.expander("View iPerf Server and NodePort Details"):
                        if pod_name:
                            st.markdown(f'iPerf Pod Name:   {pod_name}')
                            external_dns = get_external_dns_of_pod(context_name, namespace, pod_name)
                        else:
                            st.text('No pod containing "iperf-server" found.')
                            st.stop()

                        if node_port is not None:
                            st.markdown(f"External DNS of iPerf Server:   {external_dns}")
                            st.markdown(f"Node Port:   {node_port}")

                        else:
                            st.text(f'No NodePort found for service {service_name}.')
                            st.stop()
                else:
                    st.error('Cluster name or context not found in config file.')
                    st.stop()

            else: 
                external_dns = external_dns_input
                node_port = port_input
                namespace = ""


            st.text("")

            (filename, iperf_command) = iperf_command_generator(protocol,numCams,bitrate,test_duration,external_dns, node_port, namespace)
            threading.Thread(target=run_iperf_command, args=(iperf_command, filename)).start()

            run_iperf_test(protocol, filename, outputFormat, test_duration, bitrate, numCams)   
    

    with tab3:
        st.title("Ookla Speed Test")
        url = "https://www.speedtest.net/"
        st.markdown("check out this [link](%s)" % url)

    with tab4:
        # Create a simple form
        st.title('IP Address Tracer')
        ip_address = st.text_input("Enter your target IP Address or Hostname to trace:")

        # When the button is pressed, perform the trace
        if st.button('Trace IP'):
            if ip_address:  # Check if an IP address has been entered

                trace_ip(ip_address)

            else:
                st.error('Please enter a valid IP address.')


    with tab5:
        st.title('Nmap Scanning Tool')
        st.markdown("This tool is used to scan all the devices that might be on your network. \
                    PLEASE NOTE: Only use this tool sparingly if you suspect that there might be devices or \
                    users connected to your network who shouldn't be.")
        # Button to start the scan
        gateway = st.text_input("Enter the gateway of your network (i.e. 192.168.0.1):")
        subnet_mask = st.text_input("Enter the Subnet Mask of your network (i.e. 255.255.255.0):",value='255.255.255.0')        
        if st.button('Start Network Discovery'):   
            with st.spinner('Scanning...'):
                # Make sure to handle exceptions that may occur during scanning
                try:
                    network = ipaddress.IPv4Network(f'{gateway}/{subnet_mask}', strict=False)
                    scan_results = nmap_scan(str(network))
                    # Display the results in a table
                    st.success('Scan complete!')
                    df = pd.DataFrame(scan_results)
                    st.table(df)
                except Exception as e:
                    st.error(f'An error occurred: {e}')

