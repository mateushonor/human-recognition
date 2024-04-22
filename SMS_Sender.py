# import twilio
# from twilio.rest import Client
# import SMS_Keys as keys


# def messageSender():

#     client = Client(keys.account_sid,keys.auth_token)

#     message = client.messages.create(
#         body="TEST MESSAGE",
#         from_=keys.twilio_number,
#         to=keys.target_number
#     )

#     return message

# print(messageSender().body)

import subprocess
import sys

subprocess.Popen("curl https://api.twilio.com/2010-04-01/Accounts/AC181d5aa4483d49b433293e0ecd022abf/Messages.json -X POST --data-urlencode To=+5534999062849 --data-urlencode From=+12512701223 --data-urlencode Body=incurll -u AC181d5aa4483d49b433293e0ecd022abf:70faadb9a1cb0ccf799daf05000eeb56", stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
