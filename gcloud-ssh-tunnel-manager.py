import subprocess
from threading import Thread


def tunnel(name, zone, port):
    print(
        subprocess.run(["gcloud", "compute", "ssh", name, "--zone", zone, "--", "-N", "-L", f"{port}:localhost:{port}"],
                       stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

class GCloudSSHTunnelManager:
    def __init__(self):
        pass

    def start_tunnel(self, name, zone, port):
        t = Thread(target=tunnel, args=(name, zone, port))
        t.start()


if __name__ == '__main__':
    gcm = GCloudSSHTunnelManager()
    gcm.start_tunnel("jenkins-master", "europe-west10-a", 8080)
    gcm.start_tunnel("jenkins-master", "europe-west10-a", 8081)
