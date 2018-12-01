import requests
import json 
import sys

API_ENDPOINT = 'http://data.meshpower.co.rw/accounts/api/v3/173077'
AUTHORIZATION = '9748c4c77f7b1ad96cadbacc72ee4b51'

#url = API_ENDPOINT.format()
r = requests.get(API_ENDPOINT, headers={'X-Authorization': AUTHORIZATION})
if not r.ok:
    print ('no connection found')

return r.json()


################################################################
                '*InvoiceNumber':'INV-{i}-{index}'.format(i=time.strftime("%Y%m%d"), index = sum(1 for line in sf)),
################################################################
