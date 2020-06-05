import click
import json
import requests as req


@click.group()
def messages():
    pass


@click.command()
def health_check():
    url = "http://0.0.0.0:8000/"
    resp = req.get(url)

    click.echo("***Output of health check on backend*** \n")
    click.echo("Response: \n" + (resp.text) + "\n")
    click.echo("Status Code: \n" + str(resp))


@click.command()
@click.option(
    "--full_name",
    default="rachel",
    required=True,
    type=(str),
    help="What is your name? e.g. --full_name='Rachel Liu'",
)
@click.option(
    "--email",
    default="rachel4@gmail.com",
    required=True,
    type=(str),
    help="What is your email? e.g. --email='rachel@gmail.com'",
)
@click.option(
    "--password",
    default="rachel123badpass",
    required=True,
    type=(str),
    help="What is your password of choice? Passwords must be at least eight characters in length.",
)
def register(full_name, email, password):
    url = "http://0.0.0.0:8000/users"
    payload = {"full_name": full_name, "email": email, "password": password}
    resp = req.post(url, data=json.dumps(payload))

    click.echo("***Output of POST request on /users*** \n")
    click.echo("Response: \n" + (resp.text) + "\n")
    click.echo("Status Code: \n" + str(resp))


@click.command()
@click.option(
    "--username", 
    default="rachel4@gmail.com", 
    required=True, 
    type=(str)
)
@click.option(
    "--password", 
    default="rachel123badpass", 
    required=True, 
    type=(str)
)
def login(username, password):
    url = "http://0.0.0.0:8000/token/"

    payload = {"username": username, "password": password}
    resp = req.post(url, data=payload)

    click.echo("***Output of POST request on /token*** \n")
    click.echo("Response: \n" + (resp.text) + "\n")
    click.echo("Status Code: \n" + str(resp))


@click.command()
@click.option(
    "--order_id",
    default="0",
    required=True,
    type=(str),
    help="What is the id of the order you want to look up? e.g. --order_id='1'",
)
@click.option(
    "--platform_id",
    default=1,
    required=True,
    type=(int),
    help="What is the id of your platform of choice? e.g. --platform_id=1",
)
@click.option(
    "--status",
    default=1,
    required=True,
    type=(int),
    help="What is the status of the order? e.g. --status=1",
)
@click.option(
    "--user_email",
    default="rachel4@gmail.com",
    required=True,
    type=(str),
    help="What is your user email? e.g. --user_email='rachel@gmail.com'",
)
@click.option(
    "--auth_token",
    default="",
    required=True,
    type=(str),
    help="What is your auth_token upon login? hint: Bearer Token",
)
def create_order(order_id, platform_id, status, user_email, auth_token):
    head = {'Authorization': 'Bearer ' + auth_token}

    url = "http://0.0.0.0:8000/orders/"
    payload = {
        "order_id": order_id,
        "platform_id": platform_id,
        "status": status,
        "user_email": user_email,
    }
    resp = req.post(url, data=json.dumps(payload), headers = head)

    click.echo("***Output of POST request on /orders*** \n")
    click.echo("Response: \n" + (resp.text) + "\n")
    click.echo("Status Code: \n" + str(resp))


@click.command()
@click.option(
    "--email",
    default="rachel4@gmail.com",
    required=True,
    type=(str),
    help="What is the id of the order you want to look up? e.g. --order_id='1'",
)
@click.option(
    "--auth_token",
    default="",
    required=True,
    type=(str),
    help="What is your auth_token upon login? hint: Bearer Token",
)
def show_orders(email, auth_token):
    url = "http://0.0.0.0:8000/orders/" + email
    head = {'Authorization': 'Bearer ' + auth_token}

    resp = req.get(url, headers=head )
    click.echo("***Output of GET request on /orders*** \n")
    click.echo("Response: \n" + (resp.text) + "\n")
    click.echo("Status Code: \n" + str(resp))



messages.add_command(health_check)
messages.add_command(register)
messages.add_command(login)
messages.add_command(create_order)
messages.add_command(show_orders)


if __name__ == "__main__":
    messages()
