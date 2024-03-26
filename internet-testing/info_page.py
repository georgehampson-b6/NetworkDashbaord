import streamlit as st

def info_page():
    st.title('Internet Testing Tools Explained')

    st.header('iPerf Testing')
    st.markdown("""
- **When to Use It:** To measure the maximum bandwidth of your network, especially useful for performance testing between two points.
- **What It Does:** Measures the maximum network bandwidth capacity.
- **How It Does It:** Think of the network as a highway, and data packets as cars. iPerf sends cars from one city to another and measures how many cars can reach their destination in a given time. This tells us how wide the highway is.
    """)

    st.header('Speed Testing')
    st.markdown("""
- **When to Use It:** To check the speed of your internet connection.
- **What It Does:** Provides insights into your internet connection's download and upload speeds.
- **How It Does It:** Like timing how fast a letter travels from you to a friend and back. The test sends a small note to a server and measures how quickly it gets there and returns.
    """)

    st.header('Traceroute Testing')
    st.markdown("""
- **When to Use It:** To diagnose routing problems and understand the path your internet traffic takes.
- **What It Does:** Identifies the journey of your data across the internet.
- **How It Does It:** Imagine your internet data as a package being passed through several post offices before reaching its destination. Traceroute shows you every post office on the way.
    """)

    st.header('Nmap Testing')
    st.markdown("""
- **When to Use It:** To map network devices and identify potential security risks.
- **What It Does:** Scans for devices and services on a network, assessing security levels.
- **How It Does It:** Like sending a detective to find out who lives in a neighborhood, what cars they drive, and if their doors are locked.
    """)

