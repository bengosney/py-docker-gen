# py-docker-gen

Inspired by [docker-gen](https://github.com/jwilder/docker-gen)

This will listen to docker for events then uses docker to populate a Jina2 template and run a command.

## Example useage

Automaticly creating nginx reverse proxy configs.

```
Usage: py-docker-gen.py [OPTIONS] TEMPLATE OUTPUT

Options:
  --filter TEXT          Env Var that must be set for the containers
  --listen / --genarate  Either listen for changes or genrate a file now
  --command TEXT         Command to run when the file has been updated
  --help                 Show this message and exit.
```


### Templates

The jinja2 templates have access to an array called `containers` that, suprisingly, contains all the containers. Eash container has all the info from `docker info`.


## Misc

Jinja2 should be used for more things, it's not just for HTML templates.

[Click](http://click.pocoo.org/6/) is amazing if your doing anything on the command line.

## Why
Why do this when docker-gen excists? I'm lazy, I couldn't get docker-gen to work and I'm too lazy to learn Go.
