from twilio.rest import Client

account_sid = 'ACf67a578e0e882054c2e6bcf9b2635a86'
auth_token = '984887fb165669de4af021f9d0830ea9'

client = Client(account_sid, auth_token)

message = client.api.account.messages.create(
    to = '+12409181753',
    from_ ='+12182315603',
    body = "Test message from classified")
