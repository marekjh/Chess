import math

def permute_nums(input_string, term):
    term -= 1
    
    running_list = list(input_string)
    running_list.sort()
    num_digits = len(running_list)
    
    output_string = ""
    
    for i in range(num_digits, 0, -1):
        permutations = math.factorial(i - 1)
        quotient = term // permutations
        
        output_string += str(running_list[quotient])
        del running_list[quotient]
        term -= (permutations * quotient)
    
    return output_string

try:
    digits = input("Enter a string of digits to permute (no spaces/punctuation): ")
    looking_for = int(input("Check the nth item in the lexicographically sorted list of permutations where n = "))
    
    test = int(digits)
except (TypeError, ValueError):
    print("\nFollow input instructions")
else:
    try:
        if looking_for < 1:
            test2 = int(" ")
        print("\n%s" % permute_nums(digits, looking_for))
    except (ValueError, IndexError):
        print("\n" + "n must be in the range [1, %d!]" % len(digits))
    
        
        
        
    
