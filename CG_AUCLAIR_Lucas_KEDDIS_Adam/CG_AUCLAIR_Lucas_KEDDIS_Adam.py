# Projet
#########################################
# informations liées au groupe
# groupe LDDBI
# LUCAS AUCLAIR
# ADAM KEDDIS
#########################################

# import des librairies
import tkinter as tk
import PIL as pil
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import simpledialog

########################################
# le QR code qui est lu

nom = 'qr_code_ssfiltre_ascii_corrupted.png'

########################################
# variables globales

mat = 0 # matrice du QR code
inverse = False #
mat_droite = False # permet d'être sûr que le QR code est droit avant de vérifier les lignes
#liste_de_7_bits, liste contenant tous les blocs lus où chaque bloc est coupé en 2 pour avoir
# des codes 7 bits à décoder
# data, liste contenant tous les codes de 7 bits qui ont été décodés à l'aide d'Hamming (7,4)

########################################
# fonctions

def nbrCol(matrice):
    return(len(matrice[0]))

def nbrLig(matrice):
    return len(matrice)

def saving(matPix, filename):
    """Fonction qui sauvegarde l'image contenue dans matpix dans le fichier filename""" # fonction prise dans le TD 
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):
    """Fonction qui charge le fichier image filename et renvoie une  
    matrice de 0 et de 1 qui représente l'image en noir et blanc""" # fonction prise dans le TD
    global mat
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat

def modify(matrice):
    global imgModif # fonction prise dans le TD
    global nomImgCourante
    saving(matrice,"modif.png")
    imgModif=ImageTk.PhotoImage(file="modif.png")
    nomImgCourante="modif.png"

def check_angle():
    '''Fonction qui regarde les angles du QR Code'''
    global inverse, mat_droite
    if ( mat[24][18] and mat[24][19] and mat[24][20] and mat[24][21] and mat[24][22] and mat[24][23] and mat[24][24] ) == 0 :
        if ( mat[18][18] and mat[19][18] and mat[20][18] and mat[21][18] and mat[22][18] and mat[23][18] and mat[24][18] ) == 0 :
            if ( mat[18][18] and mat[18][19] and mat[18][20] and mat[18][21] and mat[18][22] and mat[18][23] and mat[18][24] ) == 0 :
                if ( mat[18][24] and mat[19][24] and mat[20][24] and mat[21][24] and mat[22][24] and mat[23][24] and mat[24][24] ) == 0 :
                    if ( mat[19][19] and mat[20][19] and mat[21][19] and mat[22][19] and mat[23][19] ) == 1 :
                        if ( mat[19][19] and mat[19][20] and mat[19][21] and mat[19][22] and mat[19][23] ) == 1 :
                            if ( mat[23][19] and mat[23][20] and mat[23][21] and mat[23][22] and mat[23][23] ) == 1 :
                                if ( mat[19][23] and mat[20][23] and mat[21][23] and mat[22][23] and mat[23][23] ) == 1 :
                                    inverse = True
                                    rotate_droite()
                                    pass
                                else:
                                    print('pas besoin de retourner')  
                                    inverse = False
                                    mat_droite = True
                            else:
                                print('pas besoin de retourner') 
                                inverse = False
                                mat_droite = True
                        else:
                            print('pas besoin de retourner') 
                            inverse = False
                            mat_droite = True
                    else:
                        print('pas besoin de retourner')
                        inverse = False
                        mat_droite = True
                else:
                    print('pas besoin de retourner')
                    inverse = False
                    mat_droite = True
            else:
                print('pas besoin de retourner')
                inverse = False
                mat_droite = True
        else:
            print('pas besoin de retourner')
            inverse = False
            mat_droite = True                        
    else:
        print('pas besoin de retourner')
        inverse = False
        mat_droite = True                

        
def rotate_droite():
    '''Rotation 90° vers la droite ''' # fonction prise du TD 
    global inverse, mat, mat_droite
    mat_res = [[(0,0,0,0)]*nbrLig(mat) for i in range(nbrCol(mat))]

    while inverse == True :
        for i in range(nbrLig(mat_res)):
            for j in range(nbrCol(mat_res)):
                mat_res[i][j] = mat[nbrLig(mat)-1-j][i]
        mat = mat_res
        mat_droite = True
        check_angle()

