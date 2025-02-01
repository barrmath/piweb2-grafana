# piweb2-grafana

Crée une base de donnée mariadDB ainsi que grafana

prèrequis :

- [podman](https://podman.io/)

Grafana avec [podman](https://podman.io/) :

construire image:

```shell
podman build -f Dockerfile -t piweb-grafana
```

configurer votre DB avec db.env

```shell
touch db.env
nano db.env
```

mettre vos mots de passe dans db.env

```shell
MYSQL_ROOT_PASSWORD=Root_password
MYSQL_PASSWORD=password_user
MYSQL_USER=USR
MYSQL_DATABASE=DB_name
```

configurer votre grafana avec grafana.env

```shell
touch db.env
nano grafana.env
```

mettre votre config grafana dans grafana.env

```yaml
GF_SERVER_ROOT_URL=Adresse_grafana
GF_SERVER_SERVE_FROM_SUB_PATH=true
#GF_SERVER_ENABLE_GZIP=true
```


Démarrage grafana :

```shell
podman-compose up -d
```

Arrêt grafana :

```shell
podman-compose down
```

Allez sur votre [localhost port 4000](http:127.0.0.1:4000) ou votre site internet et vous pouvez commencer à travailler sur les données.

PS : nginx et grafana.

si vous voulez que votre grafana utilise le reverse proxy nginx :
ajoutez le chemin ou vous voulez grafana dans la variable GF_SERVER_ROOT_URL
ajoutez GF_SERVER_SERVE_FROM_SUB_PATH=true

Dans nginx.conf
ajoutez dans la session html:

```yaml
    proxy_max_temp_file_size 0;
    proxy_buffering off;

    upstream grafana {
      server localhost:4000;
        }

    server {
    [...]
        location /grafana {
                proxy_set_header Host $http_host;
                proxy_pass http://grafana;
                }
            }
```

Vous configurez le serveur_name et le port d'ecoute selon votre configuration.
Le proxy_buffering off; ainsi que le poxy_max_temp_file_size 0; permettent de corriger les erreur 206 pouvant apparaître. (écran Grafana : failed to load application file)