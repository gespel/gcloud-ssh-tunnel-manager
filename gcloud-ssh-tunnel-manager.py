import subprocess
from threading import Thread


def tunnel(name, zone, local_port, remote_port):
    print(
        subprocess.run(["gcloud", "compute", "ssh", name, "--zone", zone, "--", "-N", "-L", f"{local_port}:localhost:{remote_port}"],
                       stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

class GCloudSSHTunnelManager:
    def __init__(self):
        pass

    def start_tunnel(self, name, zone, local_port, remote_port):
        t = Thread(target=tunnel, args=(name, zone, local_port, remote_port))
        t.start()


if __name__ == '__main__':
    gcm = GCloudSSHTunnelManager()
    gcm.start_tunnel("jenkins-master", "europe-west10-a", 8080, 8080)
    gcm.start_tunnel("jenkins-master", "europe-west10-a", 8081, 8081)
    gcm.start_tunnel("gitlab", "europe-west10-a", 8082, 80)
    gcm.start_tunnel("gitlab", "europe-west10-a", 443, 443)
