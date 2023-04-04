# Libraries
from pathlib import Path
from scipy import signal
import numpy as np
import matplotlib.pylab as plt
from os.path import exists
import scipy.io # Read .mat files
import os
import copy
import pickle
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import time


taille_carre = 6
nb_valeurs_par_touche = 10

pathname = ""        # To change w.r.t. the disk writer specs
basename = "Mesures_clavier" # To change w.r.t. the given name

chemin_stylo = 'Documents/Projet_Clavier/python/data_seance6_stylo_cor_01.pickle'
chemin_doigts = 'Documents/Projet_Clavier/python/data_seance5_doigts_lin_01.pickle'
chemin_stylo_cor = 'Documents/Projet_Clavier/python/data_seance6_stylo_cor_01.pickle'
chemin_doigts_cor = 'Documents/Projet_Clavier/python/data_seance6_doigts_cor_01.pickle'

with open(chemin_doigts, 'rb') as fp: # lecture du fichier
    _data_stylo_ = pickle.load(fp)


a=0
b=1
tab = np.zeros((6,6))
print("Début")

try:
    while True:
        try:
            start = time.time()
            listing = os.listdir(pathname)
            paths = []
            for filename in listing:
                print("add file")
          # Add .mat files
                if filename.startswith(basename) and filename.endswith(".mat"):
                    paths.append([int(os.stat(pathname + filename).st_mtime), pathname + filename])
                try :
                    if len(paths) != 0:
                        if a>=taille_carre:
                            a=1
                            b+=1
                        else :
                            a+=1
                        print("la valeur de a vaut ",a," et la valeur de b vaut ",b)
                        paths = np.sort(paths, axis = 0)
                        # Process the files by ascending date number
                        print(paths[0, 1])
                        # Cat the data field in the X matrix
                        time.sleep(0.1) # In seconds
                        reader = scipy.io.loadmat(paths[0, 1])
                        Fs = reader['tpd']['SampleFrequency'][0,0].item() # Hz
                        unit = reader['tpd']['Unit'][0,0].item() #  ('V' or ...)
                        tpd = reader['tpd']['Data'][0,0].ravel() # p length vector
                        s_norm = tpd/(np.linalg.norm(tpd))
                        os.remove(paths[0, 1])
                        #########################" Corrélation #####################"
                        print("faisons la correlation")
                        for i in range(1,taille_carre+1):
                            print("ittération du les lgnes k",i)
                            for k in range(1,taille_carre+1):
                                print("ittérations sur les colonnes i",k)
                                S=0
                                print("la longueur de data_stylo vaut ", len(_data_stylo_[(i,k)]))
                                for j in range(nb_valeurs_par_touche):
                                    print("ittération sur le nombre de signaux de la base par position j",j)
                                    corr = signal.correlate(s_norm, _data_stylo_[(i,k)][j], mode='same')
                                    print("?")
                                    S = S + np.max(corr)
                                Somme = S/nb_valeurs_par_touche
                                tab[k-1,i-1] = Somme
                                tab_transpose = np.transpose(tab)
                        #print(_correlate_)
                        print(tab_transpose)
                        print("--------- suivant ------------")
                        print("appuyer en position: ",(a+1,b))
                        #--------------------- Temps calcul -------------------------
                        end = time.time()
                        temps = end - start
                        print("le temps de calcul pour un signal vaut : ",temps)
#------------------------------------------------
                        ################ Trace correlation ####################
                        fig = plt.figure(figsize=(8,6))
                        '''
                        fig, ax = plt.subplots()
                        for i in range(1,taille_carre+1):
                            for j in range(1,taille_carre+1):
                                c = tab_transpose[i][j]
                                ax.text(i, j, str(c), va='center', ha='center')
                        '''
                        plt.pcolormesh(tab_transpose,cmap="plasma")
                        plt.title("Plot 2D array")
                        plt.colorbar()
                        plt.show()
                        
                except Exception as inst:
                    print(type(inst))    # the exception instance
                    print(inst.args)     # arguments stored in .args
                    print(inst)
                    print("erreur, on recommence")
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)
            print("erreur, on recommence")

except KeyboardInterrupt:
  print("Reader stopped")


'''
for i in range(1,taille_carre+1):
    for j in range(1,taille_carre+1):
        c = intersection_matrix[i][j]
        ax.text(i+0.5, j+0.5, str(c), va='center', ha='center')

tab = np.zeros((6,6))
for k in range(1,taille_carre+1):
    print("ittération du les lgnes k",k)
    for i in range(1,taille_carre+1):
        print("ittérations sur les colonnes i",i)
        S=0
        print("la longueur de data_stylo vaut ", len(_data_stylo_[(i,k)]))
        for j in range(nb_valeurs_par_touche):
            print("ittération sur le nombre de signaux de la base par position j",j)
            corr = signal.correlate(s_norm, _data_stylo_[(i,k)][j], mode='same')
            print("?")
            S = S + np.max(corr)
        Somme = S/nb_valeurs_par_touche
        tab[i-1,k-1] = Somme
#print(_correlate_)
print(tab)

fig = plt.figure(figsize=(8,6))
plt.pcolormesh(tab,cmap="plasma")
plt.title("Plot 2D array")
plt.colorbar()
plt.show()
'''