# class Microwave:
#     def __init__ (self, brand, power):
#         self.brand = brand
#         self.power = power
#         self.turned_on = False
#     def turning_on(self):
#         if self.turned_on:
#             print (f'Microwave of brand {self.brand} with {self.power} power is already ON')
#         else:
#             self.turned_on = True
#             print (f'Microwave of brand {self.brand} with {self.power} power is now ON')

#     def __str__(self):
#         return f'Microwave(brand={self.brand}, power={self.power}, turned_on={self.turned_on})'
    
# M1 = Microwave('LG', 800)
# print(M1)
# M1.turning_on()
# print(M1)
import sys

name = " ".join(sys.argv[1:])

def greet(name):
    return f"Hello, {name} !"

print(greet(name))