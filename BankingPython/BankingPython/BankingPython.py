import random
from re import S
import tkinter as tk
import unittest

class Account:

    def __init__(self, starting_balance :  int, first_name : str, last_name : str, root):
        self._balance = starting_balance
        self.__account_number = random.randint(0,999999)
        self.first_name = first_name
        self.last_name = last_name
        self.root = root
        
    def deposit(self, amount):
        self._balance += amount
        
    def withdraw(self, amount):

        self._balance -= amount
        
    def check_balance(self):
        return self._balance
    
    def get_account_number(self):
        return self.__account_number

        
    
class SavingsAccount(Account):

    def __init__(self, starting_balance, first_name, last_name, root):
        super().__init__(starting_balance, first_name, last_name, root)
        self.__interest_rate = 0.025
        self.show_interest_button = tk.Button(self.root, text='Show Collected Interest', command=self.calculate_interest)
        self.show_interest_button.pack()
        
    def calculate_interest(self):
        tk.Label(self.root, text=f'Interest Accumulated: {self._balance * self.__interest_rate}').pack()
    

class CurrentAccount(Account):

    def __init__(self, starting_balance, first_name, last_name, root):
        super().__init__(starting_balance, first_name, last_name, root)
        self.__transaction_fee = 1.5
        self.transaction_fee_label = tk.Label(self.root, text=f'Transaction Fee: {self.get_transaction_fee()}')
        
    def get_transaction_fee(self):
        return self.__transaction_fee
    
    def withdraw(self, amount):
        self._balance -= amount + self.get_transaction_fee()
        self.root.update()
    

class Bank:
    def __init__(self, name, address, root):
        self.root = root
        self.name = name
        self.address = address
        self.__accounts = {}

       
    def validate_account(self, account_number, password):
        try:
            # Check if account_number is a non-empty string representing a valid integer
            if account_number and account_number.isdigit():
                account = self.__accounts[int(account_number)]
                return account['password'] == password
            else:
                return False
        except KeyError:
            return False

    def create_savings_account(self, starting_amount, first_name, last_name, password):
        try:
            new_account = SavingsAccount(int(starting_amount), first_name, last_name, self.root)
            self.__accounts[new_account.get_account_number()] = {
                    'Account' : new_account,
                    'Type' : 'Savings',
                    'password' : password
                }
            return new_account
        except:
            return None
            

    def create_current_account(self, starting_amount, first_name, last_name, password):
        try:
            new_account = CurrentAccount(int(starting_amount), first_name, last_name, self.root)
            self.__accounts[new_account.get_account_number()] = {
                    'Account' : new_account,
                    'Type' : 'Current',
                    'password' : password
                }
            
            return new_account
            
        except:
            return None
    
    def get_account(self, account_number):
        try:
            return self.__accounts[account_number]
        except:
            return 'No account'
    
    # def print_accounts(self):
    #     print(self.__accounts)

    

  
