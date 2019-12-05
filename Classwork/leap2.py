################

#Mostafa Atmar
year = int(input("Enter year.\n"))
if year % 4 == 0:
	print("That year is a leap year.")
elif year % 100 == 0:
	print("That year is a leap year.")
elif year % 400 == 0:
	print("That year is a leap year.")
else: print("That year is not a leap year.")