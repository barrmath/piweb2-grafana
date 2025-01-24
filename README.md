# piweb2-grafana

prèrequis :

- [python3](https://www.python.org/)
- [podman](https://podman.io/)

Grafana sur données education nationale niveau college

Pour les données (téléchargement et traitement):

```shell
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python data.py
```

Grafana avec [podman](https://podman.io/) :

construire image:

```shell
podman build -f Dockerfile -t piweb-grafana
```

Si besoin, ajouter ou modifier les variables d'environnement pour le docker de grafana avec le fichier grafana.env
(j'ai ajouter le nom de mon site en root-url par exemple)

Démarrage grafana :

```shell
podman-compose up -d
```

Arrêt grafana :

```shell
podman-compose down
```

Allez sur votre [localhost port 4000](http:127.0.0.1:4000) et vous pouvez commencer à travailler sur les données.