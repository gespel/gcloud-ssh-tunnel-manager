import subprocess
import tkinter as tk
from functools import partial
from tkinter import ttk
from threading import Thread


def tunnel(name, zone, local_port, remote_port):
    print(
        subprocess.run(["gcloud", "compute", "ssh", name, "--zone", zone, "--", "-N", "-L", f"{local_port}:localhost:{remote_port}"],
                       stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

class GCloudSSHTunnelManager:
    def __init__(self, name, zone):
        self.zone = zone
        self.name = name

    def start_tunnel(self, local_port, remote_port):
        t = Thread(target=tunnel, args=(self.name, self.zone, local_port, remote_port))
        t.start()


def new_tunnel_dialog(name, zone, local_port, remote_port):
    label = tk.Label(root, text=f"{name} in {zone} -> {local_port}:localhost:{remote_port}", bg="gray40", fg="white")
    label.grid(row=2 + len(labels), column=0, padx=10, pady=5)
    labels.append(label)

if __name__ == '__main__':
    gcm = GCloudSSHTunnelManager("jenkins-master", "europe-west10-a")
    #gcm.start_tunnel("jenkins-master", "europe-west10-a", 8080, 8080)
    #gcm.start_tunnel("jenkins-master", "europe-west10-a", 8081, 8081)
    #gcm.start_tunnel("gitlab", "europe-west10-a", 8082, 80)
    #gcm.start_tunnel("gitlab", "europe-west10-a", 443, 443)

    root = tk.Tk()
    name_var = tk.StringVar()
    zone_var = tk.StringVar()
    local_port_var = tk.StringVar()
    remote_port_var = tk.StringVar()
    root.resizable(False, False)
    root.minsize(400, 200)
    root.title("Tunnel Manager")
    root.config(bg="gray15")

    labels = []  # Liste zum Speichern der Labels

    tk.Label(root, text="Current Tunnels:", bg="gray15", fg="white").grid(row=0, column=0, padx=10, pady=5)

    separator = ttk.Separator(root, orient="vertical")
    separator.grid(row=0, column=1, rowspan=100, sticky="ns", padx=5)

    tk.Label(root, text="Instance name:", bg="gray15", fg="white").grid(row=0, column=2, padx=10, pady=5)
    tk.Entry(root, textvariable=name_var, bg="gray15", fg="white").grid(row=0, column=3, padx=10, pady=5)

    tk.Label(root, text="Zone:", bg="gray15", fg="white").grid(row=1, column=2, padx=10, pady=5)
    tk.Entry(root, textvariable=zone_var, bg="gray15", fg="white").grid(row=1, column=3, padx=10, pady=5)

    tk.Label(root, text="Local port:", bg="gray15", fg="white").grid(row=2, column=2, padx=10, pady=5)
    tk.Entry(root, textvariable=local_port_var, bg="gray15", fg="white").grid(row=2, column=3, padx=10, pady=5)

    tk.Label(root, text="Remote port:", bg="gray15", fg="white").grid(row=3, column=2, padx=10, pady=5)
    tk.Entry(root, textvariable=remote_port_var, bg="gray15", fg="white").grid(row=3, column=3, padx=10, pady=5)

    tk.Button(root, text="Start New Tunnel", command=lambda: new_tunnel_dialog(
        name_var.get(), zone_var.get(), local_port_var.get(), remote_port_var.get()
    )).grid(row=4, column=2, padx=10, pady=5)

    root.mainloop()

