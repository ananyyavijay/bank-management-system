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

    def depositemoney(self):
        accnumber = input("please tell your acc number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("no data found")

        else:
            amount = int(input("enter the amount for deposite"))
            if amount > 10000 or amount < 0:
                print("amount is insuuficient or too large to deposite: ")

            else:
                print(userdata)
                userdata[0]['balance'] += amount
                Bank.__update()
                print("amount deposited successfully")

    def withdrawmoney(self):
        accnumber = input("please tell your acc number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("no data found")

        else:
            amount = int(input("enter the amount you want to withdraw: "))
            if userdata[0]['balance'] < amount:
                print("insufficient amount")

            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("amount withdrawn successfully")

    def showdetails(self):
        accnumber = input("please tell your acc number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        print("your details are shown below \n\n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")

    def updatedetails(self):
        accnumber = input("please tell your acc number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        print("Fill the details for change or leave it empty if no change")

        newdata = {
            "name": input("please tell new name or press enter : "),
            "email":input("please tell your new Email or press enter to skip :"),
            "pin": input("enter new Pin or press enter to skip: ")
        }
        
        if newdata["name"] == "":
            newdata["name"] = userdata[0]['name']
        if newdata["email"] == "":
            newdata["email"] = userdata[0]['email']
        if newdata["pin"] == "":
            newdata["pin"] = userdata[0]['pin']

        #non changable feilds
        newdata['age'] = userdata[0]['age']
        newdata['balance'] = userdata[0]['balance']
        newdata['accountNo'] = userdata[0]['accountNo']

        if (newdata['pin']) == str:
            newdata['pin'] = int(newdata['pin'])

        for i in newdata:
            if newdata[i] == userdata[0][i]:
                continue
            else:
                userdata[0][i] = newdata[i]
        Bank.__update()
        print("details updated successfully")

    def deleteaccount(self):
        accnumber = input("please tell your acc number: ")
        pin = int(input("please tell your pin: "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and str(i['pin']) == str(pin)]

        if not userdata:
            print("data don't exists")
        else:
            check = input("press y to delete your account or n to skip: ")

            if check == 'n' or check == 'N':
                print("account is not deleted")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully")

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

if check == 2:
    user.depositemoney()

if check == 3:
    user.withdrawmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.deleteaccount()