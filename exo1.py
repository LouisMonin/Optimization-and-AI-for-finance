# Question 1 -------------------------------------------------------
 
# Nous disposons de 20 000 euros à investir.
 
# 1) Bénéfice attendu pour chaque action :
 
# Cas 1 : le prix ne change pas : 20€ - 20€ = 0 de bénéfice.
# Cas 2 : le prix monte à 40€ : 40€ - 20€ = 20€ de bénéfices.
# Cas 3 : le prix baisse à 12€ : 12€ - 20€ = -8€ de bénéfice, c'est une perte.
 
# Calcul de l'espérance pour les actions :
# Esperance[Actions] = (1/3) * (0 + 20 - 8) = 4
 
# Bénéfice attendu pour chaque bon :
 
# Cas des bons : 90 + 100 = 10€ de bénéfices
# Esperance[Bond] = 10



# Question 2 ------------------------------------------------------- 

# 2) Bénéfice pour chaque option :
 
# On achète une option à 1000€ pour 100 actions à 15€ assurés dans 6 mois.
 
# Cas 1 : le prix de l'action est de 20€ :
# (20€ - 15€) * 100 = 500€
# --> 500€ - 1000€ = -500€ de bénéfices (ce sont des pertes).
 
# Cas 2 : le prix de l'action est de 40€ :
# (40€ - 15€) * 100 = 2500€
# --> 2500€ - 1000€ = 1500€ de bénéfices
 
# Cas 3 : le prix de l'action est de 12€ :
# (12€ - 15€) * 100 = -500€
# --> Le prix de l'action a baissé, on décide de ne pas en acheter. Résultat de l'opération : -1000€
 
# Calcul de l'espérance pour les options :
# Esperance[Option] = (1/3) * (-500 + 1500 - 1000) = 0


# Question 3 -------------------------------------------------------
 
#Pour modéliser le problème nous définissons 3 variables :
 
# xa pour les actions
# xo pour les obligations
# xb pour les bonds
 
# Notre objectif est de maximiser les bénéfices de notre gestion de portefeuille.
# Pour cela, nous avons une contrainte : nous ne pouvons pas invetsir plus de 20 000€ et nous ne pouvons pas acheter ou vendre plus de 50 actions.


# Question 4 -------------------------------------------------------

from pulp import *

# Définition des variables
problem = LpProblem("problem", LpMaximize)
xa = LpVariable("xa", lowBound=0, cat="Continuous")
xo = LpVariable("xo", lowBound=-50, upBound=50, cat="Integer") # on ne peut pas vendre ou acheter plus de 50 options
xb = LpVariable("xb", lowBound=0, cat="Continuous")


# Définition de la fonction objectif
# On a montré que le bénéfice de l'action serait de 4 (calcul de l'espérance), que le bénéfice de l'option serait de 0 et le bénéfice du bond est de (100-90)
# On pose : xa = action, xo = obligation et xb = bonds
 
# --> Alors, fonction objectif = 4*xa + 0*xo + 10*xb

problem += 4*xa + xb*10


# Définition des contraintes
# le prix maximum a dépenser est de 20000 à répartir entre action, option et bond.
#La contrainte est donc :
problem += xa *20 + xo*1000 + xb*90 <= 20000


# Résolution du problème
sol = problem.solve()

# Affichage des résultats
print ("---------- Résultat de la question 4 : ----------")
print(value(xa), value(xb), value(xo), value(problem.objective))




# Question 5 -------------------------------------------------------

# Situation 1 : p(20) = 0.25, p(40) = 0.6 et p(12) = 0.15
 
# 1) Bénéfice attendu pour chaque action :
 
# Cas 1 : le prix ne change pas : 20€ - 20€ = 0 de bénéfice avec une probabilité de 0.25
# Cas 2 : le prix monte à 40€ : 40€ - 20€ = 20€ de bénéfices avec une probabilité de 0.6
# Cas 3 : le prix baisse à 12€ : 12€ - 20€ = -8€ de bénéfice, c'est une perte avec une probabilité de 0.15
 

# Calcul de l'espérance pour les actions :
 
# Esperance[Actions] = 0 * 0.25 + 20 * 0.6 - 8 * 0.15 = 10.8
 

#Bénéfice pour chaque option :
 
# On achète une option à 1000€ pour 100 actions à 15€ assurés dans 6 mois.
 
# Cas 1 : le prix de l'action est de 20€ avec une probabilité de 0.25:
# (20€ - 15€) * 100 = 500€
# --> 500€ - 1000€ = -500€ de bénéfices (ce sont des pertes).
 
