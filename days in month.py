
def is_leap(year):
    if year%4 == 0:
        if year % 100 == 0:
            if year % 400 :
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def days_in_month(year , month):
    if month > 12 or month < 1:
        return "Enter Valid data"
    month_days = [31,28,31,30,30,31,30,31,30,31,30,31]

    if is_leap and month==2:
        return 29
    else:
        return month_days[month - 1]

# No Need to Change Anything
year = int(input("Enter a Year "))
month = int(input("Enter a month "))
days = days_in_month(year,month)
print(days)