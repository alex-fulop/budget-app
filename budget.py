import math


def get_title(category_name, length):
    offset = (length - len(category_name)) / 2
    decor = '*' * int(offset)
    return decor + category_name + decor + '\n'


def get_desc(item):
    desc = item["description"]
    trimmed_desc = desc if len(desc) < 23 else desc[:23] + ' '
    return trimmed_desc


def get_price(item):
    price = '%.2f' % item["amount"]
    return price


def get_line(item, length):
    desc = get_desc(item)
    price = get_price(item)
    spacing = ' ' * (length - len(desc) - len(price))
    line = desc + spacing + price + '\n'
    return line


class Category:

    def __str__(self):
        length = 30
        total = 0
        content = ''
        title = get_title(self.category, length)
        for item in self.ledger:
            line = get_line(item, length)
            content = content + line
            total = total + float(get_price(item))
        string = title + content + 'Total: ' + str(total)
        return string

    def __init__(self, category):
        self.category = category
        self.ledger = list()

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.deposit(-amount, description)
            return True
        return False

    def get_balance(self):
        total = 0
        for transaction in self.ledger:
            total = total + transaction["amount"]
        return total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.category)
            category.deposit(amount, "Transfer from " + self.category)
            return True
        return False

    def check_funds(self, amount):
        if self.get_balance() - amount >= 0:
            return True
        else:
            return False


def create_spend_chart(categories):
    total_spent = get_total_spent(categories)
    expenses = get_expenses(categories)

    for category in categories:
        expenses[category.category] = round_to_nearest_ten(expenses[category.category] * 100 / total_spent)
    graph = get_graph(categories, expenses)
    print(graph)
    return graph


def get_expenses(categories):
    expenses = dict()
    for category in categories:
        spent_by_category = 0
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                spent_by_category = spent_by_category + transaction["amount"]
        expenses[category.category] = abs(spent_by_category)
    return expenses


def get_graph(categories, expenses):
    main_graph = get_main_graph(categories, expenses)
    main_graph = main_graph + '    ----------\n'
    height = len(max(expenses.keys(), key=len))
    tags = get_tags(categories, height)
    return 'Percentage spent by category\n' + main_graph + tags


def get_tags(categories, height):
    tags = ''
    for index in range(height):
        line = '    '
        last_one = index != height - 1
        for category in categories:
            line = get_line_for_tag(category, index, line)
        tags = tags + line + ' \n' if last_one else tags + line + ' '
    return tags


def get_line_for_tag(category, index, line):
    if 0 <= index < len(category.category):
        return line + ' ' + category.category[index] + ' '
    else:
        return line + '   '


def get_main_graph(categories, expenses):
    output = ''
    percentage = 100
    while percentage >= 0:
        line = get_graph_line(categories, expenses, percentage)
        output = output + line + ' \n'
        percentage = percentage - 10
    return output


def get_graph_line(categories, expenses, percentage):
    line = get_graph_percentage(percentage)
    for category in categories:
        if expenses[category.category] >= percentage:
            line = line + ' o '
        else:
            line = line + '   '
    return line


def get_graph_percentage(percentage):
    if 0 < percentage < 100:
        return ' ' + str(percentage) + '|'
    elif percentage == 100:
        return str(percentage) + '|'
    else:
        return '  ' + str(percentage) + '|'


def round_to_nearest_ten(number):
    return math.floor(number / 10) * 10


def get_total_spent(categories):
    total_spent = 0
    for category in categories:
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                total_spent = total_spent + transaction["amount"]
    return abs(total_spent)