def check_lignes():
    """Vérifie que les lignes sont correctes si et seulement si le QR Code est dans le bon sens"""
    if mat_droite == True and(mat[8][6] == 1, mat[10][6] == 1,
    mat[12][6] == 1, mat[14][6] == 1, mat[16][6] == 1,
    mat[6][8] == 1, mat[6][10] == 1, mat[6][12] == 1,
    mat[6][14] == 1, mat[6][16] == 1):
        print("Les lignes apparaissent correctement et le QR Code est droit.")
    elif mat_droite == True and not (mat[8][6] == 1 and mat[10][6] == 1 and
    mat[12][6] == 1 and mat[14][6] == 1 and mat[16][6] == 1 and
    mat[6][8] == 1 and mat[6][10] == 1 and mat[6][12] == 1 and
    mat[6][14] == 1 and mat[6][16] == 1):
        print("Les lignes n'apparaissent pas correctement mais le QR Code est droit.")
    else:
        print("Il faudrait déjà savoir si le QR Code n'est pas à l'envers.")

def Hamming(bits):
    """Fonctionne qui décode une liste de 7 bits avec Hamming(7,4), cette fonction a été récupérée
    des td"""
    # calcul des valeurs des bits de contrôle
    p1 = bits[0] ^ bits[1] ^ bits[3]
    p2 = bits[0] ^ bits[2] ^ bits[3]
    p3 = bits[1] ^ bits[2] ^ bits[3]
    
    # position de l'erreur s'il y en a une (0 le cas échéant)
    num = int(p1 != bits[4])*4 + int(p2 != bits[5])*2 + int(p3 != bits[6])

    if (num == 3):
        bits[0] = int (not bits[0])
        #print("correction d'un pixel corrompu 1\n")
    if (num == 5):
        bits[1] = int (not bits[1])
        #print("correction d'un pixel corrompu 2\n")
    if (num == 6):
        bits[2] = int (not bits[2])
        #print("correction d'un pixel corrompu 3\n")
    if (num == 7):
        bits[3] = int (not bits[3])
        #print("correction d'un pixel corrompu 4\n")
    return bits[:4]

def lecture():
    #lire au plus 8 séries de blocs
    stock = []
    ss_stock = []
    size = 24 
    pair = True

    for i in range(7):
        size2 = size - i 
        size3 = size
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(7,14):
        size2 = size - i 
        size3 = size 
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True   
    stock.append(ss_stock)
    ss_stock = []
    for i in range(11,18):
        size3 = size - 2 # - 2 pour remonter de 2 cases 
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(18,25):
        size3 = size - 2 
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(7):
        size2 = size - i 
        size3 = size - 4 # - 4 pour remonter de 2 cases 
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(7,14):
        size2 = size - i 
        size3 = size - 4
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True   
    stock.append(ss_stock)
    ss_stock = []
    for i in range(11,18):
        size3 = size - 6 # - 6 pour remonter de 2 cases
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(18,25):
        size3 = size - 6
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []

    
    for i in range(7):
        size2 = size - i 
        size3 = size - 8 # - 4 pour remonter de 2 cases 
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(7,14):
        size2 = size - i 
        size3 = size - 8
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True   
    stock.append(ss_stock)
    ss_stock = []
    for i in range(11,18):
        size3 = size - 10 # - 6 pour remonter de 2 cases
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(18,25):
        size3 = size - 10
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(7):
        size2 = size - i 
        size3 = size - 12 # - 4 pour remonter de 2 cases 
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(7,14):
        size2 = size - i 
        size3 = size - 12
        if pair == True :
            ss_stock.append(mat[size3][size2])
            pair = False
        if pair == False :
            ss_stock.append(mat[size3-1][size2])
            pair = True   
    stock.append(ss_stock)
    ss_stock = []
    for i in range(11,18):
        size3 = size - 14 # - 6 pour remonter de 2 cases
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    for i in range(18,25):
        size3 = size - 14
        if pair == True :
            ss_stock.append(mat[size3][i])
            pair = False
        if pair == False : 
            ss_stock.append(mat[size3-1][i])
            pair = True
    stock.append(ss_stock)
    ss_stock = []
    print(stock)
    print(len(stock))
    return stock 
  

