import sys
import csv
import os

# By default combines files listed on command line
# If not uses hardcoded list
# To run a single file simply specify only one in either fashion
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = ['/mnt/c/Users/ross/ut_data/git/UTAUS201804DATA2-Class-Repository-DATA/03-Python/HOMEWORK/Instructions/PyBank/raw_data/budget_data_1.csv',
             '/mnt/c/Users/ross/ut_data/git/UTAUS201804DATA2-Class-Repository-DATA/03-Python/HOMEWORK/Instructions/PyBank/raw_data/budget_data_1.csv']

header = []
budget_data = []
total_months = 0
total_revenue = 0
average_revenue_change = 0
great_increase = 0
great_increase_month = ''
great_decrease = 0
great_decrease_month = ''
results = ''

# Used to account for unordered data if applicable
months = {'Jan' : '01',
          'Feb' : '02',
          'Mar' : '03',
          'Apr' : '04',
          'May' : '05',
          'Jun' : '06',
          'Jul' : '07',
          'Aug' : '08',
          'Sep' : '09',
          'Oct' : '10',
          'Nov' : '11',
          'Dec' : '12'}

# Creates pretty dollar amounts by adding commas
def add_commas(amount):
    amount = list(str(amount))[::-1]
    formatted = []
    while len(amount) > 3:
        formatted.extend(amount[:3])
        formatted.append(',')
        amount = amount[3:]
    formatted.extend(amount)
    formatted = ''.join(formatted[::-1])
    return formatted

# Puts the minus sign to the left of $
def format_currency(amount):
    if amount < 0:
        return '-$' + str(add_commas(round(amount)))[1:]
    else:
        return '$' + str(add_commas(round(amount)))

# Combine multiple CSV's if applicable
for file in files:
    with open(file) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            budget_data.append(row)

total_data = {}

# Combine values for the same month in a dict
for row in budget_data:
    if row[0] in total_data:
        total_data[row[0]] += int(row[1])
    else:
        total_data[row[0]] = int(row[1])

# Use combination of the year value and month conversion dict to put items back
# in order
total_list = sorted([[key, val] for key, val in total_data.items()],
    key=lambda x: x[0][-2:] + months[x[0][:3]])

# Get total months and revenue
total_months = len(total_list)
total_revenue = sum([month[1] for month in total_list])

# First month can't have a change so start at index 1 computing changes
for i, month in enumerate(total_list):
    if i > 0:
        month.append(month[1] - total_list[i-1][1])

# List of just the changes
changes = [month[2] for month in total_list[1:]]
        
great_increase = max(changes)
great_decrease = min(changes)

# Find corresponding months
for month in total_list[1:]:
    if month[2] == great_increase:
        great_increase_month = month[0]
    if month[2] == great_decrease:
        great_decrease_month = month[0]

average_revenue_change = sum(changes) / len(changes)

results += "Financial Analysis"
results += "\n----------------------------"
results += "\nTotal Months: " + str(total_months)
results += "\nTotal Revenue: " + format_currency(total_revenue)
results += "\nAverage Revenue Change: " + format_currency(average_revenue_change)
results += "\nGreatest Increase in Revenue: {} ({})".format(
    great_increase_month, format_currency(great_increase))
results += "\nGreatest Decrease in Revenue: {} ({})".format(
    great_decrease_month, format_currency(great_decrease))

print(results)

with open('stock_results.txt', 'w') as f:
    f.write(results)
