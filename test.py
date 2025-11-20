# l=[{'a':1,'b':2}] #iss list mei pehla element dictionary pehla hai aur uske nadar second element b ka 2 hai
# print(l[0]['b'])


data=[{"name": "Rohan", "email": "minnu@123", "phone_no": 1234567891, "pin": 1234, "Account_no": "m0KoPC668", "balance": 3500},
 {"name": "Kiran", "email": "Kiran@12345", "phone_no": 5649871234, "pin": 1597, "Account_no": "33Iow4L0K", "balance": 0},
 {"name": "Minnu", "email": "minnu@q234", "phone_no": 5467891234, "pin": 1359, "Account_no": "9r2vKNA45", "balance": 0}]

for i in data:
    if i['Account_no']=="m0KoPC668":
        data.remove(i)
print(data)