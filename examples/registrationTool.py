import InstagramAPI

# // NOTE: THIS IS A CLI TOOL
# /// DEBUG MODE ///
debug = False

r = InstagramAPI.InstagramRegistration(debug)

print "###########################"
print "#                         #"
print "# Instagram Register Tool #"
print "#                         #"
print "###########################"


def do():
    new_username = raw_input("\n\nUsername: ").strip()
    check = r.checkUsername(new_username)
    return new_username, check['available']


username, is_available = do()
while not is_available:
    print "Username " + username + " not available, try with another one\n"
    username, is_available = do()

print "Username " + username + " is available\n\n"

password = raw_input("\nPassword: ").strip()

email = raw_input("\nEmail: ").strip()

result = r.createAccount(username, password, email)
if hasattr(result, 'account_created') and result['account_created'] == True:
    print 'Your account was successfully created! :)'
