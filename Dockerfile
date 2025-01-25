FROM registry.hub.docker.com/grafana/grafana-oss:latest

EXPOSE 3000

CMD ["grafana-server"]