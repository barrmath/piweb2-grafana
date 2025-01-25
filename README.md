# piweb2-grafana

Crée une base de donnée mariadDB ainsi que grafana

prèrequis :

- [podman](https://podman.io/)

Grafana avec [podman](https://podman.io/) :

construire image:

```shell
podman build -f Dockerfile -t piweb-grafana
```

Démarrage grafana :

```shell
podman-compose up -d
```

Arrêt grafana :

```shell
podman-compose down
```

Allez sur votre [localhost port 4000](http:127.0.0.1:4000) et vous pouvez commencer à travailler sur les données.