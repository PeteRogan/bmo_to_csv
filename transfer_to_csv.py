#Note: script fails for more than nine digit dollar values

import tika
tika.initVM()
from tika import parser
import os
import csv
import re

class csv_class:
    def __init__(self):
        self.file_name = 'eStatement.csv'
        self.fields = ['Date', 'Total_Deducted', 'Total_Added', 'Closing_Balance', '', ''] #Note: empty values to separate totals from transactions
        self.rows = []
        self.account_number = int(input("Enter account number: "))

    def add_row(self, file_name, text):
        row = []

        #Extract date from name
        date = file_name[11:-4]
        row.append(date)

        match = re.search('# ' + self.account_number + ' (\d*,*\d*,*\d*.\d{2}) (\d*,*\d*,*\d*.\d{2}) (\d*,*\d*,*\d*.\d{2}) (\d*,*\d*,*\d*.\d{2})', text)

        #Extract Total_Deducted
        total_deducted = match.group(2).replace(',', '')
        row.append(float(total_deducted))

        #Extract Total_Added
        total_added = match.group(3).replace(',', '')
        row.append(float(total_added))

        #Extract Closing_Balance
        closing_balance = match.group(4).replace(',', '')
        row.append(float(closing_balance))

        #Extract transactions
        purchase_dict = {}
        text_lines = text.split('\n')
        for line in text_lines:
            regex = re.search('.{3} \d{2} (.*) (\d*,*\d*,*\d*.\d{2}) (\d*,*\d*,*\d*.\d{2})$', line)
            if regex:
                name = regex.group(1) #Extract name
                cost_str = regex.group(2).replace(',', '') #Extract cost and convert to float
                cost = float(cost_str)

                if name not in purchase_dict:
                    purchase_dict.update({name: cost}) #If name not in dictionary, create new entry
                else:
                    purchase_dict[name] += cost #Otherwise add value to existing entry

        #Add transactions to row
        for name in purchase_dict:
            if name not in self.fields: #If name not in list of fields, append list
                self.fields.append(name)

            column_index = self.fields.index(name) #Get index of field "name"
            while len(row) - 1 < column_index: #Append row with empty columns until index not out of range
                row.append(None)
            row[column_index] = purchase_dict[name]

        #Add row to csv class
        self.rows.append(row)

    def write_to_file(self):
        with open(self.file_name, 'w') as csv_file:
            csvwriter = csv.writer(csv_file)
            csvwriter.writerow(self.fields)
            csvwriter.writerows(self.rows)

stmt_dir = "./Input/Debit/"
csv_obj = csv_class()
name_list = sorted(os.listdir(stmt_dir))
for file_name in name_list:
    text = parser.from_file(stmt_dir + file_name)
    csv_obj.add_row(file_name, text["content"])

csv_obj.write_to_file()