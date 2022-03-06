import subprocess, json

out = subprocess.getoutput("PowerShell -Command \"& {Get-PnpDevice | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
j = json.loads(out)
for dev in j:
    print(dev['Status'], dev['Class'], dev['FriendlyName'], dev['InstanceId'] )

# import win32com.client
# def get_usb_device():
#     try:
#         usb_list = []
#         wmi = win32com.client.GetObject("winmgmts:")
#         for usb in wmi.InstancesOf("Win32_USBHub"):
#             print(usb.DeviceID)
#             print(usb.description)
#             usb_list.append(usb.description)

#         print(usb_list)
#         return usb_list
#     except Exception as error:
#         print('error', error)


# get_usb_device()

# import devcon_win
# import pprint

# pprint.pprint(dir(devcon_win))
# print("====================")
# pprint.pprint(dir(devcon_win.subprocess))
# print("====================")
# pprint.pprint(dir(devcon_win.subprocess.io))
# print("====================")
# pprint.pprint(dir(devcon_win.inspect))
# pprint.pprint(dir(devcon_win.hwids))

# # # Fetches the list of all usb devices:
# # result = devcon_win.subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True)

# # print(result)
# # # ... add code to parse the result and get the hwid of the device you want ...

# # # subprocess.run(['devcon', 'disable', parsed_hwid]) # to disable
# # # subprocess.run(['devcon', 'enable', parsed_hwid]) # to enable