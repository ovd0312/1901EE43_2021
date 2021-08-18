def is_Meraki(n):
    prev_digit = n%10
    n = n//10
    while n>0:
        curr_digit = n%10
        if abs(curr_digit-prev_digit)!=1:
            return False
        n = n//10;
        prev_digit = curr_digit

    return True;



input = [12, 14, 56, 78, 98, 54, 678, 134, 789, 0, 7, 5, 123, 45, 76345, 987654321]

Meraki_count = 0
Not_Meraki_count = 0

for num in input:
    if is_Meraki(num):
        print("Yes -", num, "is a Meraki Number")
        Meraki_count += 1
    else:
        print("No  -", num, "is NOT a Meraki Number")
        Not_Meraki_count += 1

print("The input list contains",Meraki_count,"Meraki and", Not_Meraki_count,"non Meraki numbers")

