# Libraries
from pathlib import Path
import os
import time
import scipy.io # Read .mat files
from scipy import signal
import numpy as np
import matplotlib.pylab as plt
from os.path import exists
import copy
import pickle

chemin = 'Documents/Projet_Clavier/python/data_seance9_stylo_01.pickle'
chemin_lin = 'Documents/Projet_Clavier/python/data_seance9_stylo_lin_01.pickle'
key_list = []
value_list = []
taille_carre = 6
nb_valeurs_par_touche = 10

for k in range(1,taille_carre + 1):
  for i in range(1,taille_carre + 1):
    key_list.append((i,k))
print("la longeur de la liste de clé vaut ",len(key_list))

##### Ecrase fichier lin si existe ##########

if exists(chemin_lin):
  os.remove(chemin_lin) #supprime le dictionnaire s'il existe déja

  ##########################################

with open(chemin, 'rb') as fp: # lecture du fichier
    _data_ = pickle.load(fp)
#print(_data_[(1,1)])
_data_lin_ = copy.deepcopy(_data_)
#print(_data_lin_[(1,1)]) # création du dionnaire à normaliser
print("la longeur du dictionnaire de donnes vaut ",len(_data_lin_))
######## Normalisation ##########""

for i in range(len(key_list)):
  #print("ittération de key_list ",i)
  for k in range(nb_valeurs_par_touche):
    #print("ittération numéo signal par touche ",k)
    v = _data_[key_list[i]][k]
    _data_lin_[key_list[i]][k] = v/(np.linalg.norm(v))

print(_data_[(1,1)][0])
print(_data_lin_[(1,1)][0])
#np.array_equal(_data_lin_[key_list[i]],normalized)


########## création du fichier normalisé ############

with open(chemin_lin, 'wb') as fp: # création du fichier
    pickle.dump(_data_lin_, fp)

#print(_data_[(1,1)])
#print(_data_lin_[(1,1)])

