import random
import string

def randomStringDigits(stringLength=8):
    """Generate a random string of letters and digits """
  
    lettersAndDigits = string.ascii_letters + string.digits
    val=''.join(random.choice(lettersAndDigits) for i in range(stringLength))
    return val