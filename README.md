# JIRA-WORKLOAD

Project to extract from JIRA the workload assigned to a component. Extract the workload to an excel file.

# Requirements

## Etape 1 - installation des outils
Installer python 3 => https://www.python.org/downloads/
Installer git => https://git-scm.com/downloads/win

Créer un répertoire "jiraLoader" et téléchargez le projet via les commandes suivantes : 

Dans un terminal, tapez : 
cd <chemin de votre répertoire jiraLoader>
git clone https://github.com/wizaord/jira-workload.git .

## Etape 2 - Initialisez le fichier configuration.ini

Dans le répertoire 'src', copiez le fichier `configuration_template.ini` dans le même répertoire mais avec le nom `configuration.ini`
Remplissez ensuite dans le fichier 'configuration.ini' les informations suivantes : 

- Pour Username, indiquez votre email
- Pour Api_token, indiquez la valeur de votre token JIRA
- Pour ComponentName, indiquez Seittra
- Pour liste_utilisateurs, indiquez la ligne suivante : i.thibault@seiitra.com, s.trirach.ext@seiitra.com,c.mirou@seiitra.com,m.barik.ext@seiitra.com,y.cheikhani.ext@seiitra.com,g.bernard.ext@seiitra.com,k.mckenna.ext@seiitra.com


## Etape 3 - Lancer l'application

Double cliquez sur le fichier "run.bat"

