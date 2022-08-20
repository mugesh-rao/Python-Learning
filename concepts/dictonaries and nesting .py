
stud_score = {
    "Vijay" : 81,
    "Mugesh" : 78,
    "Rao" : 60,
    "Susan" : 100,
}
stud_grades = {}

for student in stud_score:
    score = stud_score[student]
    if score > 90 :
     stud_grades[student] = "Outsanding"
    elif score > 80 :
     stud_grades[student] = "Expexctation"
    elif score > 70 :
     stud_grades[student] = "acceptable"
    else:
     stud_grades[student] = "Fail"
    
print(stud_grades)