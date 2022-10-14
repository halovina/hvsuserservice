import re 
def validate_new_password(password):
    flag = 0
    common_msg = "Password must contain at least 1 [a-z, A-Z, 0-9, _@$]"
    msg = ""
    while True:  
        if (len(password)<8):
            flag = -1
            msg = 'The password > 8 character'
            break
        elif not re.search("[a-z]", password):
            flag = -1
            msg = common_msg
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            msg = common_msg
            break
        elif not re.search("[0-9]", password):
            flag = -1
            msg = common_msg
            break
        elif not re.search("[_@$]", password):
            flag = -1
            msg = common_msg
            break
        else:
            flag = 0
            msg = 'Valid password'
            break
    
    if flag ==-1:
        return False, msg
    else:
        return True, msg