/** @odoo-module */
import { WebClient } from "@web/webclient/webclient";
import { onMounted } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";


patch(WebClient.prototype, "base_onboarding", {
    setup() {
        this._super();
        const userService = useService("user");
        const actionService = useService("action");

        onMounted(async () => {
            const hasOnboardingGroup = await userService.hasGroup("base_onboarding.onboarding_group");
            if (hasOnboardingGroup) {
                actionService.doAction("base_onboarding.onboarding_wizard_action", {
                    onClose: () => {
                        actionService.doAction({
                            type: "ir.actions.client", tag: "reload"
                        });
                    }
                });
            }
        });
    }
});
