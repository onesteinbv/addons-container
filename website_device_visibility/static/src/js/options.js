odoo.define('website_device_visibility.snippets.options', function (require) {
'use strict';

const options = require('web_editor.snippets.options');
require('website.editor.snippets.options');

/**
 * Manage the visibility of snippets on mobile & desktop.
 */
options.registry.DeviceVisibility = options.Class.extend({
    isTopOption: true,

    /**
     * Allows to show or hide the associated snippet in mobile or desktop display mode.
     */
    toggleDeviceVisibility : async function (previewMode, widgetValue, params) {
        this.$target[0].classList.remove('d-none', 'd-md-none', 'd-lg-none',
            'o_snippet_mobile_invisible', 'o_snippet_desktop_invisible',
            'o_snippet_override_invisible'
        );
        const style = getComputedStyle(this.$target[0]);
        this.$target[0].classList.remove(`d-md-${style['display']}`, `d-lg-${style['display']}`);
        if (widgetValue === 'no_desktop') {
            this.$target[0].classList.add('d-lg-none', 'o_snippet_desktop_invisible','o_snippet_override_invisible');
        } else if (widgetValue === 'no_mobile') {
            this.$target[0].classList.add(`d-lg-${style['display']}`, 'd-none', 'o_snippet_mobile_invisible','o_snippet_override_invisible');
        }
        this.trigger_up('snippet_option_visibility_update', {show: true});
    },
    /**
     * @override
     */
    async onTargetHide() {
        this.$target[0].classList.remove('o_snippet_override_invisible');
    },
    /**
     * @override
     */
    async onTargetShow() {
        if (this.$target[0].classList.contains('o_snippet_mobile_invisible')
                || this.$target[0].classList.contains('o_snippet_desktop_invisible')) {
            this.$target[0].classList.add('o_snippet_override_invisible');
        }
    },
    /**
     * @override
     */
    cleanForSave: async function () {
        this.$target[0].classList.remove('o_snippet_override_invisible');
    },
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    async _computeWidgetState(methodName, params) {
        if (methodName === 'toggleDeviceVisibility') {
            const classList = [...this.$target[0].classList];
            if (classList.includes('d-none') &&
                    classList.some(className => className.match(/^d-(md|lg)-/))) {
                return 'no_mobile';
            }
            if (classList.some(className => className.match(/d-(md|lg)-none/))) {
                return 'no_desktop';
            }
            return '';
        }
        return await this._super(...arguments);
    },
});

options.registry.ConditionalVisibility.include({
    /**
     * @override
     */
    async onTargetHide() {
        if (this.$target[0].classList.contains('o_snippet_invisible')) {
            this.$target[0].classList.add('o_conditional_hidden');
        }
    },
})
});
