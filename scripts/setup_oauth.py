import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--url")
@click.option("--realm")
@click.option("--client-id")
@click.option("--client-secret")
def main(env, url, realm, client_id, client_secret):
    click.echo("Setup Keycloak...")
    module_container_accessibility = env.ref("base.module_container_accessibility")
    if module_container_accessibility.state != "installed":
        return click.echo(
            "Module `container_accessibility` must be installed for this script to work",
            err=True
        )

    keycloak = env["auth.oauth.provider"].search([
        ("private", "=", True)
    ])
    values = {
        "name": "Keycloak Onestein",
        "flow": "id_token_code",
        "token_map": "preferred_username:user_id",
        "client_id": client_id,
        "client_secret": client_secret,
        "enabled": True,
        "body": "Support Login",
        "css_class": "fa fa-fw fa-support text-primary",
        "auth_endpoint": "%s/realms/%s/protocol/openid-connect/auth" % (url, realm),
        "scope": "openid email",
        "token_endpoint": "%s/realms/%s/protocol/openid-connect/token" % (url, realm),
        "jwks_uri": "%s/realms/%s/protocol/openid-connect/certs" % (url, realm),
        "private": True
    }
    if keycloak:
        keycloak.write(values)
    else:
        env["auth.oauth.provider"].create(values)

    click.echo("Remove Odoo.com login...")
    provider_openerp = env.ref("auth_oauth.provider_openerp", raise_if_not_found=False)
    if provider_openerp:
        provider_openerp.unlink()


if __name__ == '__main__':
    main()
