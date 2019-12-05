#---------------------------------------------------------------------------
# Name: Mostafa Atmar
# Project 1
# Due Date: 9/8/2019
#---------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that
# violates the ethical guidelines set forth by professor and class syllabus.
#---------------------------------------------------------------------------

print("Welcome to the Cake Slice Program!")

#from lines 3-8, defines dimensions of whole cake and each slice
cake_Type = input("What kind of cake did you make? ") 
cake_Length = int(input("How long is the cake in centimeters? "))
cake_Width = int(input("How wide is the cake in centimeters? "))
cut_Length = int(input("How long will you cut your slices in centimeters? "))
cut_Width = int(input("How wide will you cut your slices in centimeters? "))

surface_area = cake_Length * cake_Width

#calculates amount of slices by floor division of each row/column
num_slice_rows = int(cake_Length // cut_Length)
num_slice_cols = int(cake_Width // cut_Width)

#multiplies them to get total amount of slices
num_slices = num_slice_rows * num_slice_cols
slices_surface_area = num_slices * (cut_Length * cut_Width)

#percentage of the slices from the cake as a fraction
cake_percentage = round(float((slices_surface_area / surface_area) * 100))

#calculates waste by subtracting surface areas
waste = surface_area - slices_surface_area
waste_prcnt = round(float(((surface_area - slices_surface_area) 
	/ surface_area) * 100))

#edge slice calculated with perimeter, center is slices - edge
edge = int(2 * num_slice_cols) + int(2 * num_slice_rows)
edge_slices = edge - 4
center_slices = num_slices - edge_slices

#prints results
print("Your cake has a surface area of" + " " + str(surface_area) + 
	" " + "square centimeters.")
print("You can cut" + " " + str(num_slices) + " " + "total" + " " + 
	str(cut_Length) + "x" + str(cut_Width) + " " + "slices of cake.")

print("These slice dimensions can cut a total of", slices_surface_area, 
	"square centimeters, or" + " " + str(cake_percentage) + "%, of the cake.")
print("These slice dimensions will waste", waste, "square centimeters, or" + " " +
	 str(waste_prcnt) + "%, of the cake.")
print("There will be", edge_slices, "edge pieces, and", center_slices,
	 "center pieces of cake.")
print("Enjoy your", cake_Type, "cake!")


