from InstagramAPI import Checkpoint

debug = True


print("####################")
print("#                  #")
print("#    CHECKPOINT    #")
print("#                  #")
print("####################")

username = raw_input("\n\nYour username: ").strip()

if username == '':
    print("\n\nYou have to set your username\n")
    exit()

settingsPath = raw_input("\n\nYour settings path folder ([ENTER] if dedault): ").strip()
print settingsPath
if settingsPath == '':
    settingsPath = None

c = Checkpoint(username, settingsPath, debug)

token = c.doCheckpoint()

code = raw_input("\n\nCode you have received via mail: ").strip()

c.checkpointThird(code, token)

print("\n\nDone")
