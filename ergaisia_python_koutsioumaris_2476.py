import os
clear = lambda: os.system('clear')

import traceback

store_items = {
    "C1": {
        "name": "Chicken Burger",
        "ingredients": "Burger με κοτόπουλο, bacon, τυρί edam, τομάτα, μαρούλι με μαγιονέζα",
        "price": 4.20
    },
    "C2": {
        "name": "Ham Burger",
        "ingredients": "Burger με μπιφτέκι, τυρί, κέτσαπ, μουστάρδα",
        "price": 2.85
    },
    "C3": {
        "name": "Green Burger",
        "ingredients": "Burger με ζουμερό μπιφτέκι, τυρί, φρέσκια τομάτα, μαρούλι,κρεμμύδι, πίκλες, κέτσαπ και dressing sauce",
        "price": 4.20
    },
    "B1": {
        "name": "Club Sandwich",
        "ingredients": "Club sandwich με 3 πλούσιες στρώσεις Philadelphia σε φρυγανισμένο ψωμί του τοστ με ζουμερό κοτόπουλο φιλέρο, bacon, τομάτα,μαρούλι και τηγανητές πατάτες",
        "price": 10.90
    },
    "B2": {
        "name": "Σαλάτα ceasar's",
        "ingredients": "Δροσερή πράσινη σαλάτα με ζουμερό κοτόπουλου σε βάση μαρουλιού, με καλαμπόκι, κρουτόν, τριμμένο τυρί και vinaigreve ελαιόλαδου",
        "price": 6.90
    },
    "B3": {
        "name": "Κινόα με Λαχανικά",
        "ingredients": "Δροσερή σαλάτα με κινόα, κόκκινη πιπεριά, τοματίνια,αγγούρι, δυόσμο, φρέσκο μαϊντανό και sauce λαδολέμονο.",
        "price": 6.30
    },
}

class OrderClass:
    cart = {}

    @staticmethod
    def show_items():
        line_format = "{: <5} {: <20} {: <50} {: >10}"
        print(line_format.format("Code", "Item", "ingredients", "Price"))
        for item_code in store_items:
            item = store_items[item_code]
            print(line_format.format(item_code, item['name'],item['ingredients'][:50], item['price']))

    @classmethod
    def show_cart(self):
        line_format = "{: >4} {: >5} {: >10} {: >10}"
        print(line_format.format("Item", "Qty", "Price", "Total"))
        for item_code in self.cart:
            item = store_items[item_code]
            quantity = self.cart[item_code]
            price = item['price']
            total = format(quantity * price,'.2f')
            print(line_format.format( item_code, quantity, price, total))

    @classmethod
    def clear_cart(self):
        self.cart = {}

    @classmethod
    def check_values(self, code, quantity):
        has_errors = 0
        # check if code exists
        if not store_items.get(code):
            print('The code provided "%s" does not exist.'%(code))
            has_errors = 1
        # check if quantity is int
        try:
            quantity = int(quantity)
        except:
            print('Quantity should be an integer, given "%s".'%(quantity))
            has_errors = 1
        return not has_errors

    @classmethod
    def add(self, code, quantity):
        if (self.check_values(code, quantity)):
            new_value = (self.cart.get(code) or 0) + int(quantity)
            self.cart.update({ code:new_value })
            return 1
        else:
            return 0

    @classmethod
    def remove(self, code, quantity):
        if (self.check_values(code, quantity)):
            new_value = (self.cart.get(code) or 0) - int(quantity)
            if new_value < 0:
                new_value = 0
            self.cart.update({ code: new_value })
            if self.cart.get(code) == 0:
                self.cart.pop(code)
            return 1
        else:
            return 0

    @classmethod
    def get_total(self):
        items_total = 0
        for item_code in self.cart:
            item = store_items[item_code]
            price = item['price']
            quantity = self.cart[item_code]
            total = quantity * price
            items_total += total
        return format(items_total,'.2f')

    @classmethod
    def pay(self):
        total = self.get_total()
        print('Total: %s'%(total))
        methods = {
            1: 'cash',
            2: 'card'
        }
        print('Select payment method:')
        for item in methods:
            print('%s. %s'%(item,methods[item]))
        valid_method = 0
        while not valid_method:
            method_index = int(input('> '))
            if method_index == 1:
                valid_method = 1
                amount_given = input('Amount given: ')
                while amount_given < total:
                    amount_given = input('Amount is not enough, please re-enter: ')
                change = float(amount_given) - float(total)
                print('Changes amount is %.2f'%(change))
            elif method_index == 2:
                valid_method = 1
                print('Thank you, your payment has been processed.')
            else:
                print('Invalid payment method')
        return 1


def split_input(user_inp):
    vals = user_inp.split(" ")
    while len(vals) <= 2:
        vals.append('')
    return {
            "mode": vals[0],
            "code": vals[1],
            "quantity": vals[2]
        }

separator_length = 90
def print_separator(txt, separator):
    if len(txt): txt = ' {} '.format(txt)
    half_separator_length = int(separator_length/2) - int(len(txt)/2)
    print(separator * half_separator_length + txt + separator * half_separator_length)

def print_usage():
    info = "Add(A) Remove(R) Pay(P) Exit(E)"
    example = "[A|R] [Item_code] [Quantity]"
    spaces = ' ' * (int(separator_length) - int(len(info)) - int(len(example)))
    print( info + spaces + example )

order = OrderClass()
user_input = None
stop = 0
while not stop:
    try:
        clear()
        print_separator('WELCOME TO ESTIA', ' ')
        print_separator('', '-')
        order.show_items()
        print_separator('ORDER','-')
        order.show_cart()
        print_separator('', '-')
        print_usage()
        print_separator('', '-')
        user_input = input("Enter Code: ").upper()

        inp = split_input(user_input)
        mode = inp.get('mode')
        code = inp.get('code')
        quantity = inp.get('quantity')

        result = 1
        if not(mode in ['A','R','P','E']):
            input("Invalid option. Press Enter to Continue...")

        if mode == 'A':
            result = order.add(code, quantity)
        elif mode == 'R':
            result = order.remove(code, quantity)
        elif mode == 'P':
            if order.get_total() != '0.00':
                result = order.pay()
                order.clear_cart()
            else:
                print('No items were purchased')
                result = 0
        elif mode == 'E':
            stop = 1

        if not result:
            input("Press Enter to Continue...")

    except:
        print(traceback.format_exc())
        raw_input("Press return to exit")



