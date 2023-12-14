
def Convert(message):#function converts information sent by arduino to information that ca be entered in the database.
    #when message is recieved as a comma and colon seperated string uses an inline for loop to
    #split the string at every ':' and ',' and convert it to a dictionary
    message_dict=dict(u.split(":") for u in message.split(","))
    #all values in the dictionary are of type String. the following for loop finds the values that need to be integers and converts them
    for item in message_dict:
        if item == "id" or item == "HR" or item == "Rndsfired":
            message_dict[item]=int(message_dict[item])
        else:
            message_dict[item]=message_dict[item]
    return message_dict#returns the dictionary of values parsed from the string.
