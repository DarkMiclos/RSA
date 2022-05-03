from operator import mod
import random #érdemes lehet a secretset biztosabb random szám generálás érdekében használni

def random_odd_big_number(size):
  big_number = random.getrandbits(size)
  big_number = big_number | (1 << size - 1) | 1 #hogy biztosan 1024 bites legyen, mivel lehetne az 1024-ik bit 0, utolsó bit 1
  return big_number

  

def miller_rabin_prime_test(prime_candidate, round):
    if(prime_candidate <= 1 or prime_candidate == 4):
      return False
    if(prime_candidate <= 3):
      return True
    m = prime_candidate - 1
    while(m % 2 == 0):
      m = m // 2
    for i in range(round):
      base = random.randint(2, prime_candidate - 2)
      x = quick_exponent(base, m, prime_candidate)
      if(x == 1 or x == prime_candidate - 1):
        continue
      while(m != prime_candidate - 1):
        x = (x ** 2) % prime_candidate
        m = int(m * 2) #ez az S(kör) miatt van itt
        if(x == 1):
          return False
        if(x == prime_candidate - 1):
          return True
      return False
    return True


def quick_exponent(base, exponent, modulo): #exponent = kitevő
    result = 1
    apow = base
    while(exponent != 0):
        if exponent & 0x01 == 0x01:
            result = (result * apow) % modulo
        exponent >>= 1
        apow = (apow * apow) % modulo
    return result

def modInverse(a, modulo): # multiplikatív inverz
    m0 = modulo
    x = [1, 0]
    if modulo == 1:
        return 0
    while a > 1:
        q = a//modulo
        temp = modulo
        modulo = a % modulo #remainder
        a = temp
        temp = x[1]
        x[1] = x[0] - q * x[1]
        x[0] = temp
    if x[0] < 0:
        x[0] += m0
    return x[0]

def chinese_remainder_theorem(p, q, c, d): #Rsa specific
  d_remainder_p = d % (p - 1)
  d_remainder_q = d % (q - 1)
  c_remainder_p = c % p
  c_remainder_q = c % q
  x1 = quick_exponent(c_remainder_p, d_remainder_p, p)
  x2 = quick_exponent(c_remainder_q, d_remainder_q, q)
  y1 = modInverse(q, p)
  y2 = modInverse(p, q)
  return (q * x1 * y1 + p * x2 * y2) % (p * q)


def rsa(message, key_size):
  print("Key Size:", key_size)
  e = 2 ** 16 + 1 #Common value 65537
  n = 0
  while n.bit_length() != key_size:
    p = 4
    q = 4
    while not miller_rabin_prime_test(p, 128):
      p = random_odd_big_number(key_size // 2)
    while not miller_rabin_prime_test(q, 128):
      q = random_odd_big_number(key_size // 2)
    n = p * q
  print("P:", p)
  print("Q:", q)
  print("N:", n)
  fi_n = (p - 1) * (q - 1)
  print("Fi_n:", fi_n)
  d = modInverse(e, fi_n)
  print("D:", d)
  c = quick_exponent(message, e, n)
  print("Encrypted message:", c)
  m = quick_exponent(c, d, n)
  print("Decripted message:", m)
  m2 = chinese_remainder_theorem(p, q, c, d)
  print("Decrypted message with CRT:", m2)


#print(random_odd_big_number())
#print(miller_rabin_prime_test(7741, 128))
#print(modInverse(112,65))
rsa(49, 1024)
rsa(97, 2048)
#rsa(42, 4096)