#pH test
def chemical_strength(pH):
    if (float(pH) < 0.0) or (float(pH)> 14.0):
        strength = "bad measurement"
        return strength
    if (float(pH) <= 1.0):
        strength = "very strong acid"
        return strength
    if (float(pH) > 1.0) and (float(pH) < 4.0):
        strength = "strong acid"
        return strength
    if (float(pH) == 4.0):
        strength = "plain acid"
        return strength
    if (float(pH) > 4.0) and (float(pH) < 6.0):
        strength = "weak acid"
        return strength
    if (float(pH) >= 6.0) and (float(pH) < 7.0):
        strength = "very weak acid"
        return strength
    if (float(pH) <= 8.0) and (float(pH) > 7.0):
        strength = "very weak base"
        return strength
    if (float(pH) > 8.0) and (float(pH) < 10.0):
        strength = "weak base"
        return strength
    if (float(pH) == 10.0):
        strength = "plain base"
        return strength
    if (float(pH) > 10.0) and (float(pH) < 13.0):
        strength = "strong base"
        return strength
    if (float(pH) >= 13.0):
        strength = "very strong base"
        return strength
    if (float(pH) == 7.0):
        strength = "neutral"
        return strength

#light switch
def light_status(s1, s2):
    if (int(s1) > 100 or int(s1) <= 0) or (int(s2) > 100 or int(s2) <= 0):
        status = "invalid switch"
        return status
    if int(s1) + int(s2) > 200:
        status = "invalid switch"
        return status
    if int(s1) + int(s2) < 50:
        status = "off"
        return status
    if int(s1) + int(s2) > 50:
        status = "on"
        return status
    if (int(s1) < 50) or (int(s2) < 50):
        status = "off"
    #if abs(s1-s2) == 50
     #   status = "on"
      #  return status