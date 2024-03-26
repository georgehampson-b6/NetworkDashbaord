import streamlit as st
import subprocess

# Define a function to perform the trace
def trace_ip(ip_address):
    with subprocess.Popen(['tracert', ip_address], stdout=subprocess.PIPE, bufsize=1, text=True, universal_newlines=True) as proc:
        for line in proc.stdout:
            st.text(line)  # Use Streamlit's text function to print the line to the app

# Create a simple form
st.title('IP Address Tracer')
ip_address = st.text_input("Enter your IP Address to trace:")

# When the button is pressed, perform the trace
if st.button('Trace IP'):
    if ip_address:  # Check if an IP address has been entered
        trace_ip(ip_address)
    else:
        st.warning('Please enter a valid IP address.')
