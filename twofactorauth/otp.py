from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits

customer_id = "A7A625FD-AFE4-4E3D-AE51-DEBF9CCAA1BA"
api_key = "DuhC8MQ71NO89g2eamglt64gNN31+luy0TShI4zXn6K5OEbNRf98FSC5lmUPr5pf7zZNJlKzooY0b60hki4fKQ=="

phone_number = "+254702029382"
verify_code = random_with_n_digits(5)
message = "Your code is {}".format(verify_code)
message_type = "OTP"

messaging = MessagingClient(customer_id, api_key)
response = messaging.message(phone_number, message, message_type)
print(response.json)

user_entered_verify_code = input("Please enter the verification code you were sent: ")

if verify_code == user_entered_verify_code.strip():
    print("Your code is correct.")
else:
    print("Your code is incorrect.")