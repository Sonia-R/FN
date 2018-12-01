import csv
from datetime import datetime
import os 
import re
import pandas as pd
import datetime
import time
import logging
import requests


HAVANAO_FILE = '/home/sonia/Desktop/Files/partners.csv'
SALES_FILE_PATH = '/home/sonia/Desktop/Files/'
API_ENDPOINT = 'http://data.meshpower.co.rw/accounts/api/v3/{account}'
AUTHORIZATION = '9748c4c77f7b1ad96cadbacc72ee4b51'


class Transactions_record:
    def read_Partners_File(self, fp):
        transactions_list = []
        mydict ={}
        with open (fp, mode = 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            description_template = "Energy sales,""{p} From {k}"
            for row in csv_reader:
                mydict['Account_number'] = re.findall(r'\d+',row ['To'])[0]
                mydict['amount'] = row['Amount']
                mydict['PaymentSP'] = 'MTN' 
                mydict['date'] = datetime.datetime.strptime(row['Date'],'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y')
                mydict['reference'] = row['External Transaction Id']
                mydict['Quantity'] = 1
                mydict['description'] = description_template.format(p=row['To'],k =row['From Name'])  
                transactions_list.append(mydict.copy())
            return transactions_list

    
    def get_account_info(self, acc):
        url = API_ENDPOINT.format(account = acc)
        r = requests.get(url , headers ={'X-Authorization' : AUTHORIZATION})
        if not r.ok:
            return r.status_code
        return r.json()

    def create_sales_csv(self, path):
        timestr = time.strftime("%Y%m%d")
        try:
            return path+'Partners_SalesInvoice-'+timestr+'.csv'
        except Exception as e:
            logging.info('Error in creating the file: %s', str(e))


def main():
    timestr = time.strftime("%Y%m%d")
    TV_accounts_dict={}
    TV_accounts_list=[]
    tr = Transactions_record()
    sf = tr.create_sales_csv(SALES_FILE_PATH)
    tr_dict = tr.read_Partners_File(HAVANAO_FILE)

    # start writing to the sales file
    with open(sf, 'wb') as f:  
        column_headers = ['ContactName','POAddressLine1',
                    'POAddressLine2','POAddressLine3','POAddressLine4',
                    'POCity','PORegion','POPostalCode','POCountry','*InvoiceNumber',
                    'Reference','*InvoiceDate','*DueDate','Total','InventoryItemCode',
                    'Description','*Quantity','*UnitAmount',
                    'Discount','*AccountCode','*TaxType',
                    'TaxAmount','TrackingName1','TrackingOption1',
                    'TrackingName2','TrackingOption2','Currency']
        w = csv.DictWriter(f, column_headers)
        w.writeheader()
        for i in tr_dict:
            if i['Account_number'].endswith('TV'):
                TV_accounts_dict['accounts']=i['Account_number']
                TV_accounts_dict['amount'] =i['amount']
                TV_accounts_list.append(TV_accounts_dict.copy())
                with open (SALES_FILE_PATH+'Parteners_TV_Accounts'+timestr+'.csv','wb')as tv_acc_file:
                    k = csv.DictWriter(tv_acc_file,['TV_Accounts', 'Amount'])
                    k.writeheader()
                    for p in TV_accounts_list:
                        k.writerow({'TV_Accounts': p['accounts'],'Amount':p['amount']}) 
            acc_info = tr.get_account_info(i['Account_number'])
            w.writerow({
                '*InvoiceNumber':'{s} INV-{i}'.format(s='MTN', i=time.strftime("%Y%m%d")),
                'Reference': i['reference'],
                '*InvoiceDate':i['date'],
                '*DueDate': i['date'],
                '*Quantity': i['Quantity'],
                '*UnitAmount': i['amount'],
                '*AccountCode':'P&L 1.1',
                '*TaxType':'Sale Exempt (0%)',
                'ContactName':'Energy Sales {a} '.format(a ='MTN cash'),
                'Description':i['description'],
                'TrackingName2': 'SITES',
                'TrackingOption2':acc_info['site']
            })       
main()



   