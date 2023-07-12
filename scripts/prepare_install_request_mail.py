import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--email")
def main(env, email):
    click.echo("Change `Install request` email")
    mail_template = env.ref("base_install_request.mail_template_base_install_request")
    mail_template.email_to = email


if __name__ == '__main__':
    main()
