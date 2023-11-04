#!/usr/bin/env python3

FLAG = open("echo.flag", "r").readline().strip()

msg = input("Message to echo: ")
print(msg.format(FLAG))
