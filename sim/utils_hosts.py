import json

def return_hosts():
    with open('devices.json', 'r') as f:
        hosts = json.load(f)
    return hosts

def return_hosts_per_type(type_host):
    hosts = return_hosts()
    return [host for host in hosts if host.get('type') == type_host]

if __name__ == "__main__":
    hosts = return_hosts()
    print(hosts)
