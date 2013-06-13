import operator
import sys,os

class Encrypt():
 def xor(self, password,encrypt=True):
    key=self.mix_mac()
    if not encrypt:
      key+='\x00'
    p_sira = -1
    encrypted = ""
    for str_sira in range(len(key)):
       p_sira += 1
       if (p_sira >= len(password)): p_sira = 0
       p = str(password[p_sira])
       s = str(key[str_sira])
       e = chr ( operator.xor(ord(s), ord(p)))
       encrypted += e
    if encrypt:
      encrypted += str(len(password))
    return encrypted

 def decrypt(self,enc):
    enc_len=int(enc[len(enc)-1])
    return enc[:enc_len]

 def mix_mac(self):
    mac=self.getMacAddress()
    KEY='pythontr'
    mixed_mac=''
    str_mac=str(mac)
  
    for i in range(len(KEY)):
       mixed_mac+=str_mac[i]+KEY[i]
       mixed_mac+=str_mac[len(KEY):]
    return mixed_mac
 
 def getMacAddress(self):
    if sys.platform == 'win32':
       for line in os.popen("ipconfig /all"):
           if line.lstrip().startswith('Physical Address'):
              mac = line.split(':')[1].strip().replace('-',':')
              break
    else:
       for line in os.popen("/sbin/ifconfig"):
          if line.find('Ether') > -1:
             mac = line.split()[4]
             break
    return mac