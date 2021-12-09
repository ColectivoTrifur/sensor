
import argparse
import math
from termcolor import colored
from pythonosc import udp_client
from pythonosc import dispatcher, osc_server
import random
import time

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

ip="127.0.0.1"
weki_port = 6448
weki_channel = "/wek/inputs"
client = udp_client.SimpleUDPClient(ip, weki_port)
def send_from_OSC_to_weki(unused_addr, args,volume,a,b,c):
    print("buena! sending to weki")
    print(args, volume,a,b,c)
    client.send_message(weki_channel, float(args))
    print(f'sent {args} to 6448')
    time.sleep(1)


if __name__ == "__main__":
  port=3333 #the port that you expose to tidal
  #receive from tidal
  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/dirt/play", send_from_OSC_to_weki)
  server = osc_server.ThreadingOSCUDPServer(
      (ip, port), dispatcher)
  print("[*] Serving on {}".format(server.server_address))
  print("Redirects to {ip}:{weki_port}/{weki_channel}")
  server.serve_forever()




