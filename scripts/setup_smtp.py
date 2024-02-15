import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--host")
@click.option("--user")
@click.option("--password")
@click.option(
    "--encryption", type=click.Choice(["none", "starttls", "ssl"], case_sensitive=True)
)
@click.option("--port", type=int)
def main(env, host, user, password, encryption, port):
    click.echo("Setup SMTP...")
    module_container_accessibility = env.ref("base.module_container_accessibility")
    if module_container_accessibility.state != "installed":
        return click.echo(
            "Module `container_accessibility` must be installed for this script to work",
            err=True,
        )

    smtp_server = env["ir.mail_server"].search([("private", "=", True)])
    values = {
        "name": "Default SMTP",
        "smtp_authentication": "login",
        "smtp_encryption": encryption,
        "smtp_port": port,  # 587
        "sequence": 9999999,
        "smtp_host": host,
        "smtp_user": user,
        "smtp_pass": password,
        "private": True,
        "from_filter": user.split("@")[1],
    }
    if smtp_server:
        smtp_server.write(values)
    else:
        env["ir.mail_server"].create(values)
    mail_domain = user.split("@")[1]
    env["ir.config_parameter"].set_param(
        "mail.default.from", "notifications@" + mail_domain
    )


if __name__ == "__main__":
    main()
