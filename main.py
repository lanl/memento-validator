import click
from mementoweb.apps.daily_validator.main import run as daily_validator_run


@click.group()
def daily_validator():
    pass


@daily_validator.command()
@click.option("--env", default="daily-validator.env", help="Location of the .env configuration")
def daily(env):
    daily_validator_run(env)


@click.group()
def cli_validator():
    pass


@cli_validator.command()
@click.option("--uri", help="URI of the resource")
@click.option("--type", "type_",
              type=click.Choice(["original", "memento", "timemap", "timegate"], case_sensitive=False),
              help="Type of resource")
@click.option("--date", default="Sun, 01 Apr 2010 12:00:00 GMT", help="Date Time for testing the resource")
@click.option("--follow", default=False, help="Follow up tests or not")
def cli(uri, type_, date, follow):
    print(uri)
    print(type_)
    print(date)
    print(follow)


command_collection = click.CommandCollection(sources=[daily_validator, cli_validator])
if __name__ == '__main__':
    print("""
        ___  ___                          _                    _     
        |  \/  |                         | |                  | |    
        | .  . | ___ _ __ ___   ___ _ __ | |_ _____      _____| |__  
        | |\/| |/ _ \ '_ ` _ \ / _ \ '_ \| __/ _ \ \ /\ / / _ \ '_ \ 
        | |  | |  __/ | | | | |  __/ | | | || (_) \ V  V /  __/ |_) |
        \_|  |_/\___|_| |_| |_|\___|_| |_|\__\___/ \_/\_/ \___|_.__/ 
    """)
    command_collection()
