import Bank_management_account as Bank
from getpass import getpass
import pickle
import os
Record = {}
# Save data to file
if os.path.exists("record.pkl"):
    with open("record.pkl", "rb") as f:
        Record = pickle.load(f)

ADMIN_PASSWORD = "admin123"

# Admin: View all savings/current accounts
def view_all_accounts():
    print("\n--- Admin Access ---")
    password = getpass("Enter admin password: ")
    if password != ADMIN_PASSWORD:
        print("Access Denied: Incorrect password.")
        return
    
    acc_type = input("Enter account type to view (savings/current): ").strip().lower()
    if acc_type not in ['savings', 'current']:
        print("Invalid account type.")
        return

    found = False
    for acc in Record.values():
        if acc._Type == acc_type:
            found = True
            if acc_type == 'savings':
                print(f"Name: {acc.Acc_Holder}, Acc No: {acc.account_no}, Age: {acc._Age}, Type: {acc._Type}, Balance: ₹{acc.Balance}")
            elif acc_type == 'current':
                print(f"Name: {acc.Acc_Holder}, Acc No: {acc.account_no}, Age: {acc._Age}, Type: {acc._Type}, Balance: ₹{acc.Balance}, Overdraft: ₹{acc.Overdraft}")
    
    if not found:
        print(f"No {acc_type} accounts found.")

#Account creation
def Create_acc():
    name = input("Enter your Name : ").strip()
    try:
        age = int(input("Enter your Age: "))
        if age < 18:
            print("You must be at least 18 years old to open a bank account.")
            return
        bal = float(input("Enter your Opening Balance: "))
        if bal <= 0:
            print("You must Enter Positive Balance.")
            return
    except ValueError:
        print("Please enter valid numeric input.")
        return
    passw = getpass("Enter your password : ").strip()
    acc_type = input("Enter your account type (savings/current) : ").strip().lower()
    if acc_type not in ['savings', 'current']:
        raise Bank.WrongValueError("Invalid account type entered.")
    
    if(acc_type == 'current'):
        acc = Bank.CurrentAccount(name, age, passw, acc_type, bal)
    else:
        acc = Bank.SavingsAccount(name, age, passw, acc_type, bal)
    
    Record[acc.account_no] = acc
    print(f"Your account has been stored. Account No: {acc.account_no}")
#account validation
def validate_account():
    try:
        acc_no = int(input("Enter your account no : "))
    except ValueError:
        print("Invalid account number format.")
        return None, None, None
    passw = getpass("Enter your password : ").strip()
    acc = Record.get(acc_no)
    return acc_no, passw, acc    

def find_accounts_by_name(name):
    matches = [acc for acc in Record.values() if acc.Acc_Holder.lower() == name.lower()]
    for acc in matches:
        print(f"Account holder : {acc.Acc_Holder}\nAge : {acc._Age}\nAccount No: {acc.account_no}\nType: {acc._Type}\nBalance: ₹{acc.Balance}")   

def main():
    print("\nABC Bank Welcomes You")

    while True:
        print("\n-------- MENU --------")
        print("1 - Open Your Account")
        print("2 - Check Account Balance")
        print("3 - Deposit Amount")
        print("4 - Withdraw Amount")
        print("5 - Change Your password")
        print("6 - Close Your Account")
        print("7 - View Transaction History")
        print("8 - Apply Interest")
        print("9 - Find Account by Name")
        print("10 - Access Master List")
        print("0 - Exit the Bank")
        
        try:
            choice = int(input("Enter your choice : "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            Create_acc()
        elif choice in [2, 4, 5, 6, 7, 8]:
            acc_no, passw, acc = validate_account()
            if acc is not None:
                actions = {
                    2: acc.CheckBalance,
                    4: acc.WithdrawAmount,
                    5: acc.changePassword,
                    6: acc.close_acc,
                    7: acc.view_transaction_history,
                    8: getattr(acc, "apply_interest", lambda *_: print("Interest not supported for this account."))
                }
                actions[choice](acc_no, passw)
            else:
                print("Account not found.")
        elif choice == 3:
            try:
                acc_no = int(input("Enter your account no : "))
                acc = Record.get(acc_no)
                if acc is not None:
                    acc.DepositAmount(acc_no)
                else:
                    print("Account not found.")
            except ValueError:
                print("Invalid account number format.")
        elif choice == 9:
            name = input("Enter the account holder's name : ").strip()
            find_accounts_by_name(name)
        elif choice == 10:  # or any free case number
            view_all_accounts()
        elif choice == 0:
            print("Thank you for your time. Have a good day!")
            break
        else:
            print("Please select a valid option.")

    with open("record.pkl", "wb") as f:
        pickle.dump(Record, f)


if __name__== "__main__":
    main()