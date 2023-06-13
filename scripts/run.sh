#!/bin/bash
gosu odoo python /odoo/scripts/set_base_url.py -d $DB_NAME --log-level=error --domain "$DOMAIN"

if [[ -n "$ADMIN_USER_PWD" && "$CHANGE_ADMIN_USER_PWD" == "true" ]]; then
  gosu odoo python /odoo/scripts/change_password.py -d $DB_NAME --log-level=error --login admin --password "$ADMIN_USER_PWD"
fi

if [[ -n "$SMTP_HOST" && "$SETUP_SMTP" == "true" ]]; then
  gosu odoo python /odoo/scripts/setup_smtp.py -d $DB_NAME --log-level=error --host "$SMTP_HOST" --user "$SMTP_USER" --password "$SMTP_PASSWORD"
fi

if [[ "$PREPARE_CUSTOMER_USER" == "true" ]]; then
  gosu odoo python /odoo/scripts/prepare_customer_user.py -d $DB_NAME --log-level=error --email "$COMPANY_EMAIL" --group-file /odoo/scripts/groups.txt
fi

if [[ "$UPDATE_COMPANY" == "true" ]]; then
  gosu odoo python /odoo/scripts/update_company.py -d $DB_NAME --log-level=error --name "$COMPANY_NAME" --email "$COMPANY_EMAIL" --coc "$COMPANY_COC" --city "$COMPANY_CITY" --zip "$COMPANY_ZIP" --street "$COMPANY_STREET"
fi

gosu odoo python /odoo/scripts/uninstall_modules.py -d $DB_NAME --log-level=error --modules "$MODULES"
