FROM registry.hub.docker.com/grafana/grafana-oss:latest

RUN grafana cli plugins install yesoreyeram-infinity-datasource

EXPOSE 3000

CMD ["grafana-server"]