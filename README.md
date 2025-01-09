
# Script MACD Alert avec Alerte de Prix

## Description
Ce script surveille :
1. Le croisement des lignes MACD pour un token spécifique sur la blockchain Solana.
2. Un seuil de prix configurable par l'utilisateur.

Il envoie une alerte email lorsqu'un croisement MACD est détecté ou si le prix dépasse le seuil configuré.

## Installation sur Replit
1. Crée un compte ou connecte-toi sur [Replit](https://replit.com/).
2. Crée un nouveau projet Python.
3. Upload les fichiers de ce dossier dans ton projet.
4. Crée un fichier `.env` avec les variables d'email suivantes :
   - EMAIL_ADDRESS : Ton adresse Gmail
   - EMAIL_PASSWORD : Ton mot de passe Gmail
   - TO_EMAIL : Adresse email de destination

## Exécution
Clique sur **Run** dans Replit pour démarrer le script.
