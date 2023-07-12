import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--email")
@click.option("--group-file", default=None)
@click.option("--group", "-g", multiple=True, default=[])
def main(env, email, group_file, group):
    groups = list(group)
    if group_file:
        with open(group_file, "r") as f:
            for line in f:
                line = line.replace("\n", "")
                if not line:
                    continue
                groups.append(line)

    click.echo("Update customer user...")
    customer_user = env.ref("base_customer_user.user_customer", raise_if_not_found=False)
    group_ids = []
    if customer_user:
        if customer_user.login == "customer_user":
            customer_user.write({
                "login": email
            })
            customer_user.partner_id.write({
                "email": email
            })

        if customer_user.state == "new":
            group_ids.append(
                env.ref("base_onboarding.onboarding_group").id
            )
            try:
                customer_user.action_reset_password()
            except Exception as e:
                click.echo(click.style(str(e), fg="red"))

        # Assign groups
        for group_xml_id in groups:
            group_record = env.ref(group_xml_id, raise_if_not_found=False)
            if group_record:
                group_ids.append(group_record.id)
            else:
                click.echo(click.style("Group `%s` doesn't exists" % group_xml_id, fg="red"))
        customer_user.write({
            "groups_id": [(6, 0, group_ids)]
        })
    else:
        click.echo("Customer user doesn't exists", err=True)


if __name__ == '__main__':
    main()
