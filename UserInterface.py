from sys import argv
import re

#Creates user options
def menu():
    print "\nWelcome to Twitter Snitch\n"
    print "Please Select One Of The Following Options"
    print "1) Run Twitter Snitch"
    print "2) Add Twitter Name(s) To List"
    print "3) Add Keyword(s) To List"
    print "4) Add E-Mail Recipient(s) To List"
    print "5) Exit\n"
    selection = int(raw_input("Please Make Selection Or Press ENTER For Default (1)") or 1)
    checkSelection(selection)

def checkEmail(newRecip):
	if len(newRecip) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", newRecip) != None:
			return 1
	return 0

#checks Selection
def checkSelection(selection):

#if selection is 1 run full script
    if selection == 1:
        from TwitterSnitch import loopy
	loopy()

#elif selection is 2 append user list, check for @ and remove spaces
#call menu if interupted
    elif selection == 2:
        from TwitterSnitch import loadUsers
	nameList, load_twit_usrs = loadUsers()
        with open(load_twit_usrs, "a") as users:
            try:
                while True:
					newName = raw_input("\nPlease Enter Name\n")
					newName = newName.replace(" ","")
					if not "@" in newName: newName = "@" + newName
					if "" in newName:
						print "Invalid Entry"
					else:
						users.write("\n")
						users.write(newName)
						users.flush()
            except KeyboardInterrupt:
				menu()

#elif selection is 3 append keywords
#call menu if interupted
    elif selection == 3:
        from TwitterSnitch import loadKeywords
	loadKeywords, load_Keywords = loadKeywords()
        with open(load_Keywords,"a") as keywords:
            try:
                while True:
					newKey = raw_input("\nPlease Enter Keyword\n")
					newKey = newKey.replace(" ","")
					if "" in newKey:
						print "Invalid Entry"
					else:
						keywords.write("\n")
						keywords.write(newKey)
						keywords.flush()
            except KeyboardInterrupt:
                menu()

#elif` selection is 4 append recipients
#call menu if interupted
    elif selection == 4:
        from TwitterSnitch import loadRecipients
	recipientList, load_recipients = loadRecipients()
        with open(load_recipients,"a") as recipients:
            try:
                while True:
				newRecip = raw_input("\nPlease Enter Recipient\n")
				checkMail = checkEmail(newRecip)
				if checkMail is 0:
					print "Invalid Entry"
				else:
					recipients.write("\n")
					recipients.write(newRecip)
					recipients.flush()
            except KeyboardInterrupt:
                menu()

    elif selection == 5:
        exit
#end cehckSelection()

#calls menu to start
menu()