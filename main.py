from ipaddress import ip_network
from subprocess import check_output
from threading import Thread
from queue import Queue

subnet = input("Enter subnet id\n>> ")
netmask = input("Enter subnetmask or CIDR\n>> ")

replies = []


def dispatcher():
    while True:
        item = q.get()
        ping(item)
        q.task_done()

q = Queue()

for i in range(10):
    t = Thread(target=dispatcher)
    t.daemon = True
    t.start()


def ping(ip_address):
    try:
            replies.append(str(check_output('ping ' + ip_address + ' -n 1 -w 50')).split("data:")[1]
                           .split("TTL")[0].split(" ")[2][:-1])
    except:
        return

try:
    ip_range = list(ip_network(subnet+'/'+netmask))[1:-1]
    print("Scanning", ip_network(subnet+'/'+netmask))
    for ip_address in ip_range:
        q.put(str(ip_address))

    q.join()

    print("\nReachable addresses found:")
    for reply in replies:
        print(reply)

except ValueError:
    print("Error: Invalid subnet ID or subnetmask")
