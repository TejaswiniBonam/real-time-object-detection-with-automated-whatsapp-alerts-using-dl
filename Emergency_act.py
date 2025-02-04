from twilio.rest import Client
#account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
#auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
X = 'A-Ca40ab86502b72a1ee2e3b5ef28195c53'
Y = 'c-a3b32aa91b86d88a021915f72d8b1b9'

client = Client(X, Y)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  to='whatsapp:+919951280286',
  body= 'EMERGENCY AT House No 123 Main Street, Anytown, CA 12345',
  
)

print(message.sid)