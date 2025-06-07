# MiniCoop

MiniCoop est un ensemble de petites applications Streamlit simulant un service de livraison de repas.

## Applications disponibles

- **client.py** : passer une commande directement.
- **resto.py** : interface restaurant pour consulter les commandes en attente.
- **admin.py** : attribuer un coursier aux commandes.
- **coursier.py** : interface pour les coursiers.
- **marketplace.py** : page de *place de marché* pour parcourir les restaurants et commander directement depuis leur menu.

Les commandes sont stockées dans le fichier `data.csv`.

## Lancer une application

Installez les dépendances puis exécutez le fichier souhaité avec Streamlit.

```bash
pip install streamlit pandas
streamlit run marketplace.py  # exemple pour démarrer la marketplace
```
