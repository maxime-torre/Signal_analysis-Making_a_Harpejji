# Libraries
from pathlib import Path
from scipy import signal
import numpy as np
import matplotlib.pylab as plt
from os.path import exists
import scipy.io # Read .mat files
import os
import time
import pickle
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import time
from sklearn.neighbors import KNeighborsClassifier
import winsound 

# frequency
lad3 =  466.164
Si3 = 493.883
do3 = 523.251
dod3 = 	554.365
Re3 = 	587.33
Red3 = 	622.254
Mi3 = 	659.255
Fa3 = 	698.456
Fad3 = 	739.989
Sol3 = 	783.991
Sold3 = 830.609
La3 = 	880
Lad4 = 932.328
Si4 = 	987.767
Do4 = 	1046.5
Dod4 = 1108.73

tab_son = np.array([[Red3,Re3,dod3,do3,Si3,lad3],[Fa3,Mi3,Red3,Re3,dod3,do3],
[Sol3,Fad3,Fa3,Mi3,Red3,Re3],[La3,Sold3,Sol3,Fad3,Fa3,Mi3],
[Si4,Lad4,La3,Sold3,Sol3,Fad3],[Dod4,Do4,Si4,Lad4,La3,Sold3]])

# duration is set to 800 milliseconds             
dur = 800 # ms


taille_carre = 6
nb_valeurs_par_touche = 10

pathname = "Documents/Projet_Clavier/Mesures/"        # To change w.r.t. the disk writer specs
basename = "Mesures_clavier" # To change w.r.t. the given name

chemin_stylo = 'Documents/Projet_Clavier/python/data_seance9_stylo_lin_01.pickle'
chemin_doigts = 'Documents/Projet_Clavier/python/data_seance5_doigts_lin_01.pickle'
chemin_stylo_cor = 'Documents/Projet_Clavier/python/data_seance6_stylo_cor_01.pickle'
chemin_doigts_cor = 'Documents/Projet_Clavier/python/data_seance6_doigts_cor_01.pickle'

tuple_xy = []
for i in range(1,taille_carre+1):
    for k in range(1,taille_carre+1):
        tuple_xy.append([k,i])

print(tuple_xy)

with open(chemin_stylo, 'rb') as fp: # lecture du fichier
    _data_stylo_ = pickle.load(fp)

key_list = []
for i in range(1,36+1):
      for j in range(nb_valeurs_par_touche):
        key_list.append(i)

tab_value = []


for cle, valeur in _data_stylo_.items():
    for i in range(nb_valeurs_par_touche):
        tab_value.append(valeur[i])

_data_array_ = np.array(tab_value)
key_list = np.array(key_list).reshape(-1,)

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
                        s_norm_new = np.array(s_norm).reshape(1, -1)
                        os.remove(paths[0, 1])
                        #########################" Corrélation knn #####################"
                        knn = KNeighborsClassifier(n_neighbors = 10) # Creation of the classifier
                        knn.fit(_data_array_, key_list) # Model fitting
                        y_predict = knn.predict(s_norm_new) # Prediction
                        coordonne = tuple_xy[int(y_predict)-1]
                        print("la valeur de coordonnée vaut : ",(coordonne[1],coordonne[0]))
                        print_value = np.zeros((6,6))
                        print_value[coordonne[0]-1,coordonne[1]-1] = 1
                        #------------------- Son --------------------------
                        winsound.Beep(int(tab_son[coordonne[1]-1,coordonne[0]-1]), dur)
                        print("la fréquence vaut :",tab_son[coordonne[1]-1,coordonne[0]-1] )
                        print("y_predict vaut ",y_predict)
                        print("--------- suivant ------------")
                        print("appuyer en position: ",(a+1,b))
                        #--------------------- Temps calcul -------------------------
                        end = time.time()
                        temps = end - start
                        print("le temps de calcul pour un signal vaut : ",temps)
#------------------------------------------------
                        ################ Trace correlation ####################
                        '''
                        fig = plt.figure(figsize=(8,6))
                        plt.pcolormesh(print_value,cmap="plasma")
                        plt.title("Plot 2D array")
                        plt.colorbar()
                        plt.show()
                        '''
                        

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



