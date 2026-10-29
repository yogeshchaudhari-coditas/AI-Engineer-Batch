"""

A small e-commerce company gets customer support emails in a shared inbox. A person reads each one, decides what it’s about, and forwards it to the right colleague. This is slow, and urgent issues get buried.
Build a system that reads customer emails from a folder called emails and does the following for each one. It doesn’t need to connect to a real inbox.


Classify the email as one of five categories: refund request, order status, product complaint, account/login issue, or other.
Assign a priority of high, medium, or low. An email about a payment problem, a threat to cancel or leave, or a safety concern must be high.
Look up the customer’s order in the company’s order data. Create this data yourself as a simple file of 10 to 15 fake orders, each with an order ID, customer email, item, amount, status, and order date. Use the order wherever it is relevant to the email.
Draft a polite reply that cites the customer’s actual order details. The reply must not promise a refund or a delivery date that the order data doesn’t support.
Do not draft a reply if the email is vague, abusive, or refers to an order that doesn’t exist, or if the system isn’t confident in its classification. Flag the email for human review with a one-line reason.
Output a structured result for each email that a downstream system can consume. It should contain the category, priority, whether an order was found, the drafted reply or escalation flag, and the reason.

1. refund request
2. order status
3. product complaint
4. account/login issue
5. other

Priority:
1. High
2. Medium
3. Low
"""

import csv
from datetime import datetime
from enum import Enum

class Service_Email(Enum):
    SUPPORT = "support@shop.example"
    PAYMENT = "payment.support@shop.example"
    ORDER_STATUS = "order.status@shop.example"
    PRODUCT_COMPLAINT = "product.complaint@shop.example"
    LOGIN_ISSUE = "login.support@shop.example"
    OTHER = "other.support@shop.example"

class EmailPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Read CSV Data
filename = "./orders.csv"
fields = []  # Column names
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:    
        rows.append(row)

# print (f">>>>>>Order Data:{rows}")



# Email Data Reader
def read_emails(email_file_name: str="email_001"):

    with open(f"./emails/{email_file_name}.txt", "r", encoding="utf-8") as file:
        content = file.read()
        email_lines = content.splitlines()
        print(email_lines)
        
        # Fetching customer name and email
        customer_name_email = email_lines[0]
        cust_fname = customer_name_email.split()[1]
        cust_lname = customer_name_email.split()[2]
        cust_email = customer_name_email.split()[len(customer_name_email.split()) - 1]

        # Fetched Order ID from email
        #TODO: Need to implement a better way to fetch order id from email body
        order_id = email_lines[7]

        # print(f"Customer Name: {cust_fname} {cust_lname}, Email: {cust_email}, Order ID: {order_id}")

        email_lines = content.splitlines()
    return cust_fname, cust_lname, cust_email, order_id, email_lines

def forward_email_to_service(customer_name, customer_email, order_id, category):

    if category == "PAYMENT":
        service_email = Service_Email.PAYMENT.value
    elif category == "ORDER_STATUS":
        service_email = Service_Email.ORDER_STATUS.value
    elif category == "PRODUCT_COMPLAINT":
        service_email = Service_Email.PRODUCT_COMPLAINT.value
    elif category == "LOGIN_ISSUE":
        service_email = Service_Email.LOGIN_ISSUE.value
    else:
        service_email = Service_Email.OTHER.value

    from_email = Service_Email.SUPPORT.value
    subject = f"Customer Support Email - Order ID: {order_id} - Category: {category} - Priority: {priority}"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mail_body = f"""
        Hi {service_name},
        We have received an email from {customer_name} ({customer_email}) regarding order ID: {order_id}.
        The email has been classified under the category: {category} with a priority of {priority}.
        Please review and take necessary action.
        Thanks,
        Support Team
        """
    print(">>>>>>>> Forwarding Email to Service Team <<<<<<<<")
    print(
        f"""
        From: {from_email}
        To: {service_email}
        Subject: {subject}
        Date: {current_date}
        Body:
        {mail_body}
        """
    )

def email_classification(email_content):
    # Placeholder for email classification logic
    # This function should analyze the email content and return a category and priority
    # For now, we will return a dummy category and priority
    return "ORDER_STATUS", EmailPriority.HIGH.value

if __name__ == "__main__":
    # Read Email
    cust_fname, cust_lname, cust_email, order_id, email_lines = read_emails("email_001")

    # Check for order existence
    order_found = any(order_id in row for row in rows)

    if order_found:
        # Email Classification
        category, priority = email_classification(email_lines)

        # Forward Email to Service Team
        forward_email_to_service(f"{cust_fname} {cust_lname}", cust_email, order_id, category)

    

