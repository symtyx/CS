class Student:
	def __init__(self,first_name,last_name,id,gpa):
		self.first_name = first_name
		self.last_name = last_name
		self.id = id
		self.gpa = gpa
	
	def printable(self, self.first_name, self.last_name, self.id, self.gpa):
		return self.first_name + " " + self.last_name + " " + str(self.id) + " " + str(self.gpa)

	def gpa_update(self, x):
		self.gpa += x

	def __eq__(self,other):
        if self.GPA == other.GPA:
            return True
        else:
            return False
            
	def __gt__(self, other):
		if self.gpa > self.other:
			return True
		else:
			return False
	
	def __lt__(self,other):
		if self.gpa < self.other:
			return True
		else:
			return False

class myClass:
	def __init__(self,students):
		self.students = []
	def students(self):
	