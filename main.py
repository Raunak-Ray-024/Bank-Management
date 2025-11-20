from pathlib import Path
import json
import random
import string
class Bank:
    database='database.json' #main database location
    data=[]  #this list is temporary data , 
    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("we are facing some issues")
    except Exception as err:
        print("an error occured",err)



    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data)) 
    
    @staticmethod
    def __accountno():
        alpha=random.choices(string.ascii_letters,k=5)
        digits=random.choices(string.digits,k=4)
        id=alpha+digits
        random.shuffle(id)
        return"".join(id)
    
    
    def create_acc(self):
        d={
            "name":input("enter your name"),
            "email":input("enter your email"),
            "phone_no":int(input("enter your phone number")),
            "pin":int(input("enter your 4 digit pin")),
            "Account_no":Bank.__accountno(),
            "balance":0
        }
        if len(str(d['pin']))!=4:
            print("review your pin")
        elif len(str(d['phone_no']))!=10:
            print("review your phone number")
        else:
            Bank.data.append(d)
            Bank.__update()
        
        
    def deposit_money(self):
        Account =input("Enter account number: ")
        setpin = int(input("Enter PIN: "))
        user_data=[i for i in Bank.data if i['Account_no']==Account and  i['pin']==setpin]
        
        if not user_data:
            print("Invalid PIN or account not found.")
        else:
            amount=int(input("enter amount"))
            if amount<=0:
                print("invalid")
            elif amount>10000:
                print("greater than 10000")
            else:
                user_data[0]['balance']+=amount
            Bank.__update()
            print("Amount credited")

           
    def withdraw_money(self):
        Account = input("Enter account number: ")
        setpin = int(input("Enter PIN: "))
        user_data=[i for i in Bank.data if i['Account_no']==Account and  i['pin']==setpin]
        
        if not user_data:
            print("Invalid PIN or account not found.")
        else:
            amount=int(input("enter amount"))
            if amount<=0:
                print("invalid")
            elif amount>10000:
                print("greater than 10000")
            else:
                if user_data[0]['balance']<amount:
                    print("Error")
                else:
                    user_data[0]['balance']-=amount
            
            Bank.__update()
            print("Amount debited")
    

    def details(self):
            Account = input("Enter account number: ")
            setpin =int(input("Enter PIN: "))
            user_data=[i for i in Bank.data if i['Account_no']==Account and  i['pin']==setpin]
        
            if not user_data:
                print("Invalid PIN or account not found.")
            else:
                for i in user_data[0]:
                    print(f"{i}:{user_data[0][i]}")
                print("displayed")

    def update(self):
        Accno = input("Enter account number: ")
        pin = int(input("Enter PIN: "))
        user_data=[i for i in Bank.data if i['Account_no']==Accno and  i['pin']==pin]
        if not user_data:
            print("Invalid PIN or account not found.")
        else: 
            print("you cannot change account number")
            print("now update your details and skip if you dont want to")
            new_data={
            "name":input("enter your new name"),
            "email":input("enter your new email"),
            "phone_no":input("enter your new phone number"),
            "pin":input("enter your new 4 digit pin"),
            }
            #handle the skipped value
            for i in new_data:
                if new_data[i]=="":
                    new_data[i]=user_data[0][i]
            new_data['Account_no'] = user_data[0]['Account_no']
            new_data['balance'] = user_data[0]['balance']
            # print(new_data)
            #update new data to database
            for i in user_data[0]:
                if user_data[0][i]==new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i]=int(new_data[i])
                    else:
                        user_data[0][i]=new_data[i]
            # print(user_data)
            Bank.__update()
            print("Details Updated")

    def delete(self):
        Accno = input("Enter account number: ")
        pin = int(input("Enter PIN: "))
        user_data=[i for i in Bank.data if i['Account_no']==Accno and  i['pin']==pin]
        if not user_data:
            print("Invalid PIN or account not found.")
        else:
            for i in Bank.data:
                if i['Account_no']==Accno and i['pin']==pin:
                    user_data.remove(i)
            Bank.__update()
            print("data deleted")


user=Bank()
print("press 1 to create an account")
print("press 2 to deposit money")
print("press 3 to withdraw money")
print("press 4 to get details")
print("press 5 to update details")
print("press 6 to delete account")
print("******************************************************************************************************************************************")
 
#json file containing main data is copied to temporary data and changes is made there

check=int(input("enter your choice"))
if check==1:
    user.create_acc()
if check==2:
    user.deposit_money()
if check==3:
    user.withdraw_money()
if check==4:
    user.details()
if check==5:
    user.update()
if check==6:
    user.delete()


