
def convert_to_dict(message):
    """
    Convert information sent by Arduino to a dictionary.

    Parameters:
    - message (str): A comma and colon-separated string.

    Returns:
    - dict: A dictionary containing parsed values from the string.
    """
   
    #split the string at every ':' and ',' and convert it to a dictionary
    message_dict=dict(u.split(":") for u in message.split(","))
    #all values in the dictionary are of type String. the following for loop finds the values that need to be integers and converts them
    for item in message_dict:
        if item == "id" or item == "HR" or item == "Rndsfired":
            message_dict[item]=int(message_dict[item])
        else:
            message_dict[item]=message_dict[item]
    return message_dict#returns the dictionary of values parsed from the string.
