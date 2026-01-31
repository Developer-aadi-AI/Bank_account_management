import random
import datetime
from getpass import getpass

class WrongValueError(Exception):
    def __init__(self, message="The value does not match the choice"):
        super().__init__(message)

class BankAccount:
    used_no = set()
    def __init__(self, Acc_Holder, Age,  Password):
        self.Acc_Holder = Acc_Holder
        self._Age = Age
        self._Password = Password
        self._Type = None
        self.isclose = False
        while True:
            acc = random.randint(100000,999999)
            if acc not in BankAccount.used_no:
                self.account_no = acc
                print(f"Account creation successfull\nYour account no. is {self.account_no}")
                BankAccount.used_no.add(acc)
                break

    def _log_transaction(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("transactions.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Account {self.account_no}: {message}\n")            

    def _authenticate_acc(self, acc_no):
        if self.isclose == True:
            print("This account is closed and cannot be used.")
            return False
        else:
            return acc_no == self.account_no
                 
    
    def _authenticate_passw(self, passw):
        if self.isclose == True:
            print("This account is closed and cannot be used.")
            return False
        else:
            return passw == self._Password
                
    
    def validate_credentials(self, acc_no, passw):
        acc_match = self._authenticate_acc(acc_no)
        pass_match = self._authenticate_passw(passw)
        if acc_match and pass_match:
            return "OK"
        elif acc_match:
            return "Wrong password"
        elif pass_match:
            return "Wrong account number"
        else:
            return "Both incorrect"
        
    def changePassword(self,acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":
            new_pass = getpass("Enter new password: ")
            confirm = getpass("Confirm new password: ")
            if new_pass == confirm:
                self._Password = new_pass
                print("Password changed successfully.")
                self._log_transaction("Password changed.")
            else:
                print("Passwords did not match.")
        else:
            print(status)
    
    def view_transaction_history(self, acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":
            with open("transactions.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if f"Account {self.account_no}:" in line:
                        print(line.strip())
        else:
            print(status)
    @staticmethod
    def safe_amount_input(prompt="Enter amount: "):
        try:
            amount = float(input(prompt))
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            return amount
        except ValueError as e:
            print("Invalid input:", e)
            return None
    
class CurrentAccount(BankAccount):
    def __init__(self, Acc_Holder, Age, Password, Type, Balance):
        super().__init__(Acc_Holder, Age, Password)
        self._Type = Type
        self.Balance = Balance
        self.Overdraft = Balance*3
        self.Draft_limit = self.Overdraft

    def CheckBalance(self,acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":            
            print(f"Your Account balance is {self.Balance}rs and your overdraft limit is {self.Overdraft}rs") 
            self._log_transaction("Checked balance.")
        else:
            print(status)

    def DepositAmount(self, acc_no):
        if(super()._authenticate_acc(acc_no)):
            amount = self.safe_amount_input("Enter amount to deposit")
            if amount is None:
                return    
                
                
            if(self.Overdraft < self.Draft_limit):
                remaining = self.Draft_limit - self.Overdraft
                if(remaining>=amount):
                    self.Overdraft += amount
                else:
                    self.Overdraft = self.Draft_limit
                    self.Balance += (amount - remaining)
                    self._log_transaction(f"Deposited ₹{amount}. New Balance: ₹{self.Balance}")
            else:
                self.Balance += amount
                self._log_transaction(f"Deposited ₹{amount}. New Balance: ₹{self.Balance}")
            print(f"your account with account number {self.account_no} is credited with {amount}rs")
        else:
            print("Wrong account no is Entered")

    def WithdrawAmount(self, acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":            
            amount = self.safe_amount_input("Enter the amount you want to Withdraw : ")
            if amount is None:
                return
            
            if(amount<=self.Balance):
                self.Balance -= amount
            elif(amount>self.Balance and (amount-self.Balance)<=self.Overdraft):
                self.Overdraft = self.Overdraft - (amount-self.Balance)
                self.Balance = 0
            else:
                print("The amount you want to debit is more than your Overdraft limit ")
                self._log_transaction(f"Failed withdrawal attempt of ₹{amount}. Insufficient funds.")
                return
            print(f"your account with account number {self.account_no} is Debited with {amount}rs")
            self._log_transaction(f"Withdrew ₹{amount}. Remaining Balance: ₹{self.Balance}, Overdraft: ₹{self.Overdraft}")        
        else:
            print(status)

    def close_acc(self, acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":
            if(self.Overdraft == self.Draft_limit):
                print(f"The account with account no : {self.account_no} is closed and the amount {self.Balance}rs is given ")
                self.Balance = 0
                self.isclose = True
                self._log_transaction("Account closed. Final Balance returned.")

            else:
                print(f"Clear your dues before closing your account. Dues are {self.Draft_limit - self.Overdraft}rs")
        else:
            print(status)

class SavingsAccount(BankAccount):
    def __init__(self, Acc_Holder, Age, Password, Type,  Balance):
        super().__init__(Acc_Holder, Age, Password)
        self._Type = Type
        self.Balance = Balance

    def CheckBalance(self,acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":
            print(f"Your Account balance is {self.Balance} rs") 
            self._log_transaction("Checked balance.")
        else:
            print(status)

    def DepositAmount(self, account_no):
        if(super()._authenticate_acc(account_no)):
            amount = self.safe_amount_input("Enter the amount you want to deposit : ")
            if amount is None:
                return
            
            self.Balance += amount
            print(f"your account with account number {self.account_no} is credited with {amount}rs")
            self._log_transaction(f"Deposited ₹{amount}. New Balance: ₹{self.Balance}")
        else:
            print("Wrong account no is Entered")


    def WithdrawAmount(self, acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":
            amount = self.safe_amount_input("Enter the amount you want to Withdraw : ")
            if amount is None:
                return
            if(amount<=self.Balance):
                self.Balance -= amount
                print(f"your account with account number {self.account_no} is Debited with {amount}rs")
                self._log_transaction(f"Withdrew ₹{amount}. Remaining Balance: ₹{self.Balance}")
            else:
                print("Insufficient Balance")
                self._log_transaction(f"Failed withdrawal attempt of ₹{amount}. Insufficient funds.")
        else:
            print(status)

    def close_acc(self, acc_no, passw):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":
            print(f"The account with account no : {self.account_no} is closed and the amount : {self.Balance}rs is given ")
            self.Balance = 0
            self.isclose = True
            self._log_transaction("Account closed. Final Balance returned.")                
        else:
            print(status)

    def apply_interest(self, acc_no, passw, rate=0.04):
        status = self.validate_credentials(acc_no, passw)
        if status == "OK":    
            interest = self.Balance * rate
            self.Balance += interest
            self._log_transaction(f"Interest of ₹{interest} applied.")
            print(f"The interest is {interest}rs for account_no : {acc_no}. Final Balance = {self.Balance}rs")
        else:
            print(status)