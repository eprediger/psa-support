import click
from flask_cli import with_appcontext

from main.db.database import db
from main.models import Cliente, Ticket, TicketTarea

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()