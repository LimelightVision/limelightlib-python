import ipaddress
import requests
import threading
import socket
import websocket
import json
import ifaddr

def broadcast_message(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), ('255.255.255.255', port))

def broadcast_on_all_interfaces(message, port):
    for adapter in ifaddr.get_adapters():
        for ip in adapter.ips:
            if ip.is_IPv4:
                net = ipaddress.ip_network(f"{ip.ip}/{ip.network_prefix}", False)
            else:
                net = ipaddress.ip_network(f"{ip.ip[0]}/{ip.network_prefix}", False)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(message.encode(), (str(net.broadcast_address), port))

def listen_for_responses(port,timeout=1):
    discovered_devices = []
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.bind(("", port))
        sock.settimeout(timeout)
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                discovered_devices.append(addr[0])
                #print(f"Received data from {addr}: {data.decode()}")
        except socket.timeout:
            pass
    return discovered_devices

def discover_limelights(broadcast_port=5809, listen_port=5809, timeout=2):
    broadcast_on_all_interfaces("LLPhoneHome",broadcast_port)
    return listen_for_responses(listen_port,timeout)

class Limelight:
    def __init__(self, address):
        self.base_url = f"http://{address}:5807"
        self.ws_url = f"ws://{address}:5806"
        self.latest_results = None
        self.ws = None
        self.ws_thread = None

    def get_results(self):
        return requests.get(f"{self.base_url}/results").json()
        
    def capture_snapshot(self, snapname):
        headers = {'snapname': snapname}
        return requests.get(f"{self.base_url}/capturesnapshot", headers=headers).content

    def upload_snapshot(self, snapname, image_path):
        headers = {'snapname': snapname}
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            return requests.post(f"{self.base_url}/uploadsnapshot", headers=headers, files=files)

    def snapshot_manifest(self):
        return requests.get(f"{self.base_url}/snapshotmanifest").json()

    def delete_snapshots(self):
        return requests.get(f"{self.base_url}/deletesnapshots")

    def upload_neural_network(self, nn_type, file_path):
        headers = {'type': nn_type}
        with open(file_path, 'rb') as nn_file:
            files = {'file': nn_file}
            return requests.post(f"{self.base_url}/uploadnn", headers=headers, files=files)

    def hw_report(self):
        return requests.get(f"{self.base_url}/hwreport").json()

    def cal_default(self):
        return requests.get(f"{self.base_url}/cal-default").json()

    def cal_file(self):
        return requests.get(f"{self.base_url}/cal-file").json()

    def cal_eeprom(self):
        return requests.get(f"{self.base_url}/cal-eeprom").json()

    def cal_latest(self):
        return requests.get(f"{self.base_url}/cal-latest").json()

    def hwreport(self):
        return requests.get(f"{self.base_url}/hwreport").json()

    def update_cal_eeprom(self, cal_data):
        return requests.post(f"{self.base_url}/cal-eeprom", data=cal_data)

    def update_cal_file(self, cal_data):
        return requests.post(f"{self.base_url}/cal-file", data=cal_data)

    def delete_cal_latest(self):
        return requests.delete(f"{self.base_url}/cal-latest")

    def delete_cal_eeprom(self):
        return requests.delete(f"{self.base_url}/cal-eeprom")

    def delete_cal_file(self):
        return requests.delete(f"{self.base_url}/cal-file")

    def get_status(self):
        response = requests.get(f"{self.base_url}/status")
        if response.ok:
            return response.json()
        else:
            return None

    def get_name(self):
        status = self.get_status()
        if status and 'status' in status:
            return status['status'].get('name', None)
        return None

    def get_temp(self):
        status = self.get_status()
        if status and 'status' in status:
            return status['status'].get('temp', None)
        return None

    def get_fps(self):
        status = self.get_status()
        if status and 'status' in status:
            return status['status'].get('fps', None)
        return None

    def enable_websocket(self):
        def on_message(ws, message):
            self.latest_results = json.loads(message)
        def on_error(ws, error):
            print(f"WebSocket error: {error}")
        def on_close(ws):
            print("WebSocket closed")
        def run(*args):
            self.ws = websocket.WebSocketApp(self.ws_url,
                                             on_message=on_message,
                                             on_error=on_error,
                                             on_close=on_close)
            self.ws.run_forever()
        self.ws_thread = threading.Thread(target=run)
        self.ws_thread.start()

    def disable_websocket(self):
        if self.ws:
            self.ws.close()
            self.ws_thread.join()

    def get_latest_results(self):
        return self.latest_results
