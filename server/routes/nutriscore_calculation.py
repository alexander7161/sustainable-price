def points_A_not_beverages(nutrients):
    a = b = c = d = 0

    if(nutrients['energy'] <= 335):
        a = 0
    elif(nutrients['energy'] <= 670):
        a = 1
    elif(nutrients['energy'] <= 1005):
        a = 2
    elif(nutrients['energy'] <= 1340):
        a = 3
    elif(nutrients['energy'] <= 1675):
        a = 4
    elif(nutrients['energy'] <= 2010):
        a = 5
    elif(nutrients['energy'] <= 2345):
        a = 6
    elif(nutrients['energy'] <= 2680):
        a = 7
    elif(nutrients['energy'] <= 3015):
        a = 8
    elif(nutrients['energy'] <= 3350):
        a = 9
    else:
        a = 10

    if(nutrients['sugars'] <= 4.5):
        b = 0
    elif(nutrients['sugars'] <= 9):
        b = 1
    elif(nutrients['sugars'] <= 13.5):
        b = 2
    elif(nutrients['sugars'] <= 18):
        b = 3
    elif(nutrients['sugars'] <= 22.5):
        b = 4
    elif(nutrients['sugars'] <= 27):
        b = 5
    elif(nutrients['sugars'] <= 31):
        b = 6
    elif(nutrients['sugars'] <= 36):
        b = 7
    elif(nutrients['sugars'] <= 40):
        b = 8
    elif(nutrients['sugars'] <= 45):
        b = 9
    else:
        b = 10

    if(nutrients['saturated_fat'] <= 1):
        c = 0
    elif(nutrients['saturated_fat'] <= 2):
        c = 1
    elif(nutrients['saturated_fat'] <= 3):
        c = 2
    elif(nutrients['saturated_fat'] <= 4):
        c = 3
    elif(nutrients['saturated_fat'] <= 5):
        c = 4
    elif(nutrients['saturated_fat'] <= 6):
        c = 5
    elif(nutrients['saturated_fat'] <= 7):
        c = 6
    elif(nutrients['saturated_fat'] <= 8):
        c = 7
    elif(nutrients['saturated_fat'] <= 9):
        c = 8
    elif(nutrients['saturated_fat'] <= 10):
        c = 9
    else:
        c = 10

    if(nutrients['sodium'] <= 90):
        d = 0
    elif(nutrients['sodium'] <= 180):
        d = 1
    elif(nutrients['sodium'] <= 270):
        d = 2
    elif(nutrients['sodium'] <= 360):
        d = 3
    elif(nutrients['sodium'] <= 450):
        d = 4
    elif(nutrients['sodium'] <= 540):
        d = 5
    elif(nutrients['sodium'] <= 630):
        d = 6
    elif(nutrients['sodium'] <= 720):
        d = 7
    elif(nutrients['sodium'] <= 810):
        d = 8
    elif(nutrients['sodium'] <= 800):
        d = 9
    else:
        d = 10

    return a, b, c, d


def simplified_nutriscore(nutrients):
    a = b = c = d = 0
    try:
        a, b, c, d = points_A_not_beverages(nutrients)
        score = a + b + c + d
    except:
        score = -100

    nutriscore = 'E'

    if(score > -99 and score < -1):
        nutriscore = "A"
    elif(score >= 0 and score <=2):
        nutriscore = "B"
    elif(score >= 3 and score <= 10):
        nutriscore = "C"
    elif(score >= 11 and score <= 18):
        nutriscore = "D"
    #     elif(score > 18):
    #         nutriscore = "E"

    return nutriscore