lookup = "abcdefghijklmnopqrstuvwxyz" * 2                                   #the alphabet (twice)
password_check = "kgxmwpbpuqtorzapjhfmebmccvwycyvewpxiheifvnuqsrgexl"       #what the password is checked against
a_test = "addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj"               #the result of what a password consisting of all a's is transformed to
offset = []
password = ""

# get the offset applied to each character
for char in a_test:
    offset.append(lookup.index(char))

#subtract the offset from the position of each character in password_check to find the character needed before the transformation
for i in range(len(password_check)):
    password += lookup[lookup.index(password_check[i])+26-offset[i]]

print(password)
