{% for container in containers %}
  {% if container.Config.Env.port %}
upstream {{ container.Config.Env.hostname }} {
    server {{ container.NetworkSettings.FirstIPAddress }}:{{ container.Config.Env.port }};
}
    {% endif %}
{% endfor %}

server {
  server_name _;
  listen 80;

{% for container in containers %}
  {% if container.Config.Env.port %}
  location /{{ container.Config.Env.hostname }} {
      proxy_pass http://{{ container.Config.Env.hostname }};
  }
  {% endif %}  
{% endfor %}
}