def conversionEntier(liste,b):
    """Fonction qui convertit une liste de bits codés dans une certaine base au nombre correspondant
    en décimal, fonction récupérée des td"""

    res = 0
    liste.reverse()
    for i in range (len(liste)):
      res += liste[i]*(b**i)
    return res

def couper_liste():
    """Fonction qui coupe les bloques à lire en 2 dans la liste qui contient tous les blocs
    de manière à avoir des listes de 7 bits"""

    global liste_de_7_bits

    liste_lec = (lecture()[0:bit_code()])
    liste_de_7_bits = []
    for liste in liste_lec:
        liste_de_7_bits.append(liste[0:7])
        liste_de_7_bits.append(liste[7:])

def appliquer_Hamming():
    """Fonction qui applique Hamming(7,4) aux listes de 7 bits que l'on a obtenu après avoir
    lu les blocs à lire"""

    global liste_de_7_bits
    global data

    data = []
    for i in liste_de_7_bits:
        data.append(Hamming(i))
    print("liste des demi-blocs décodés avec Hamming = ", data)


def interpretation():
    """Fonction qui regarde la valeur du bit en position (24,8) et applique le décodage
    en fonction de l'énoncé, si = 0 alors il faut les décoder en hexadécimal sinon il faut
    les décoder avec ASCII"""
    global data
    liste_finale = []

    if mat[24][8] == 0:
        print("pixel en mat[24][8] = 0")
        liste_de_transition = []
        c = 0
        while c < nbrLig(data):
            liste_de_transition.append(data[c] + data[c + 1])
            c += 2
        for i in liste_de_transition:
            liste_finale.append(hex(conversionEntier(i, 2)))
        print(liste_finale)

    else:
        liste_de_transition = []
        print("pixel en mat[24][8] = 1")
        c = 0
        while c < nbrLig(data):
            liste_de_transition.append(data[c] + data[c + 1])
            c += 2
        for i in liste_de_transition:
            liste_finale.append(chr(conversionEntier(i, 2)))
        print(liste_finale)

    


def filtre():
    '''Fonction qui permet de mettre un filtre'''
    fil = []
    ss_fill = []
    pair = True
    if mat[22][8] == 0 and mat[23][8] == 0 : 
        print("Aucun filtre")  
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                ss_fill.append(0)
            fil.append(ss_fill)
            ss_fill = []
                      
    elif mat[22][8] == 0 and mat[23][8] == 1 : 
        print("un damier dont la case en haut a gauche est noire")
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if pair == True : 
                    ss_fill.append(0)
                elif pair == False :
                    ss_fill.append(1)
                pair = not pair
            fil.append(ss_fill)
            ss_fill = []
        
    elif mat[22][8] == 1 and mat[23][8] == 0 : 
        print(" des lignes horizontales altern´ees noires et blanches, la plus haute ´etant noire ")
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if pair == True : 
                    ss_fill.append(0)
                elif pair == False :
                    ss_fill.append(1)
            fil.append(ss_fill)
            pair = not pair
    elif mat[22][8] == 1 and mat[23][8] == 1 : 
        print("des lignes verticales altern´ees noires et blanches, la plus `a gauche ´etant noire")
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if pair == True : 
                    ss_fill.append(0)
                elif pair == False :
                    ss_fill.append(1)
                pair = not pair
            pair = not pair 
            fil.append(ss_fill)
            ss_fill = []
    for i in range(len(fil)):
        for j in range(len(fil[i])):
            mat[i][j] = mat[i][j] ^ fil[i][j]


def bit_code():
    stockage = []
    a = 0 
    for i in range(13,18):
        stockage.append(mat[i][0])
    z = len(stockage) - 1
    for j in range(0,len(stockage)): 
        a += stockage[j]*(2**z)
        z -= 1 
    print(a, "est le nombre de blocs à decoder")
    return a

#############################################
# appel des fonctions

loading(nom)
check_angle()
check_lignes()
filtre()
#bit_code() appelée dans la fonction d'après
#lecture() appelée dans la fonction d'après
couper_liste()
appliquer_Hamming()
interpretation()