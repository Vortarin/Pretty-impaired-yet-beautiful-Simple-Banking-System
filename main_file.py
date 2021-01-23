# Write your code here
import random
import sqlite3


class DBHelper:
    def __init__(self, dbname='card.s3db'):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

    def setup(self):
        stmt = '''CREATE TABLE IF NOT EXISTS card (
        id INTEGER, 
        number TEXT, 
        pin TEXT, 
        balance INTEGER DEFAULT 0
        );'''
        self.cur.execute(stmt)
        self.conn.commit()

    def add_item(self, id, number, pin, balance):
        stmt = f'INSERT INTO card (id, number, pin, balance) VALUES ({id}, {number}, {pin}, {balance})'
        self.cur.execute(stmt)
        self.conn.commit()

    def delete_item(self, id):
        stmt = f'DROP FROM card WHERE id = {id}'
        self.cur.execute(stmt)
        self.conn.commit()

    def get_credentials(self, number, pin):
        stmt = f'SELECT number, pin FROM card WHERE number = {number} AND pin = {pin}'
        self.cur.execute(stmt)
        if self.cur.fetchone() is None:
            print("\nWrong card number or PIN!")
            return False
        else:
            print("\nYou have successfully logged in!")
            return True

    def get_balance(self, number):
        stmt = f'SELECT balance FROM card WHERE number = {number};'
        self.cur.execute(stmt)
        return self.cur.fetchone()[0]

    def get_nums(self):
        stmt = 'SELECT number FROM card;'
        self.cur.execute(stmt)
        ans = []
        for elem in self.cur.fetchall():
            ans.append(elem[0])
        return ans

    def get_ids(self):
        stmt = 'SELECT id FROM card;'
        self.cur.execute(stmt)
        ans = []
        for elem in self.cur.fetchall():
            ans.append(elem[0])
        return ans

    def get_max_id(self):
        stmt = 'SELECT max(id) FROM card;'
        self.cur.execute(stmt)
        return self.cur.fetchone()[0]

    def check_luhn(self, number):
        num = [int(x) for x in number]
        num[0::2] = (x * 2 for x in num[0::2])
        num[0::2] = (x - 9 if x > 9 else x for x in num[0::2])
        return True if sum(num) % 10 == 0 else False

    def add_income(self, amount, number):
        stmt = f'UPDATE card SET balance = balance + {amount} WHERE number = {number};'
        self.cur.execute(stmt)
        self.conn.commit()

    def transfer(self, sender_number):
        card_num = input('\nTransfer\nEnter card number:')
        if not self.check_luhn(card_num):
            print('Probably you made a mistake in the card number. Please try again!')
        else:
            if card_num == sender_number:
                print("You can't transfer money to the same account!")
            elif card_num not in self.get_nums():
                print('Such a card does not exist.')
            else:
                amount = int(input('\nEnter how much money you want to transfer:\n'))
                if self.get_balance(sender_number) < amount:
                    print('Not enough money!')
                elif amount < 0:
                    print('You really want to send a negative number?')
                else:
                    self.add_income(-amount, sender_number)
                    self.add_income(amount, card_num)
                    print('Success!')

    def del_account(self, card_num):
        stmt = f'DELETE FROM card WHERE number = {card_num};'
        self.cur.execute(stmt)
        self.conn.commit()


class Bank:
    iin = '400000'

    def __init__(self):
        self.db = DBHelper()
        self.db.setup()

    def menu(self):
        while True:
            choice = int(input('\n1. Create an account\n2. Log into account\n0. Exit\n'))
            if choice == 1:
                self.create_acc()
            elif choice == 2:
                num = input('\nEnter your card number:')
                pin = input('Enter your PIN:')
                if self.db.get_credentials(num, pin):
                    while choice != 0:
                        print('\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
                        choice = int(input())
                        if choice == 1:
                            print(f'\nBalance: {self.db.get_balance(num)}')
                        if choice == 2:
                            income = int(input(f'\nEnter income:\n'))
                            self.db.add_income(income, num)
                            print('Income was added!')
                        if choice == 3:
                            self.db.transfer(num)
                        if choice == 4:
                            self.db.del_account(num)
                            print('\nThe account has been closed!')
                            break
                        if choice == 5:
                            print("\nYou have successfully logged out!")
                            break
            if choice == 0:
                break
        print('\nBye!')

    def create_acc(self):
        id_ = self.create_id()
        card_num = self.create_num()
        pin = self.create_pin()
        balance = 0
        self.db.add_item(id_, card_num, pin, balance)
        print(f'\nYour card has been created\nYour card number:\n{card_num}\nYour card PIN:\n{pin}')

    def create_num(self):
        while True:
            num = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            if num not in self.db.get_nums():
                break
        card_num = Bank.iin + num
        num_l = card_num  # Another Luhn algorith right here, it's pretty dummy code, but it was 
        num_l = list(num_l)  # written at one shot under the inspiration, and I wanted to leave it just as it is
        i = 0
        for elem in num_l:
            elem = int(elem)
            num_l[i] = elem * 2 if i % 2 == 0 else elem
            i += 1
        i = 0
        for elem in num_l:
            num_l[i] = elem - 9 if elem > 9 else elem
            i += 1
        sum_ = sum(num_l)
        checksum = str(10 - sum_ % 10)
        if checksum == '10':
            checksum = '0'  # and the Luhn ends here
        return card_num + checksum

    def create_id(self):
        max_id = self.db.get_max_id()
        if max_id is None:
            id_ = 0
        else:
            id_ = max_id + 1
        return id_

    def create_pin(self):
        pin = str(random.randint(0, 9999))
        n_pin = '0' * (4 - len(pin)) + pin
        return n_pin


if __name__ == "__main__":
    a = Bank()
    a.menu()
