/** @odoo-module **/
import { MobileSwitchCompanyMenu } from "@web/webclient/burger_menu/mobile_switch_company_menu/mobile_switch_company_menu";
import { registry } from "@web/core/registry";

const { xml } = owl;

registry.category("systray").remove("SwitchCompanyMenu")

MobileSwitchCompanyMenu.template =  xml`<div></div>`;
