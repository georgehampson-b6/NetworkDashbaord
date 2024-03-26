import nmap

def nmap_scan(target):
    nm = nmap.PortScanner()

    # Perform a ping scan to discover hosts
    nm.scan(hosts=target, arguments='-sn')
    # Prepare the results
    results = []
    for host in nm.all_hosts():
        host_info = {
            'IP Address': nm[host]['addresses'].get('ipv4', 'N/A'),
            'MAC Address': nm[host]['addresses'].get('mac', 'N/A'),
            'Status': nm[host].state(),
            'Hostname': ', '.join([hostname['name'] for hostname in nm[host]['hostnames']]) if nm[host]['hostnames'] else 'N/A'
        }
        results.append(host_info)
    return results