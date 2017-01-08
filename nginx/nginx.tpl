{% for container in containers %}
upstream {{ container.Config.Env.hostname }} {
  server {{ container.NetworkSettings.IPAddress }}:{{ container.Config.Env.port }};
}
{% endfor %}

server {
  server_name _;
  listen 80;

{% for container in containers %}
  location /{{ container.Config.Env.hostname }} {
      proxy_pass http://{{ container.Config.Env.hostname }};
  }
{% endfor %}
}