# Cas 2 : le prix de l'action est de 40€ avec une probabilité de 0.6:
# (40€ - 15€) * 100 = 2500€
# --> 2500€ - 1000€ = 1500€ de bénéfices
 
# Cas 3 : le prix de l'action est de 12€ avec une probabilité de 0.15:
# (12€ - 15€) * 100 = -500€
# --> Le prix de l'action a baissé, on décide de ne pas en acheter. Résultat de l'opération : -1000€
 
 
# Calcul de l'espérance pour les options :
 
# Esperance[Option] = -500 * 0.25 + 1500 * 0.6 -1000 *0.15 = 625
 

# Situation 2 : p(20) = 0.4, p(40) = 0.2 et p(12) = 0.4
 
#Bénéfice attendu pour chaque action :
 
# Cas 1 : le prix ne change pas : 20€ - 20€ = 0 de bénéfice avec une probabilité de 0.4
# Cas 2 : le prix monte à 40€ : 40€ - 20€ = 20€ de bénéfices avec une probabilité de 0.2
# Cas 3 : le prix baisse à 12€ : 12€ - 20€ = -8€ de bénéfice, c'est une perte avec une probabilité de 0.4
 
# Calcul de l'espérance pour les actions :
 
# Esperance[Actions] = 0 * 0.4 + 20 * 0.2 - 8 * 0.4 = 0.8
 
#Bénéfice pour chaque option :
 
# On achète une option à 1000€ pour 100 actions à 15€ assurés dans 6 mois.
 
# Cas 1 : le prix de l'action est de 20€ avec une probabilité de 0.4:
# (20€ - 15€) * 100 = 500€
# --> 500€ - 1000€ = -500€ de bénéfices (ce sont des pertes).
 
# Cas 2 : le prix de l'action est de 40€ avec une probabilité de 0.2:
# (40€ - 15€) * 100 = 2500€
# --> 2500€ - 1000€ = 1500€ de bénéfices
 
# Cas 3 : le prix de l'action est de 12€ avec une probabilité de 0.4:
# (12€ - 15€) * 100 = -500€
# --> Le prix de l'action a baissé, on décide de ne pas en acheter. Résultat de l'opération : -1000€
 
# Calcul de l'espérance pour les options :
 
# Esperance[Option] = -500 * 0.4 + 1500 * 0.2 -1000 *0.4 = -300
 


# Question 6 -------------------------------------------------------

# Situation 1 :

# Définition des variables
problem = LpProblem("problem", LpMaximize)
xa = LpVariable("xa", lowBound=0, cat="Continuous")
xo = LpVariable("xo", lowBound=-50, upBound=50, cat="Integer") # on ne peut pas vendre ou acheter plus de 50 options
xb = LpVariable("xb", lowBound=0, cat="Continuous")


# Définition de la fonction objectif

# On a montré que le bénéfice de l'action serait de 4 (calcul de l'espérance), que le bénéfice de l'option serait de 0 et le bénéfice du bond est de (100-90)
# On a donc 4*xa + 0*xo + 10*xb

problem += 10.8*xa + xb*10 + xo * 625

# Définition des contraintes
# le prix maximum a dépenser est de 20000 à répartir entre action, oprion et bond
problem += xa *20 + xo*1000 + xb*90 <= 20000


# Résolution du problème
sol = problem.solve()

# Affichage des résultats
print ("---------- Résultat de la question 6.1 : ----------")
print(value(xa), value(xb), value(xo), value(problem.objective))




# Sitution 2 :

# Définition des variables
problem = LpProblem("problem", LpMaximize)
xa = LpVariable("xa", lowBound=0, cat="Integer")
xo = LpVariable("xo", lowBound=-50, upBound=50, cat="Integer") # on ne peut pas vendre ou acheter plus de 50 options
xb = LpVariable("xb", lowBound=0, cat="Integer")


# Définition de la fonction objectif

# On a montré que le bénéfice de l'action serait de 4 (calcul de l'espérance), que le bénéfice de l'option serait de 0 et le bénéfice du bond est de (100-90)
# On a donc 4*xa + 0*xo + 10*xb

problem += 0.8*xa + xb*10 + xo * (-300)

# Définition des contraintes
# le prix maximum a dépenser est de 20000 à répartir entre action, oprion et bond
problem += xa *20 + xo*1000 + xb*90 <= 20000


# Résolution du problème
sol = problem.solve()

# Affichage des résultats
print ("---------- Résultat de la question 6.2 : ----------")
print(value(xa), value(xb), value(xo), value(problem.objective))

