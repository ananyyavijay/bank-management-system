import json
import random
import string
from pathlib import Path

class Bank:
    database = 'info.json'
    info = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                info = json.loads(fs.read()) #Converts JSON string to Python object using json.loads()
        else:
            print("no such file exists")
    except Exception as err:
        print(f"an exception occured as {err}")

    @staticmethod
    def update():
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.info))

    def createaccount(self):
        info = {
            "name" : input("Tell your name: "),
            "age" : int(input("Tell your age: ")),
            "email" : input("Tell your email: "),
            "pin" : int(input("Tell your 4 number pin: ")),
            "accountNo" : 1230,
            "balance" : 0
        }
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("sorry you cannot create an account")
        else:
            print("account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note your account number")

            Bank.data.append(info)
        
            Bank.update()

user = Bank()
print("press 1 for creating an account")
print("press 2 for depositing money in bank")
print("press 3 for withdrawing the money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting your account")

check = int(input("tell your response:- "))
 
if check == 1:
    user.createaccount()