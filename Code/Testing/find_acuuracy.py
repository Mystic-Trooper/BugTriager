
A=["mike_wilson@oti.com",
"james_moody@oti.com",
 "dirk_baeumer@oti.com",
 "adam_kiezun@oti.com",
 "randy_giffen@oti.com",
 "knut_radloff@oti.com",
 "daniel_megert@oti.com",
 "erich_gamma@oti.com",
] 
B = ["mike_wilson@oti.com",
"james_moody@oti.com",
 "dirk_baeumer@oti.com",
 "adam_kiezun@oti.com",
 "randy_giffen@oti.com",
 "knut_radloff@oti.com",
 "daniel_megert@oti.com",
 "erich_gamma@oti.com",
 ] 


def overlapping_percentage(x, y):
    count=0;
    for index in range(0,len(A)-1):
        if(A[index]==B[index]):
            count+=1
    return (count*100)/len(A)
print(overlapping_percentage(A, B))
# 87.00