odoo.define('website_device_visibility.snippets.editor', function (require) {
'use strict';

const snippetsEditor = require('web_editor.snippet.editor');

snippetsEditor.SnippetsMenu.include({
    /**
     * @override
     */
    _updateInvisibleDOM: function () {
        return this._execWithLoadingEffect(() => {
            this.options.wysiwyg.odooEditor.automaticStepSkipStack();
            this.invisibleDOMMap = new Map();
            const $invisibleDOMPanelEl = $(this.invisibleDOMPanelEl);
            $invisibleDOMPanelEl.find('.o_we_invisible_entry').remove();
            const invisibleSelector = '.o_snippet_invisible,.o_snippet_mobile_invisible,.o_snippet_desktop_invisible';
            const $invisibleSnippets = snippetsEditor.globalSelector.all().find(invisibleSelector).addBack(invisibleSelector);

            $invisibleDOMPanelEl.toggleClass('d-none', !$invisibleSnippets.length);

            const proms = _.map($invisibleSnippets, async el => {
                const editor = await this._createSnippetEditor($(el));
                const $invisEntry = $('<div/>', {
                    class: 'o_we_invisible_entry d-flex align-items-center justify-content-between',
                    text: editor.getName(),
                }).append($('<i/>', {class: `fa ${editor.isTargetVisible() ? 'fa-eye' : 'fa-eye-slash'} ml-2`}));
                $invisibleDOMPanelEl.append($invisEntry);
                this.invisibleDOMMap.set($invisEntry[0], el);
            });
            return Promise.all(proms);
        }, false);
    },
});

snippetsEditor.SnippetEditor.include({
    /**
     * @override
     */
    cleanForSave: async function () {
        if (this.isDestroyed()) {
            return;
        }
        this.willDestroyEditors = true;
        await this.toggleTargetVisibility(!this.$target.hasClass('o_snippet_invisible')
            && !this.$target.hasClass('o_snippet_mobile_invisible')
            && !this.$target.hasClass('o_snippet_desktop_invisible'));
        const proms = _.map(this.styles, option => {
            return option.cleanForSave();
        });
        await Promise.all(proms);
    },
});

});
