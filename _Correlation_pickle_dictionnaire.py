# Libraries
from pathlib import Path
import os
import time
import scipy.io # Read .mat files
from scipy import signal
import numpy as np
import matplotlib.pylab as plt
from os.path import exists
import random
import pickle



# Global variables
pathname = ""        # To change w.r.t. the disk writer specs
basename = "Mesures_clavier" # To change w.r.t. the given name
fichier = open(pathname,'r')
X = []    # At this point n and p are unknown
Nb_sample = 1000
fe = 200000
temps = np.linspace(0,Nb_sample/fe,Nb_sample)
Reponse_clavier = []
Pas_detection = 5 # le coté du carré d'une zone de détection en mm
N_elements = 5 # le nombre de carré par ligne
chemin = 'C:/Users/torre/Documents/Projet_Clavier/python/data.pickle'

# Création de la base de données de références sous forme de dictionnaire
dict = dict()

key_list = []
value_list = []
for k in range(1,16):
  for i in range(1,18):
    key_list.append((i,k))
    value_list.append(random.sample(range(6), 5))

#print(key_list)
#print(value_list)
############################### Implémentationdes coordonnées dans la base de donnés ##################
if exists(chemin):
  os.remove(chemin) #supprime le dictionnaire s'il existe déja

dict_from_list = {key_list[i]: value_list[i] for i in range(len(key_list))}
#print(dict_from_list)


#################################################

#################################
try :
# Infinite loop to read and process the data to be acquired
  while True:
    try :
      # List all files
      listing = os.listdir(pathname)
      paths = []
      for filename in listing:
          # Add .mat files
        if filename.startswith(basename) and filename.endswith(".mat"):
            paths.append([int(os.stat(pathname + filename).st_mtime), pathname + filename])
      # if one file is find
      #print(paths)
      for k in range(1,16):
        for i in range(1,18):
            if len(paths) != 0:
            # Sort files by modification time
                paths = np.sort(paths, axis = 0)

          # Process the files by ascending date numbers
          
                for h in range(paths.shape[0]):
                    print(paths[h, 1])
                    # Cat the data field in the X matrix
                    time.sleep(0.01) # In seconds
                    reader = scipy.io.loadmat(paths[h, 1])
                    Fs = reader['tpd']['SampleFrequency'][0,0].item() # Hz
                    unit = reader['tpd']['Unit'][0,0].item() #  ('V' or ...)
                    tpd = reader['tpd']['Data'][0,0].ravel() # p length vector
                    #X.append(tpd)
                    dict_from_list[(i,k)] = tpd
                    print("la valeur du ",h,"signal est mise en position ",(i,k))
                    print(dict_from_list)
                    plt.figure()
                    plt.show
                    os.remove(paths[h, 1])
            # Concatenate to X
            #########################" Corrélation #####################"
            '''
            fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
        
            clock = np.arange(64, len(Base_Signal), 128)
            ax_orig.plot(Base_Signal) # plot signal
            #ax_orig.plot(clock, Base_Signal[clock], 'ro') # plot points rouge
            ax_orig.set_title('Original signal')
            ax_noise.plot(X[k]) # plot bruit
            ax_noise.set_title('Signal with noise')
            A_max_signal = np.max(X[k])
            corr = signal.correlate(X[k], Base_Signal, mode='same')*(A_max_base/A_max_signal)
            print("coucou")
            ax_corr.plot(corr)
            print(np.max(corr))
            ax_corr.plot(clock, corr[clock], 'ro')
            ax_corr.axhline(0.5, ls=':')
            ax_corr.set_title('Cross-correlated')
            fig.tight_layout()
            plt.show()
            '''
            #############################################################
    except Exception as inst:
      print(type(inst))    # the exception instance
      print(inst.args)     # arguments stored in .args
      print(inst)
      print("erreur, on recommence")
except KeyboardInterrupt:
  print("Reader stopped")


with open(chemin, 'wb') as fp: # création du fichier
    pickle.dump(dict_from_list, fp)

with open(chemin, 'rb') as fp: # lecture du fichier
    _data_ = pickle.load(fp)
print(_data_)
#print('cccc')
#print(_data_[(2,1)])