class App:
    def __init__(self, root, bank):
        self.root = root
        self.root.geometry('1000x700')
        self.bank = bank
        
        self.active_account = Account(0, "", "", self.root)
        self.current_frame = tk.Frame()
        self.current_frame.pack()
        self.load_login(self.current_frame)
        
    
        #######################===LOGIN FRAME===#################################
    def load_login(self, frame):

        self.enter_details_label = tk.Label(frame, text='Please enter your login details')
        self.enter_details_label.pack()
        
        self.account_number_label = tk.Label(frame, text='Account Number:')
        self.account_number_label.pack()
        
        self.account_number_entry = tk.Entry(frame)
        self.account_number_entry.pack()
        
        self.password_label = tk.Label(frame, text='Password:')
        self.password_label.pack()
        
        self.password_entry = tk.Entry(frame)
        self.password_entry.pack()
    
        self.submit_button = tk.Button(frame, text='Login', command=self.login)
        self.submit_button.pack()
        
        self.register_button = tk.Button(frame, text='Register', command=lambda : self.load_frame(self.current_frame, self.load_register))
        self.register_button.pack()
    ############################################################################
        
    #######################===ACCOUNT FRAME===###################################
    def load_account(self, frame, account):
        
        self.logout_button = tk.Button(frame, text='Logout', command=self.logout)
        self.logout_button.pack()

        self.account_number_label = tk.Label(frame, text=f'Account Number: {self.active_account.get_account_number()}')
        self.account_number_label.pack()
        
        self.account_type_label = tk.Label(frame, text=f'Account Type: {self.bank.get_account(self.active_account.get_account_number())["Type"]}')
        self.account_type_label.pack()
    
        self.current_amount_label = tk.Label(frame, text='Current Balance: ')
        self.current_amount_label.pack()
        
        self.balance_label = tk.Label(frame, text=self.active_account.check_balance())
        self.balance_label.pack()
        
        self.withdraw_button = tk.Button(frame, text='Withdraw', command=lambda: self.enter_amount('Withdraw', self.current_frame))
        self.withdraw_button.pack()
        
        self.deposit_button = tk.Button(frame, text='Deposit', command=lambda: self.enter_amount('Deposit', self.current_frame))
        self.deposit_button.pack()


    #############################################################################
     
    #####################===Register Frame===###################################
    def load_register(self, frame):

        self.option = tk.StringVar(self.root, value='1')
        
        self.savings_radio = tk.Radiobutton(frame, text='Savings Account', value='1', variable=self.option)
        self.savings_radio.pack()
        self.current_radio = tk.Radiobutton(frame, text='Current Account', value='2', variable=self.option)
        self.current_radio.pack()
        

        self.enter_details_label = tk.Label(frame, text='Please enter your details')
        self.enter_details_label.pack()
        
        self.first_name_label = tk.Label(frame, text='First Name:')
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(frame)
        self.first_name_entry.pack()
        
        self.last_name_label = tk.Label(frame, text='Last Name:')
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(frame)
        self.last_name_entry.pack()
        
        self.starting_amount_label = tk.Label(frame, text='How much would you like to deposit to open your account:')
        self.starting_amount_label.pack()
        self.starting_amount_entry = tk.Entry(frame)
        self.starting_amount_entry.pack()
        
        self.password_label = tk.Label(frame, text='Password:')
        self.password_label.pack()
        self.password_entry = tk.Entry(frame)
        self.password_entry.pack()
        
        self.check_password_label = tk.Label(frame, text='Re-enter Password:')
        self.check_password_label.pack()
        self.check_password_entry = tk.Entry(frame)
        self.check_password_entry.pack()
    
        self.submit_button = tk.Button(frame, text='Submit', command=self.register)
        self.submit_button.pack()
        
        #######################################################################################################
    
        ####################===Functions===##################################################################
    def transaction(self, function, amount, transaction_fee):

        if function == self.active_account.withdraw and (amount + transaction_fee) > self.active_account.check_balance():
            self.enter_amount_label.config(text='Insufficient Funds')
            return
        function(amount)
        self.balance_label.config(text=self.active_account.check_balance())
        self.enter_amount_label.destroy()
        self.amount_entry.destroy()
        self.submit_button.destroy()
    
    def enter_amount(self, type, frame):
        self.enter_amount_label = tk.Label(frame, text='Enter amount')
        self.enter_amount_label.pack()
        
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.pack()
        
        self.submit_button = tk.Button(frame, text='submit', command= lambda: self.transaction(self.active_account.withdraw if type == 'Withdraw' else self.active_account.deposit, int(self.amount_entry.get()), self.active_account.get_transaction_fee() if self.bank.get_account(self.active_account.get_account_number())['Type'] == 'Current' else 0)) #type:ignore
        self.submit_button.pack()
        
    
    def login(self):
        if self.bank.validate_account(self.account_number_entry.get(), self.password_entry.get()):
            account = self.bank.get_account(int(self.account_number_entry.get()))['Account']
            self.active_account = account
            self.load_frame(self.current_frame, self.load_account, self.active_account )
        else:
            self.enter_details_label.config(text='Incorrect login deatils')

            
            
    def logout(self):
        self.active_account = Account(0, "", "", self.root)
        self.load_frame(self.current_frame, self.load_login)
        

    def register(self):
        account_type = self.option.get()
        if (self.first_name_entry.get() == '' or self.last_name_entry.get() == '' or self.password_entry.get() == '' or self.check_password_entry.get() == '') or (self.password_entry.get() != self.check_password_entry.get()):
            self.enter_details_label.config(text='Invalid details')
            return

        if account_type == '1':
            new_account = self.bank.create_savings_account(self.starting_amount_entry.get(), self.first_name_entry.get(), self.last_name_entry.get(), self.password_entry.get())
        else:
            new_account = self.bank.create_current_account(self.starting_amount_entry.get(), self.first_name_entry.get(), self.last_name_entry.get(), self.password_entry.get())
            
        if new_account == None:
            self.enter_details_label.config(text='Please enter a valid starting amount')
            
        else:
            self.active_account = new_account
            self.load_frame(self.current_frame, self.load_account, self.active_account)
            
            
    def load_frame(self, frame, load_new_frame, account = None):
        existing_widgets = list(self.current_frame.winfo_children())

        # Clear existing widgets in the current frame
        for widget in existing_widgets:
            widget.destroy()

        # Pack the new frame
        if account == None:
            load_new_frame(frame)
        else:
            load_new_frame(frame, account)

            

# def main():
#     root = tk.Tk()
#     bank = Bank('AIB', 'Dublin, Co.Dublin', root)
#     app = App(root, bank)
#     root.mainloop()
    
# main()



class TestCurrentAccountWithdraw(unittest.TestCase):
    def test_current_withdraw(self):
        account = CurrentAccount(100, 'John', 'Doe', tk.Tk())
        account.withdraw(50)
        self.assertEqual(account.check_balance(), 50) # Doesn't factor in transaction_fee
    
    def test_savings_withdraw(self):
        account = SavingsAccount(100, 'John', 'Doe', tk.Tk())
        account.withdraw(200)
        self.assertEqual(account.check_balance(), -100) # Will not allow minus account balance
        

        
class TestBankValidateAccount(unittest.TestCase):
    def test_validate_account(self):
        bank = Bank('YourBank', 'SomeAddress', tk.Tk())
        acc = bank.create_savings_account(100, 'John', 'Doe', 'password123')
        self.assertTrue(bank.validate_account(str(acc.get_account_number()), 'password456')) 
        # Returns False due to incorrect password

class TestGetAccount(unittest.TestCase):
    def test_get_account(self):
        bank = Bank('YourBank', 'SomeAddress', tk.Tk())
        self.assertEqual(bank.get_account('788378'), Account) # Getting an account that doesnt exist





if __name__ == '__main__':
    unittest.main()







