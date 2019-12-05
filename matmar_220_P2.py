def blood_pressure(systolic, diastolic):
	mean_pressure = (systolic + 2 * diastolic) / 3 
	#precalculates mean pressure

	if (systolic > 180) or (diastolic > 120):
		risk_level = 1.4
	elif (systolic >= 140) or (diastolic >= 90):
		risk_level = 1.3
	elif (systolic >= 130) or (diastolic >= 80):
		risk_level = 1.2
	elif (systolic >= 120) and (diastolic < 80):
		risk_level = 1.1
	elif (systolic < 120) and (diastolic < 80):
		risk_level = 1.0
	#runs systolic and diastolic from highest to lowest risk levels
	
	combined_risk = round(float(risk_level * mean_pressure), 2)
	#multiplies risk level and mean pressure, rounds to tens place
	
	return combined_risk



def standard_BMI(weight, height, ISU):
	if ISU == True:	   #ISU will calculate as 'normal'
		BMI = round((weight)/(height**2), 2)
		return BMI  
	else:    #converts to ISU then calculates
		new_weight = weight * (1/35)
		new_height = height * 0.025
		BMI = round((new_weight)/(new_height**2), 2)
		return BMI



def BMI_chart(weight, height, age, gender):
#checks BMI from highest to lowest for adults	
	if age >= 18:
		if standard_BMI(weight, height, True) > 30:
			return 'obese'
		elif ((standard_BMI(weight, height, True) > 25) and 
		(standard_BMI(weight, height, True) <= 30)):
			return 'overweight'
		elif ((standard_BMI(weight, height, True) >= 18.5) and  
		(standard_BMI(weight, height, True) <= 25)):
			return 'normal'
		elif standard_BMI(weight, height, True) < 18.5:
			return 'underweight'

#checks for male children
	elif gender == 'male':
		if standard_BMI(weight, height, True) > 22:
			return 'obese'
		elif ((standard_BMI(weight, height, True) > 19) and 
		(standard_BMI(weight, height, True) <=22)):
			return 'overweight'
		elif ((standard_BMI(weight, height, True) >= 14) and 
		(standard_BMI(weight, height, True) <= 29)):
			return 'normal'
		elif standard_BMI(weight, height, True) < 14:
			return 'underweight'

#checks for female children
	elif gender == 'female':
		if standard_BMI(weight, height, True) > 23:
			return 'obese'
		elif ((standard_BMI(weight, height, True) > 20) and 
		(standard_BMI(weight, height, True) <= 23)):
			return 'overweight'
		elif ((standard_BMI(weight, height, True) >= 15) and 
		(standard_BMI(weight, height, True) <= 30)):
			return 'normal'
		elif standard_BMI(weight, height, True) < 15:
			return 'underweight'


def HCT(red_cells, total_cells, age, gender):
	if total_cells < 1000000:  #checks if total cells are less than million
		return False
	if age >= 18:  	#branches adults from children
		if gender == 'male': #male adult
			if (((red_cells / total_cells) * 100 < 40.7) or 
			(red_cells / total_cells) * 100 > 50.3):
				return False

			else:
				return True
		if gender == 'female': #female adult
			if (((red_cells / total_cells) * 100 < 36.1) or 
			(red_cells / total_cells) * 100 > 44.3):
				return False

			else:
				return True
	else: #children, male and female have same math
		if (round(((red_cells / total_cells)) * 100 < 36) or 
			((red_cells / total_cells)) * 100 > 40):
			return False
		else:
			return True


def LDL(total, HDL, trig, age, gender):
#sets the calculations for base k and LDL
	k = 0.2
	low_density = total - HDL - k * trig
	

#equation for elevated trig and k
	if (total > 250) and (trig > 43.5):
		k = 0.19
		if total >= 260:
			new_k = ((total - 250) // 10) * 0.01
			k = k - new_k

	elif (trig <= 11.3) or (trig >= 43.5):
		k = 0
	
	#LDL for adults	
	if age >= 18:
		if low_density < 120: #with lower LDL rate
			risk = 0
			return risk
			if gender == 'male':
				if HDL < 40:
					risk = risk + 1
					return int(risk)
				if HDL > 70:
					if risk >= 1:
						risk = risk - 1
						return int(risk)
			if gender == 'female':
				if HDL < 50:
					if risk < 5:
						risk = risk + 1
						return int(risk)
				if HDL > 70:
					if risk >= 1:
						risk = risk - 1
						return int(risk)
			else:
				return int(risk)

		elif low_density < 220: #with higher LDL rates
			if gender == 'male':
				risk = 1
				adult_risk = (((low_density - 120)) // 20)
				risk = risk + adult_risk
				if HDL < 40:
					risk = risk + 1
					return int(risk)
				if HDL > 70:
					risk = risk - 1
					return int(risk)
				return int(risk)
			if gender == 'female':
				risk = 1
				adult_risk = (((low_density - 120)) // 20)
				risk = risk + adult_risk
				if HDL < 50:
					if risk < 5:
						risk = risk + 1
						return int(risk)
				if HDL > 70:
					if risk > -1:
						risk = risk - 1
						return int(risk)
				return int(risk)

	#LDL for children
	if age < 18:
		if low_density < 100:
			risk = 0
			return int(risk)
		else:
			if low_density < 170:
				risk = 1
				child_risk = ((low_density - 100) // 15)
				risk = risk + child_risk
				return int(risk)







