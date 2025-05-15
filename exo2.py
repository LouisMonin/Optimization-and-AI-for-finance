import pandas as pn
import numpy as np 
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


#reading the data
myData = pn.read_csv("/Users/sabine/Desktop/CYTech/S3/Optim_IA/Examen/housing.csv")
nbColumns = myData.shape[1]
nbVars = nbColumns


# Question 1 -------------------------------------------------------

# Tracer un histogramme pour la dernière colonne MEDV
plt.figure(figsize=(8, 6))
plt.hist(myData[' MEDV'], bins=20, color='skyblue', edgecolor='black')
plt.title("Histogramme des prix médians")
plt.xlabel("Prix médians")
plt.ylabel("Fréquence")
plt.show()

# Question 2 -------------------------------------------------------

# Cette fonction prend en entrée les prix dans la colonne MEDV et les transforme en 3 catégories : Low, Intermediate, High

def num2categ(tab, b1, b2):
   tab_ret = [] 
   for i in range(tab.size):
     if (tab[i]<=b1):
       tab_ret.append("Bas")
     elif (tab[i]>=b2):
       tab_ret.append("Haut")
     else:
       tab_ret.append("Moyen")
   return tab_ret


# On extrait les prix du dataset
# On prend comme bornes b1 et b2 les quantiles 0.33 et 0.66 afin de créé 3 classes de tailles environ égales 
price = np.array(myData[' MEDV'])
b1 = np.quantile(price, 0.33)
b2 = np.quantile(price, 0.66)

# On applique la fonction num2categ pour obtenir les classes
tab_cls = num2categ(price, b1, b2)
lst_cls = list(tab_cls)
myData['Class'] = lst_cls

print("Nous avons ", lst_cls.count('Haut')," Haut")
print("Nous avons ", lst_cls.count('Bas')," Bas")
print("Nous avons ", lst_cls.count('Moyen')," Moyen")


# Question 3 -------------------------------------------------------

# On crée la fonction permettant d'encoder les classes

def encodeClass(s_class):
  if (s_class=='Bas'):
    return [1,0,0]
  elif (s_class=='Haut'):
    return [0,0,1]
  else:
    return [0,1,0]
  

# On encode les classes
X=myData.values[:,:nbVars]
X=X.astype('float64')
Y=myData.values[:,nbColumns]
encoded_Y = np.array([encodeClass(y) for y in list(Y)])


# On divise les données en données d'entrainement et de test

X_train, X_test, Y_train, Y_test = train_test_split( X, encoded_Y, test_size = 0.3, random_state = 100)


# Création du réseau de neurones

nn = Sequential()
nn.add(Dense(5, input_dim=nbVars, activation='sigmoid'))
nn.add(Dense(3, activation='relu'))
# On finit par une couche de 3 neurones pour les 3 classes, la fonction softmax permet la multi-classification
nn.add(Dense(3, activation='softmax'))



nn.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

nn.fit(X_train, Y_train, epochs=500, batch_size=5)

# On entraine le réseau de neurones
score = nn.evaluate(X_test, Y_test, verbose=2)

# Question 4 -------------------------------------------------------

# On affiche la précision du modèle
print('Test accuracy:', score[1])

# On affiche la matrice de confusion
Y_pred = nn.predict(X_test)
Y_pred_1 = Y_pred.argmax(axis=1)
Y_test_1 = Y_test.argmax(axis=1)
confusion = confusion_matrix(Y_pred_1, Y_test_1)
print(confusion)


# Question 5 -------------------------------------------------------

# Partie a 

for numc in range(nbColumns-1):
    C = myData.values[:,numc]
    print("Column ",numc,": ","Min = ",round(min(C),2),"   Max = ",round(max(C),2),"   Mean = ",round(np.mean(C),2),"   Sd = ",round(np.std(C),2))
    
# Les moyennes, écarts-types, minimums et maximums des colonnes sont très différents, il est donc nécessaire de normaliser les données


# Partie b

scaler2 = StandardScaler()
scaler2.fit(X)
X_scaled2 = scaler2.transform(X)
X = X_scaled2

encoded_Y = np.array([encodeClass(y) for y in list(Y)])

X_train, X_test, Y_train, Y_test = train_test_split( X, encoded_Y, test_size = 0.3, random_state = 100)

# Création du réseau de neurones

nn = Sequential()
nn.add(Dense(5, input_dim=nbVars, activation='sigmoid'))
nn.add(Dense(3, activation='softmax'))

nn.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

nn.fit(X_train, Y_train, epochs=500, batch_size=5)

# On entraine le réseau de neurones
score = nn.evaluate(X_test, Y_test, verbose=2)

# On affiche la précision du modèle
print('Test accuracy:', score[1])

# On affiche la matrice de confusion
Y_pred = nn.predict(X_test)
Y_pred_1 = Y_pred.argmax(axis=1)
Y_test_1 = Y_test.argmax(axis=1)
confusion = confusion_matrix(Y_pred_1, Y_test_1)
print(confusion)

# La normalisation des données a permis d'améliorer la précision du modèle

# On affiche de nouveau les données normalisées
for numc in range(nbColumns-1):
    C = X[:,numc]
    print("Column ",numc,": ","Min = ",round(min(C),2),"   Max = ",round(max(C),2),"   Mean = ",round(np.mean(C),2),"   Sd = ",round(np.std(C),2))