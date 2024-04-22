from twilio.rest import Client
import SMS_Keys as keys


def messageSender():

    client = Client(keys.account_sid,keys.auth_token)

    message = client.messages.create(
        body="TEST MESSAGE",
        from_=keys.twilio_number,
        to=keys.target_number
    )

    return message

print(messageSender().body)

#import subprocess


# message="TESTE 123"
# apiurl = "https://api.twilio.com/2010-04-01/Accounts/AC181d5aa4483d49b433293e0ecd022abf/Messages.json"
# method = "POST"
# to = f"--data-urlencode To={keys.target_number}"
# from_ = f"--data-urlencode From={keys.twilio_number}"
# access = f"-u {keys.account_sid}:{keys.auth_token}"
# msgbody = f"--data-urlencode Body={message}"
# sender = f"curl {apiurl} -X {method} {to} {from_} {msgbody} {access}"



# p = subprocess.Popen(sender, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)

# print(p)
