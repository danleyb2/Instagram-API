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


def do_get_username():
    new_username = raw_input("\n\nUsername: ").strip()
    check = r.checkUsername(new_username)
    return new_username, check.isAvailable()


username, is_available = do_get_username()
while not is_available:
    print "Username " + username + " not available, try with another one\n"
    username, is_available = do_get_username()

print "Username " + username + " is available\n\n"

password = raw_input("\nPassword: ").strip()


def do_get_email():
    new_email = raw_input("\n\nEmail: ").strip()
    check = r.checkEmail(new_email)
    return new_email, check.isAvailable()


email, is_available = do_get_email()
while not is_available:
    print "Email is not available, try with another one\n"
    email, is_available = do_get_email()

name = raw_input("\nName (Optional): ").strip()

result = r.createAccount(username, password, email)

if result.isAccountCreated():
    print 'Your account was successfully created! :)'
else:
    print "Error during registration."
