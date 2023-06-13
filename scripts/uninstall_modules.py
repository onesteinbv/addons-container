import click
import click_odoo


def _recurse_dependencies(env, modules):
    all_modules = modules
    for module in modules:
        all_modules += _recurse_dependencies(env, module.dependencies_id.mapped("depend_id"))
    return all_modules


@click.command()
@click_odoo.env_options(default_log_level="error")
# @click.option("--module", "-m", multiple=True, default=[])
@click.option("--modules")
def main(env, modules):
    modules = list(map(lambda m: m.strip(), modules.split(",")))
    click.echo("Uninstalling modules...")
    modules = env["ir.module.module"].search([
        ("name", "in", modules)
    ])
    installed_modules = env["ir.module.module"].search([
        ("state", "=", "installed"),
        ("auto_install", "=", False)
    ])
    desired_modules = _recurse_dependencies(env, modules)
    to_uninstall = installed_modules - desired_modules

    click.echo("Founds %s modules to uninstall: %s" % (len(to_uninstall), ", ".join(to_uninstall.mapped("name"))))


if __name__ == '__main__':
    main()
