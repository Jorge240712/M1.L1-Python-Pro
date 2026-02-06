import random
elements = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
length = int(input("Ingrese la longitud de la contraseña:"))
password = ""
for i in range(length):
    password += random.choice(elements)
print("Tu contraseña:", password)
