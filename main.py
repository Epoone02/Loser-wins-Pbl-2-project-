class Arbre:

  def __init__(self, e, f1, f2):
    self.donnee = e
    self.filsG = f1
    self.filsD = f2

  def insert(self, valeur):
    a = self
    continuer = True
    while continuer:
      if valeur < a.donnee:
        if a.filsG is None:
          a.filsG = Arbre(valeur, None, None)
          continuer = False
        else:
          a = a.filsG
      else:
        if a.filsD is None:
          a.filsD = Arbre(valeur, None, None)
          continuer = False
        else:
          a = a.filsD


def insertion(arbre, val):
  arbre = arbre
  continuer = True
  while continuer:
    if val < arbre.donnee:
      if arbre.filsG is None:
        arbre.filsG = Arbre(val, None, None)
        continuer = False
      else:
        arbre = arbre.filsG
    else:
      if arbre.filsD is None:
        arbre.filsD = Arbre(val, None, None)
        continuer = False
      else:
        arbre = arbre.filsD


def genereABR(liste):
  arbre = Arbre(liste[0], None, None)
  for valeur in liste[1:]:
    insertion(arbre, valeur)
  return arbre

def parcoursI(arbre):
  if arbre is None:
    return []
  else:
    return parcoursI(arbre.filsG) + [arbre.donnee] + parcoursI(arbre.filsD)
  
def minABR(arbre):
  a = arbre
  while a.filsG is not None:
    a = a.filsG
  return a.donnee