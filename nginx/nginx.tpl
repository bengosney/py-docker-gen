server {
	server_name _; # This is just an invalid value which will never trigger on a real hostname.
	listen 80;
	return 503;
}

{% for container in containers %}
upstream {{ container.Config.Env.hostname }} {
  {%- for port in container.NetworkSettings.Ports %}
    {%- if port != '443' %}
      server {{ container.NetworkSettings.IPAddress }}:{{ port }};
    {%- endif %}
  {%- endfor %}
}

server {
  server_name {{ container.Config.Env.hostname }};
  listen 80;

  location / {
      proxy_pass http://{{ container.Config.Env.hostname }};
  }
}
{% endfor %}
