import click
import click_odoo


def _recurse_dependencies(env, modules):
    all_modules = modules
    for module in modules:
        all_modules += _recurse_dependencies(env, module.dependencies_id.mapped("depend_id"))
    return all_modules


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--modules")
@click.option("--do-uninstall", is_flag=True, default=False)
def main(env, modules, do_uninstall):
    modules = list(map(lambda m: m.strip(), modules.split(",")))
    click.echo("Applying modules...")
    modules = env["ir.module.module"].search([
        ("name", "in", modules)
    ])
    installed_modules = env["ir.module.module"].search([
        ("state", "=", "installed"),
        ("auto_install", "=", False)
    ])
    desired_modules = _recurse_dependencies(env, modules)
    to_uninstall = installed_modules - desired_modules

    click.echo("Install modules...")
    modules.button_immediate_install()

    click.echo("Found %s modules to uninstall: %s" % (len(to_uninstall), ", ".join(to_uninstall.mapped("name"))))
    if do_uninstall:
        click.echo("Uninstalling...")
        to_uninstall.button_immediate_uninstall()
    else:
        click.echo("Not uninstalling")


if __name__ == '__main__':
    main()
