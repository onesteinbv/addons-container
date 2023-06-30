import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--host")
@click.option("--user")
@click.option("--password")
def main(env, host, user, password):
    click.echo("Setup SMTP...")

    count_server = env["ir.mail_server"].search([], count=True)
    if count_server:
        click.echo("Already have a SMTP server")
        return

    values = {
        "name": "Default SMTP",
        "smtp_authentication": "login",
        "smtp_encryption": "starttls",
        "smtp_port": 587,
        "sequence": 9999999,
        "smtp_host": host,
        "smtp_user": user,
        "smtp_pass": password,
    }
    env["ir.mail_server"].create(values)


if __name__ == '__main__':
    main()
