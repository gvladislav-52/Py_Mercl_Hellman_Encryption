import random

class Merkle_Hellman:
    def __init__(self):
        self.word = ""
        self.vector_first = []
        self.vector_second = []
        self.vec_str = []
        self.vector_encryption = []
        self.dec_vec = []
        self.decimalValues = []
        self.q = 0
        self.r = 0
        self.r_shtix = 0

    def to_binary(self, decimal):
        binary = ""
        while decimal > 0:
            binary = str(decimal % 2) + binary
            decimal //= 2
        while len(binary) < 7:
            binary = "0" + binary
        return binary

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def intilization_vector(self):
        for i in range(8):
            self.vector_first.append(2 ** i)

    def intilization_Q(self):
        self.q = random.randint(0, 100) + self.vector_first[-1]
        return self.q

    def intilization_R(self):
        self.r = random.randint(1, 100)
        while not self.is_prime(self.r):
            self.r = random.randint(1, 100)
        return self.r

    def setWord(self):
        import os
        self.word = os.getenv("temp")

    def getWord(self):
        return self.word

    def setVector_String(self):
        for i in range(len(self.getWord())):
            self.vec_str.append(self.to_binary(ord(self.getWord()[i])))

    def public_key(self):
        for c in self.vector_first:
            self.vector_second.append(c * self.r % self.q)

    def encryption(self):
        for str in self.vec_str:
            sum = 0
            for i in range(len(str)):
                if str[i] == '1':
                    sum += self.vector_second[i]
            self.vector_encryption.append(sum)

    def decryption(self):
        self.r_shtix = self.multiplicative_Inverse(self.r, self.q)
        self.vector_first.sort(reverse=True)

        temp = []
        for i in self.vector_encryption:
            temp.append(i * self.r_shtix % self.q)

        for i in range(len(temp)):
            index = ""
            while temp[i] != 0:
                for c in range(len(self.vector_first)):
                    if c == 0:
                        continue
                    if temp[i] < self.vector_first[c]:
                        index += "0"
                        continue
                    else:
                        index += "1"
                        temp[i] -= self.vector_first[c]
                index = index[::-1]
                self.dec_vec.append(index)

        self.binaryToDecimal(self.dec_vec)

    def gcd_Extended(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.gcd_Extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def multiplicative_Inverse(self, a, m):
        gcd, x, y = self.gcd_Extended(a, m)
        if gcd != 1:
            return -1
        else:
            return (x % m + m) % m

    def binaryToDecimal(self, binaryValues):
        for binary in binaryValues:
            decimal = 0
            base = 1
            for i in range(len(binary) - 1, -1, -1):
                if binary[i] == '1':
                    decimal += base
                base *= 2
            self.decimalValues.append(decimal)

    def function_Show(self):
        print("Q:\t", self.q)
        print("R:\t", self.r)
        print("R':\t", self.r_shtix)
        print("Vector_first:\t", self.vector_first)
        print("Vector_second:\t", self.vector_second)
        print("Word:\t\t", self.vec_str)
        print("Encryption:\t", self.vector_encryption)
        print("Bin string:\t", self.dec_vec)
        print("Decryption:\t", ''.join([chr(c) for c in self.decimalValues]))
