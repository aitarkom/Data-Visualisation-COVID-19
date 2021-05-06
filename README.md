# Data-Visualisation-COVID-19

## Table des matières

 - [Introduction](#Introduction)
 - [User's Guide](#users-Guide)
 - [Developer's Guide](#developers-Guide)
 - [Lien vers les datasets](#lien-vers-les-datasets)
 - [Instructions d'execution](#instructions-dexecution)

## Introduction

Ce dashboard a pour but de visualiser l'evolution du nombre de cas et du nombre de morts dues a la COVID a travers le monde

## User's Guide

Afin d'exécuter sans erreur ce code, il faudra installer tous les packages suivant dans votre invite de commande en tapant ceci : pip install le_nom_du_package.

Liste des librairies/packages utilisés :
- dash
- pandas
- dash_html_components
- dash_core_components
- dash.dependencies
- plotly.express
- json

Il est aussi possible d'installer tous ces packages directement via le requirements.txt en tapant la commande : **$ pip install -r requirements.txt**

Une fois les packages installés vous devez lancer l'application avec la commande : **py app.py**



## Developer's Guide

Ce guide mentionnera l'architecture et les fonctions utiles du projet ainsi que de potentielles pistes de développement.

#### L'architecture du projet

Le projet se décompose en 3 fichiers.
- app.py (initialise l'application et crée le serveur Dash. Il met aussi en forme et traite la data afin de la rendre exploitable.)
- requirements.txt (Liste de toutes les librairies nécessaire au lancements de l'application)
- README.md

#### Les différentes fonctions présentent dans le projet

Dans le fichier **app.py**<br>
> - La fonction delete_no_data_graph() ne prend pas de paramètre et renvoie la liste des pays dont on possède les données pour créer le dashboard.<br>
> - La fonction delete_no_data_map() crée un dashboard avec toutes les données nécéssaires a la mise en place de la carte choropleth.<br>
> - La fonction update_graphe_cas(country,cases) prend en argument le pays selectionné et les données choisies. Elle retourne les options choisies ainsi qu'une courbe.
> - La fonction update_graphe_mort(country,deaths) prend en argument le pays selectionné et les données choisies. Elle retourne les options choisies ainsi qu'une courbe.
> - La fonction update_map(data_map) prend en argument les données choisies. Elle retourne l'options choisies ainsi qu'une carte choropleth.

## Lien vers le dataset

Base de données : https://covid.ourworldindata.org/data/owid-covid-data.json<br>

## Instructions d'execution

- Télécharger le dossier "Data-Visualisation-COVID-19"
- Le dézipper
- Ouvrir l'invite de commande
- Se déplacer dans les répertoires afin que le répertoire courant soit Data-Visualisation-COVID-19
- installer les librairies requises (mentionnée dans le User's Guide)
- Rentrer cette ligne de commande dans l'invité : python app.py
