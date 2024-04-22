from twilio.rest import Client
import SMS_Keys as keys


def messageSender():

    client = Client(keys.account,keys.auth_token)

    message = client.messages.create(
        body="TEST MESSAGE",
        from_=keys.twilio_number,
        to=keys.target_number
    )

    return message

print(messageSender().body)
