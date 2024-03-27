from PIL import Image
import os

#Fonction qui encode les couleurs dans 2 char
def encodeColor(red, green, blue):
    letter1 = 0b00000000
    letter2 = 0b00000000
    letter1 |= int(red/255*15) << 2
    letter1 |= (int(green/255*15) & 0b1111) >> 2
    letter2 |= (int(green/255*15) & 0b0011) << 4
    letter2 |= int(blue/255*15)
    letter1 += 33
    letter2 += 33
    return chr(letter1) + chr(letter2)

#Resolution de l'image
largeur, hauteur = (160, 111)

#Recupere le nom du fichier à encoder
imageName = input("Le nom de l'image à encoder > ")

#Chargement et mise à l'echelle de l'image
image = Image.open(imageName)
image = image.resize((largeur, hauteur))

#Tableau de l'image
imageChar = [""] * 111

#Parcours de chaque pixel de l'image
for y in range(hauteur):
    for x in range(largeur):
        pixel = image.getpixel((x,y))
        imageChar[y] += encodeColor(pixel[0], pixel[1], pixel[2])

#Creation du fichier de l'image dans un .py pour le lire sur une calculatrice
filenamepy = f"{os.path.splitext(imageName)[0]}.py"
with open(filenamepy, "w") as file:
    file.write("""from kandinsky import *
def decodeColor(letter1, letter2):
    letter1 = ord(letter1) - 33
    letter2 = ord(letter2) - 33
    return color((letter1 >> 2 & 0b1111)/15*255 , (((letter1 & 0b11) << 2) | (letter2 >> 4 & 0b11))/15*255 , (letter2 & 0b1111)/15*255)

def printLine(line, i):
    for letter in range(0, len(line), 2):
        fill_rect(letter, 2*i, 2, 2, decodeColor(line[letter], line[letter + 1]))
"""
    ) 

    for i in range(0, 111):
        file.write("printLine(\"")
        for j in imageChar[i]:
            if(j == '"'):
                file.write("\\\"")
            elif(j == '\\'):
                file.write("\\\\")
            else:
                file.write(f"{j}")
        file.write(f"\",{i})\n")
