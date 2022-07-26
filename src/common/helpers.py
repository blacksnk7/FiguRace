def check_integer(value):
    '''
    This function simply checks if a given value is an integer or not. If it is, the function returns the same value that was given.
    If it isnt, the retruned value will be a string which explains the type of error encountered.
    '''
    try:
        int(value)
    except ValueError:
        value = 'error'
    return value

def check_positive_value(value):
    '''
    This function checks if a value is an integer and then checks if said value is equal or greater than 0.
    '''
    value = check_integer(value)
    if(value != 'error'):
        if (int(value) < 0):
            value = 'error'
            print("here")
    return value
