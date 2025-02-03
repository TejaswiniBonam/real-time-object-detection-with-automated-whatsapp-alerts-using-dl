from twilio.rest import Client
account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  to='whatsapp:+919951280286',
  body= 'EMERGENCY AT XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  
)

print(message.sid)