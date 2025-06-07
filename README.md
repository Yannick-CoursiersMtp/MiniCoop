# MiniCoop

Cette application Streamlit permet la gestion simplifiée des commandes pour un restaurant fictif.

- `data.db` est la base de données utilisée pour stocker les commandes.
- `data.csv` peut être présent à titre d'exemple local, mais il n'est plus suivi par Git.

Les interfaces disponibles sont les suivantes :

- `admin.py` : administration des commandes et attribution des coursiers;
- `client.py` : prise de commandes côté client;
- `resto.py` : suivi des commandes côté restaurant;
- `coursier.py` : consultation des livraisons pour chaque coursier.

Lancez l'application principale avec `streamlit run resto.py`.
