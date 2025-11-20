import streamlit as st
from pathlib import Path
import json
import random
import string

# ------------------ ORIGINAL BANK CLASS ---------------------

class Bank:
    database='database.json'
    data=[]

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
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __accountno():
        alpha=random.choices(string.ascii_letters,k=5)
        digits=random.choices(string.digits,k=4)
        id=alpha+digits
        random.shuffle(id)
        return "".join(id)

    def create_acc(self, name, email, phone, pin):
        d={
            "name":name,
            "email":email,
            "phone_no":phone,
            "pin":pin,
            "Account_no":Bank.__accountno(),
            "balance":0
        }
        Bank.data.append(d)
        Bank.__update()
        return d["Account_no"]

    def deposit_money(self, acc, pin, amount):
        user=[i for i in Bank.data if i['Account_no']==acc and i['pin']==pin]
        if not user:
            return False, "Invalid Account or PIN"
        if amount <= 0:
            return False, "Amount must be positive"
        user[0]["balance"] += amount
        Bank.__update()
        return True, "Deposit successful"

    def withdraw_money(self, acc, pin, amount):
        user=[i for i in Bank.data if i['Account_no']==acc and i['pin']==pin]
        if not user:
            return False, "Invalid Account or PIN"
        if amount <= 0:
            return False, "Amount must be positive"
        if user[0]["balance"] < amount:
            return False, "Insufficient balance"
        user[0]["balance"] -= amount
        Bank.__update()
        return True, "Withdrawal successful"

    def get_details(self, acc, pin):
        user=[i for i in Bank.data if i['Account_no']==acc and i['pin']==pin]
        if not user:
            return None
        return user[0]

    def update(self, acc, pin, new_name, new_email, new_phone, new_pin):
        user=[i for i in Bank.data if i['Account_no']==acc and i['pin']==pin]
        if not user:
            return False

        u = user[0]
        u["name"] = new_name if new_name else u["name"]
        u["email"] = new_email if new_email else u["email"]
        u["phone_no"] = new_phone if new_phone else u["phone_no"]
        u["pin"] = new_pin if new_pin else u["pin"]

        Bank.__update()
        return True

    def delete(self, acc, pin):
        user=[i for i in Bank.data if i['Account_no']==acc and i['pin']==pin]
        if not user:
            return False
        Bank.data.remove(user[0])
        Bank.__update()
        return True

# ------------------------------------------------------------

st.title("🏦 Bank Management System")
st.write("A simple UI for your Bank class using Streamlit.")

bank = Bank()

menu = st.sidebar.selectbox(
    "Select Action",
    ["Create Account", "Deposit Money", "Withdraw Money", "Get Details", "Update Details", "Delete Account"]
)


# ------------------ CREATE ACCOUNT --------------------------
if menu == "Create Account":
    st.header("Create New Account")
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    phone = st.text_input("Enter phone number")
    pin = st.text_input("Enter 4-digit PIN")

    if st.button("Create Account"):
        if len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be 4 digits")
        elif len(phone) != 10 or not phone.isdigit():
            st.error("Phone number must be 10 digits")
        else:
            acc = bank.create_acc(name, email, int(phone), int(pin))
            st.success(f"Account created successfully! Your Account Number: {acc}")


# ------------------ DEPOSIT --------------------------
elif menu == "Deposit Money":
    st.header("Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        ok, msg = bank.deposit_money(acc, int(pin), amount)
        if ok:
            st.success(msg)
        else:
            st.error(msg)


# ------------------ WITHDRAW --------------------------
elif menu == "Withdraw Money":
    st.header("Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        ok, msg = bank.withdraw_money(acc, int(pin), amount)
        if ok:
            st.success(msg)
        else:
            st.error(msg)


# ------------------ SHOW DETAILS --------------------------
elif menu == "Get Details":
    st.header("Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Show Details"):
        data = bank.get_details(acc, int(pin))
        if data:
            st.json(data)
        else:
            st.error("Invalid Account or PIN")


# ------------------ UPDATE DETAILS --------------------------
elif menu == "Update Details":
    st.header("Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    name = st.text_input("New Name (optional)")
    email = st.text_input("New Email (optional)")
    phone = st.text_input("New Phone (optional)")
    new_pin = st.text_input("New PIN (optional)")

    if st.button("Update"):
        result = bank.update(acc, int(pin), name, email, phone, new_pin)
        if result:
            st.success("Details updated successfully")
        else:
            st.error("Invalid Account or PIN")


# ------------------ DELETE ACCOUNT --------------------------
elif menu == "Delete Account":
    st.header("Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Delete"):
        result = bank.delete(acc, int(pin))
        if result:
            st.success("Account deleted successfully")
        else:
            st.error("Invalid Account or PIN")
