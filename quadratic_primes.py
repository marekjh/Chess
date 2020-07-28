# ***Problem description here: projecteuler.net/problem=27 ***


def check_prime(n, mode = "check"):
    i = 0
    
    while prime_list[i] <= n ** 0.5:
        if n % prime_list[i] == 0:
            return False
        i += 1
        
    if mode == "check":
        return True
    elif mode == "add":
        prime_list.append(n)

def quadratic_primes(primes):
    variables_list = []

    #This embedded loop takes care of constructing the list, starting with checking n = 1
    for b in primes:
        a_min = int(-(b + 1))
        
        for a in range(a_min, 999, 2):
            formula = (1 ** 2) + (a * 1) + b
            if check_prime(formula):
                variables_list.append((a, b))

    #This embedded loop will then check each (a, b) value pair and, for each subsequent n, determine
    #if n ** 2 + an + b is prime, getting rid of the pairs for whom this is not prime
    n = 2
    while len(variables_list) > 1:
        count = 0 #Accounts for how deletions affect variables_list's indexing
        
        for i in range(len(variables_list)):
            check = False
            (a, b) = variables_list[i - count]
            a_min = int(-((1 / n) * b + n))
            
            if a >= a_min:
                formula = (n ** 2) + (a * n) + b
                if check_prime(formula):
                    check = True
            
            if not check:
                del variables_list[i - count]
                count += 1

        n += 1
    
    (final_a, final_b) = variables_list[0]
    return final_a * final_b

prime_list = [2, 3]    
for num in range(5, 1000, 2):
    check_prime(num, mode = "add")

print(quadratic_primes(prime_list))
   
                
            
        
        
        
        
        
        
