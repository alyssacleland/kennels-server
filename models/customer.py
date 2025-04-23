class Customer():

    def __init__(self, id, name, address, email="", password=""):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.password = password

# Before you implement the method to query the database by the email address provided by the client, you need to update your Customer model to implement default parameter values.

# The reason for this is because when create some Customer instances to send back the client, sending the password in the response is a bad idea. Also, there's no reason to send the email in the case since the client obviously already has the email address to reference.

# Now, you can create an instance of a Customer with only three positional arguments instead of needing all 5.
