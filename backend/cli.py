import click
from main import *
import json
import requests as req


@click.group()
def messages():
  pass


@click.command()
def health_check():
    url = 'http://0.0.0.0:8000/'
    resp = req.get(url)

    click.echo("***Output of health check on backend*** \n")
    click.echo('Response: \n' + (resp.text) + '\n')
    click.echo('Status Code: \n' + str(resp))


@click.command()
@click.option('--full_name', default='rachel', required=True, type=(str), help="What is your name? e.g. --full_name='Rachel Liu'")
@click.option('--email', default='rachel@gmail.com', required=True, type=(str),  help="What is your email? e.g. --email='rachel@gmail.com'")
@click.option('--password', default='rachel123badpass', required=True, type=(str), help="What is your password of choice? Passwords must be at least eight characters in length.")
def register_user(full_name, email, password):
    url = 'http://0.0.0.0:8000/users'
    payload = {
    'full_name': full_name, 
    'email': email,
    'password': password}
    resp = req.post(url, data=json.dumps(payload))
    
    click.echo("***Output of POST request on /users*** \n")
    click.echo('Response: \n' + (resp.text) + '\n')
    click.echo('Status Code: \n' + str(resp))

@click.command()
@click.option('--name', default='rachel', required=True, type=(str))
@click.option('--username', default='rachel@gmail.com', required=True, type=(str))
@click.option('--password', default='rachel123badpass', required=True, type=(str))
def login_user(name, username, password):
    url = 'http://0.0.0.0:8000/token/'
    
    payload = {
        'name': name,
    'username': username, 
    'password': password,
    }
    resp = req.post(url, data=payload)
    
    click.echo("***Output of POST request on /token*** \n")
    click.echo('Response: \n' + (resp.text) + '\n')
    click.echo('Status Code: \n' + str(resp))


@click.command()
@click.option('--order_id', default="0", required=True, type=(str), help="What is the id of the order you want to look up? e.g. --order_id='1'")
@click.option('--platform_id', default=1, required=True, type=(int), help="What is the id of your platform of choice? e.g. --platform_id=1")
@click.option('--status', default=1, required=True, type=(int), help="What is the status of the order? e.g. --status=1")
@click.option('--user_email', default="rachel@gmail.com", required=True, type=(str), help="What is your user email? e.g. --user_email='rachel@gmail.com'")
def create_order_for_user(order_id, platform_id, status, user_email):
    url = 'http://0.0.0.0:8000/orders/'
    payload = {
    'order_id': order_id,
    'platform_id': platform_id, 
    'status': status,
    'user_email': user_email,
    }
    resp = req.post(url, data=json.dumps(payload))

    click.echo("***Output of POST request on /orders*** \n")
    click.echo('Response: \n' + (resp.text) + '\n')
    click.echo('Status Code: \n' + str(resp))


messages.add_command(health_check)
messages.add_command(register_user)
messages.add_command(login_user)
messages.add_command(create_order_for_user)


if __name__ == '__main__':
    messages()