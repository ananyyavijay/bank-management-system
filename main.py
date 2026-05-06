import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read()) #Converts JSON string to Python object using json.loads()
        else:
            print("no such file exists")
    except Exception as err:
        print(f"an exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerator(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=5) 
        id = alpha + num
        random.shuffle(id) #shuffle gives a list
        return "".join(id)

    def createaccount(self):
        info = {
            "name" : input("Tell your name: "),
            "age" : int(input("Tell your age: ")),
            "email" : input("Tell your email: "),
            "pin" : int(input("Tell your 4 number pin: ")),
            "accountNo" : Bank.__accountgenerator(),
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
        
            Bank.__update()

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