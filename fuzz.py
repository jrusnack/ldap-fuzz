#!/usr/bin/env python


import socket, os, random, subprocess

HOST='127.0.0.1'
PORT = 389
ITERATIONS = 100000

def fuzzed_payload():
  # choose random ldap payload
  payload_file = random.choice(os.listdir("payloads"))

  # run through radamsa
  p = subprocess.Popen(['radamsa', 'payloads/%s' % payload_file], 
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  return out

def ds_alive():
  if os.system('systemctl status dirsrv.target > /dev/null'):
    return False
  else:
    return True


for n in range(ITERATIONS):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(fuzzed_payload())
  except socket.error:
    pass
  finally:
    s.close()

  if not ds_alive():
    print("DS crashed!")
    exit()

