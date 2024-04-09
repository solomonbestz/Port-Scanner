import socket
import threading

from queue import Queue


class Scanner:
    def __init__(self, website):
        self.website = website
        self.open_ports = []
        self.port_list = range(1, 1024)
        self.queue = Queue()
        self.fill_queue()

    def get_ip(self) -> None:
        try:
            return socket.gethostbyname(self.website)
        except:
            return "Incorrect Website / Ip Not Found"
        
    def scan_port(self, port: int) -> bool:
        try:
            target = self.get_ip()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            return True
        except Exception as e:
            print(e)
            return False

    def fill_queue(self) -> None:
        for port in self.port_list:
            self.queue.put(port)

    def worker(self) -> None:
        while not self.queue.empty():
            port = self.queue.get()
            if self.scan_port(port):
                print(f"{port} is Open")
                self.open_ports.append(port)
            
    def scan(self) -> None:
        self.thread_list = []
        for n in range(100):
            thread = threading.Thread(target=self.worker)
            self.thread_list.append(thread)
        
        for thread in self.thread_list:
            thread.start()
        
        for thread in self.thread_list:
            thread.join()

        print(f"Open Port Are: {self.open_ports}")
        

if __name__=='__main__':
    scanner = Scanner(input("Enter Website Address: "))
    scanner.scan()