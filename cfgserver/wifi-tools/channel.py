import getpass
import telnetlib

HOST = "172.16.95.49"
# user = input("Enter your remote account: ")
user = "admin"
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)
# tn.set_debuglevel(255)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.read_until(b" #")

tn.write(b"config wireless-controller wtp-profile\n")
tn.read_until(b"(wtp-profile)")

tn.write(b"edit FP320C\n")
tn.read_until(b"(FP320C)")

tn.write(b"set ap-country AL\n")
tn.read_until(b"Do you want to continue? (y/n)")
tn.write(b"y\n")

tn.write(b"config radio-2\n")
tn.write(b"set channel ?\n")

tn.write(b"end\n")

print(tn.read_until(b"# end"))