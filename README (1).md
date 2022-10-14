# Prosper Loans data Exploration
## by Mayo Takémsi Norris KADANGA


## Dataset

Ce présent document porte sur l'analyse exploratoire de la base ProsperLoans, une base de 113937 lignes ou observations et 81 colonnes. Elle nous renseigne sur les demandeurs de prêts aux Etats-Unis ainsi que leurs différentes caractéristiques.


## Summary of Findings

Les différentes types d'analyses à savoir, univariées, bivariées et multivariées nous ont permis de trouver  des résultats assez pertinents. Les individus dont le remboursement du prêt est toujours en cours démeurent les plus nombreux. Aussi, nous avons remarqué que les taux d'intérêts ne dépassent pas les 40%.   Certaines caractéristiques des demandeurs de prêts affectent le satut du remboursement de leurs prêts, il s'agit par exemple du statut profession de l'emprunteur ou encore du niveau de son revenu. Les taux annuels quant à eux augmentent selon le classement de AA à HR.

## Key Insights for Presentation

Pour la présentation, j'ai investie mes analyses sur l'influence des certaines variables que j'ai jugé comme étant de potentiels prédicteurs de mes variables d'intérêts à savoir Le statut du prêt(LoanStatus) et le taux annuels (BorrowerAPR). 
Pour commencer, j'ai d'abord analyser la distribution de la variable d'intérêt LoanStatus, puis je me suis intéressé à distribution  de la variable IsBorrowerHomeowner, qui joue un important rôle d'après l'analyse exploratoire. D'après mes analyses dans la  partie exploratoire, j'ai observé une forte corrélation entre les taux annuels et les montants initiaux des prêts et aussi une forte influence des diffirents classements des individus sur leurs taux d'intérêts annuels. J'ai donc poursuivie avec un graphique comportant deux diagrammes bivariés, des boîtes à mostatches, mettant en relation BorrowerAPR et ProsperRating (Alpha) d'une part, 'LoanOriginalAmount et ProsperRating (Alpha) d'autre part. 
Pour finir, j'ai réaliser un graphique multivarié mettant en relation trois variables à travers un diagramme à barres, 'LoanOriginalAmount et LoanStatus, puis IsBorrowerHomeowner. J'ai utilisé l'encodage de couleur pour faire apparâitre l'effet de la troisième variable. 
