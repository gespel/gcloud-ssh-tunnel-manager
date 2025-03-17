import subprocess
import yaml
import pprint
import tkinter as tk
from functools import partial
from tkinter import ttk
from threading import Thread


def tunnel(name, zone, local_port, remote_port):
    exec_string = f"gcloud compute ssh {name} --zone {zone} -- -N -L {local_port}:localhost:{remote_port}"
    #print(exec_string)
    #print(subprocess.run(["gcloud", "compute", "ssh", name, "--zone", zone, "--", "-N", "-L", f"{local_port}:localhost:{remote_port}"], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))
    print(subprocess.run([exec_string], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))
class GCloudSSHTunnelManager:
    def __init__(self, name, zone):
        self.zone = zone
        self.name = name

    def start_tunnel(self, local_port, remote_port):
        t = Thread(target=tunnel, args=(self.name, self.zone, local_port, remote_port))
        t.start()

if __name__ == '__main__':
    with open("backends.yaml", "r") as f:
        config = yaml.safe_load(f)
        for server in config["backends"]:
            name = server["name"]
            zone = server["zone"]
            ports = server["ports"]
            gcm = GCloudSSHTunnelManager(name, zone)
            for port in ports:
                local_port = port["local_port"]
                remote_port = port["remote_port"]
                gcm.start_tunnel(local_port, remote_port)
