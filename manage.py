#!/usr/bin/env python

import os

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean
from appname import create_app
from appname.models import db, User

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('appname.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, User=User)


@manager.command
def create_tables():
    db.create_all()


@manager.command
def drop_tables():
    db.drop_all()


@manager.command
def create_superuser():
    if User.query.count() == 1:
        if not Role.query.count():
            superuser = Role()
            superuser.name = 'superuser'
            superuser.description = 'superuser'
            db.session.add(superuser)
            db.session.commit()
        else:
            superuser = Role.query.filter(Role.name == 'superuser').one()
        admin = User.query.first()
        admin.roles.append(superuser)
        db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
def create_admin(email, password):
    admin = User()
    admin.email = email
    admin.password = encrypt_password(password)
    admin.active = True
    admin.confirmed_at = datetime.now(tzlocal())
    db.session.add(admin)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
