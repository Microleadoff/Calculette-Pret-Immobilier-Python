# calculatrice_pret_immo_Python

## Description

Calculatrice de prêt immobilier avec tableau d'amortissement, mois par mois, exportable en PDF.

## Pré-requis

Connaissance en Python CLI
Python 3.12 (stable à ce jour) https://www.python.org/downloads/
Extension pour l'IDE (ici VsCode : https://code.visualstudio.com/docs/python/python-tutorial)

## Installation

    - Installation de Python CLI et des extension IDE
    - Installation des bibliothèques et modules complémentaires : 
        - pip install fpdf 
    - Extension pour visualisation ds VsCode : 
        - vscode-pdf 
    - Lancer le server Python depuis la page app.py (execution du script)

## Méthodes de calculs

    L'utilisateur doit rentrer 3 données : 
        - montant du crédit
        - taux nominal annuel
        - durée de remboursement en années
    
    L'EMI (échéance mensuelle d'amortissement) est l'échéance total du mois, elle comprend le remboursement du capital emprunté et les intérêts de la mensualité.
    
    La formule de calcul : EMI = P x r(1+r)^n/(1+r)^n-1
        - P = montant initial du prêt
        - r = le taux d'intérêt mensuel en centième
        - n = le nombre de mensualités
        
    Exemple :
        montant : 100 000 €
        taux : 1.2 %
        durée : 15 ans

        P = 100 000
        r = 1.2/12 = 0.10% = 0.001
        n = 15 x 12 = 180

        EMI = P x ((r((1+r)^n)) / (((1+r)^n)-1)) 
                ==>> formule avec toutes les parenthèses pour décomposition du calcul
            (1+r) = (1 + 0.001) = 1.001
            (1+r)^n = 1.001^180 = 1.1971

            r((1+r)^n) = 0.001 x 1.1971 = 0.0012
            ((1+r)^n)-1 = 1.1971 - 1 = 0.1971

            ((r((1+r)^n)) / (((1+r)^n)-1)) = 0.0012 / 0.1971 = 0.0061
        
        EMI = 100 000 x ((0.001((1+0.001)^180)) / (((1+0.001)^180)-1)) 
        EMI = 100 000 x 0.0061 = 607.33

    Le tableau d'amortissement :
        solde initial (reporté chaque nouvelle mensualité)
        l'EMI (échéance)
        les intérêts (mensuel) : solde initial x r 
        l'amortissement : L'EMI - intérêts mensuel
        solde restant : solde initial - l'amortissement

        dans notre exemple :
        mois    solde initial   échéance    intérêts    amortissement   solde restant
        1       100 000         607.33      100         507.33          99 492.67
        2       99 492.67       607.33      99.49       507.84          98 984.83
        ...
