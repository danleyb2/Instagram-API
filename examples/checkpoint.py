from InstagramAPI import Checkpoint

username = ''  # // Your username
settingsPath = None
debug = False

c = Checkpoint(username, settingsPath, debug)

print("####################")
print("#                  #")
print("#    CHECKPOINT    #")
print("#                  #")
print("####################")

if username == '':
    print("\n\nYou have to set your username\n")
    exit()

token = c.doCheckpoint()

code = raw_input("\n\nCode you have received via mail: ").strip()

c.checkpointThird(code, token)

print("\n\nDone")
