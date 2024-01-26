#!/bin/bash
python /odoo/scripts/set_base_url.py -c $ODOO_RC -d $DB_NAME --log-level=error --domain "$DOMAIN"

if [[ -n "$ADMIN_USER_PWD" && "$CHANGE_ADMIN_USER_PWD" == "true" ]]; then
  python /odoo/scripts/change_password.py -c $ODOO_RC -d $DB_NAME --log-level=error --login admin --password "$ADMIN_USER_PWD"
fi

if [[ -n "$SMTP_HOST" && "$SETUP_SMTP" == "true" ]]; then
  python /odoo/scripts/setup_smtp.py -c $ODOO_RC -d $DB_NAME --log-level=error --host "$SMTP_HOST" --user "$SMTP_USER" --password "$SMTP_PASSWORD"
fi

if [[ "$PREPARE_CUSTOMER_USER" == "true" ]]; then
  python /odoo/scripts/prepare_customer_user.py -c $ODOO_RC -d $DB_NAME --log-level=error --email "$COMPANY_EMAIL" --group-file /odoo/scripts/groups.txt
fi

if [[ "$UPDATE_COMPANY" == "true" ]]; then
  python /odoo/scripts/update_company.py -c $ODOO_RC -d $DB_NAME --log-level=error --name "$COMPANY_NAME" --email "$COMPANY_EMAIL" --coc "$COMPANY_COC" --city "$COMPANY_CITY" --zip "$COMPANY_ZIP" --street "$COMPANY_STREET"
fi

# python /odoo/scripts/prepare_install_request_mail.py -c $ODOO_RC -d $DB_NAME --log-level=error --email "ict@onestein.nl"

if [[ -n "$UNINSTALL_MODULES" && "$UNINSTALL_MODULES" == "True" ]]; then
  python /odoo/scripts/apply_modules.py -c $ODOO_RC -d $DB_NAME --log-level=error --modules "$MODULES" --do-uninstall
else
  python /odoo/scripts/apply_modules.py -c $ODOO_RC -d $DB_NAME --log-level=error --modules "$MODULES"
fi

python /odoo/scripts/uninstall_auto_install_modules.py -c $ODOO_RC -d $DB_NAME --log-level=error

if [[ -n "$KEYCLOAK_URL" ]]; then
  python /odoo/scripts/setup_oauth.py -c $ODOO_RC -d $DB_NAME --log-level=error --url "$KEYCLOAK_URL" --realm "$KEYCLOAK_REALM" --client-id "$KEYCLOAK_CLIENT_ID" --client-secret "$KEYCLOAK_CLIENT_SECRET"
fi

python /odoo/scripts/localize.py
