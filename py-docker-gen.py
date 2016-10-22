from docker import Client
import jinja2
import json
import requests
import os
import re
import click
from urlparse import parse_qs, urlparse
import hashlib
import subprocess

templateLoader = jinja2.FileSystemLoader( searchpath=os.getcwd() )
templateEnv = jinja2.Environment( loader=templateLoader )

client = None
old_md5 = '0000000000000000000000000'

@click.command()
@click.argument('template')
@click.argument('output')
@click.option('--filter', default=None, help='Env Var that must be set for the containers')
@click.option('--listen/--genarate', default=True, help='Either listen for changes or genrate a file now')
@click.option('--command', default=None, help='Command to run when the file has been updated')
@click.option('--notify', default=None, help='Container to notify of changes')
@click.option('--socket', default='unix://var/run/docker.sock')
def cli(template, output, filter, listen, command, notify, socket):
    global client
    client = Client(base_url=socket)
    if listen:
        listenForEvents(template, output, filter, command, notify)
    else:
        generateTemplate(template, output, filter)

def md5File(file):
    try:
        return hashlib.md5(open(file, 'rb').read()).hexdigest()
    except:
        return hashlib.md5('File not found').hexdigest()


def generateTemplate(template_name, output, filter=None):
    hostfinder = re.compile('%s=.*' % filter)
    context = []

    for container in client.containers():
        details = client.inspect_container(container['Id'])
        if filter == None or any(hostfinder.match(env) for env in details['Config']['Env']):
            envs = {}
            for env in details['Config']['Env']:
                bits = env.split('=')
                envs[bits[0]] = bits[1]

            details['Config']['Env'] = envs

            details['NetworkSettings']['Ports'] = [port.split('/')[0] for port in details['NetworkSettings']['Ports']]
            context.append(details)

    template = templateEnv.get_template(template_name)
    outputText = template.render({'containers': context})

    with open(output, 'w') as f:
        f.write(outputText)
    

def listenForEvents(template, output, filter=None, command=None, notify=None):
    click.echo('Listening for docker events')
    old_md5 = md5File(output)
    for raw_event in client.events():
        event = json.loads(raw_event)
        if 'status' in event and event['status'] in ['start', 'die']:
            click.echo("%s event" % event['status'])
            generateTemplate(template, output, filter)
            
            new_md5 = md5File(output)
            if new_md5 != old_md5:
                click.echo('File changed')
                old_md5 = new_md5
                if command != None:
                    click.echo("Running %s" % command)
                    subprocess.call(command, shell=True)
                if notify != None:
                    click.echo("Sending SIGHUP to %s" % notify)
                    client.kill(notify, 1)
            else:
                click.echo('No change')


if __name__ == '__main__':
    cli()
