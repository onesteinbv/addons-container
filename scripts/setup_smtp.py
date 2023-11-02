import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--host")
@click.option("--user")
@click.option("--password")
def main(env, host, user, password):
    click.echo("Setup SMTP...")
    module_container_accessibility = env.ref("base.module_container_accessibility")
    if module_container_accessibility.state != "installed":
        return click.echo(
            "Module `container_accessibility` must be installed for this script to work",
            err=True
        )

    smtp_server = env["ir.mail_server"].search([
        ("private", "=", True)
    ])
    values = {
        "name": "Default SMTP",
        "smtp_authentication": "login",
        "smtp_encryption": "starttls",
        "smtp_port": 587,
        "sequence": 9999999,
        "smtp_host": host,
        "smtp_user": user,
        "smtp_pass": password,
        "private": True
    }
    if smtp_server:
        smtp_server.write(values)
    else:
        env["ir.mail_server"].create(values)


if __name__ == '__main__':
    main()
