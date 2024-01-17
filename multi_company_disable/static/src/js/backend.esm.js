/** @odoo-module **/

import { registry } from "@web/core/registry";
import { } from "@web/webclient/switch_company_menu/switch_company_menu";
import { MobileSwitchCompanyMenu } from "@web/webclient/burger_menu/mobile_switch_company_menu/mobile_switch_company_menu";
const { xml } = owl;

registry.category("systray").remove("SwitchCompanyMenu")

MobileSwitchCompanyMenu.template =  xml`<div></div>`;
