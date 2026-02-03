class Bank_Account:
    def __init__(self,name,number,balance): # This is called the constructor method
        self.customer_name=name
        self.account_number=number
        self.balance=balance
    def deposit(self,amount):
        c=amount+self.balance
        print("Amount Deposited:",c)
        print("Balance:",self.balance+amount)

    def __del__(self):
        print(self.customer_name,"Bank Account Closed") # This is called the destructor method

    def display(self):
        print("Customer Name:",self.customer_name)
        print("Account Number:",self.account_number)
        print("Balance:",self.balance)

customer1=Bank_Account("Priya",123456,1000.0)
customer1.display()
customer1.deposit(500.0)