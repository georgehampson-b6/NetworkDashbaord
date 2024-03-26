import yaml
import os
from kubernetes import client, config

def load_kube_config(config_path, cluster_name):
    with open(config_path, 'r') as file:
        kube_config = yaml.safe_load(file)

    # Find the cluster
    for cluster in kube_config['clusters']:
        if cluster_name in cluster['name']:
            # Find the corresponding context
            print(f"FOUND {cluster_name} in {cluster['name']}")

            for context in kube_config['contexts']:
                if context['context']['cluster'] == cluster['name']:
                    return context['name']
    return None

def find_pod_by_name(context_name, namespace, pod_name_contains):
    # Use the specified context
    config.load_kube_config(context=context_name)
    
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)

    for pod in pods.items:
        if pod_name_contains in pod.metadata.name:
            return pod.metadata.name  # Return the first matching pod name
    return None  # If no matching pod is found

def get_external_dns_of_pod(context_name, namespace, pod_name):
    config.load_kube_config(context=context_name)
    
    v1 = client.CoreV1Api()
    pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
    node_name = pod.spec.node_name
    print(f"Pod {pod_name} is on node {node_name}")

    node = v1.read_node(name=node_name)
    for address in node.status.addresses:
        if address.type == "ExternalDNS":
            return address.address

    return None  # If no external IP

def get_service_node_port(context_name, namespace, service_name):
    # Use the specified context
    config.load_kube_config(context=context_name)

    v1 = client.CoreV1Api()
    service = v1.read_namespaced_service(name=service_name, namespace=namespace)

    for port in service.spec.ports:
        if port.node_port:
            return port.node_port  # Return the first NodePort found

    return None  # If no NodePort is found

# # Example usage
# config_path = os.path.expanduser("~/.kube/config")  # Default kubeconfig path
# cluster_name = 'pvf-us-east-2'
# context_name = load_kube_config(config_path, cluster_name)


# if context_name:
#     namespace = 'atlanta'
#     pod_name_contains = 'iperf-server'
#     service_name = 'iperf-node-port'
#     pod_name = find_pod_by_name(context_name, namespace, pod_name_contains)
#     node_port = get_service_node_port(context_name, namespace, service_name)

#     if pod_name:
#         print(f'Found pod: {pod_name}')
#         external_dns = get_external_dns_of_pod(context_name, namespace, pod_name)
#         print(f'External DNS for pod {pod_name}: {external_dns}')
#     else:
#         print('No pod containing "iperf-server" found.')

#     if node_port:
#         print(f'NodePort for service {service_name}: {node_port}')
#     else:
#         print(f'No NodePort found for service {service_name}.')


# else:
#     print('Cluster name or context not found in config file.')

