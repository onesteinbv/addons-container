# Copyright 2023 Onestein BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, models
from odoo.tools.float_utils import float_is_zero


class TrialBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.trial_balance"

    def _get_consolidation_groups_data(self, accounts_data, total_amount, foreign_currency):
        accounts_ids = list(accounts_data.keys())
        accounts = self.env["consolidation.account"].browse(accounts_ids)
        account_group_relation = {}
        for account in accounts:
            accounts_data[account.id]["complete_code"] = (
                account.group_id.complete_code + " / " + account.code
                if account.group_id.id
                else ""
            )
            if account.group_id.id:
                if account.group_id.id not in account_group_relation.keys():
                    account_group_relation.update({account.group_id.id: [account.id]})
                else:
                    account_group_relation[account.group_id.id].append(account.id)
        groups = self.env["consolidation.group"].browse(account_group_relation.keys())
        groups_data = {}
        for group in groups:
            groups_data.update(
                {
                    group.id: {
                        "id": group.id,
                        "code": group.code_prefix_start,
                        "name": group.name,
                        "parent_id": group.parent_id.id,
                        "parent_path": group.parent_path,
                        "type": "group_type",
                        "complete_code": group.complete_code,
                        "account_ids": group.compute_account_ids.ids,
                        "initial_balance": 0.0,
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": 0.0,
                        "ending_balance": 0.0,
                    }
                }
            )
            if foreign_currency:
                groups_data[group.id]["initial_currency_balance"] = 0.0
                groups_data[group.id]["ending_currency_balance"] = 0.0
        for group_id in account_group_relation.keys():
            for account_id in account_group_relation[group_id]:
                groups_data[group_id]["initial_balance"] += total_amount[account_id]["initial_balance"]
                groups_data[group_id]["debit"] += total_amount[account_id]["debit"]
                groups_data[group_id]["credit"] += total_amount[account_id]["credit"]
                groups_data[group_id]["balance"] += total_amount[account_id]["balance"]
                groups_data[group_id]["ending_balance"] += total_amount[account_id]["ending_balance"]
                if foreign_currency:
                    groups_data[group_id]["initial_currency_balance"] += total_amount[account_id]["initial_currency_balance"]
                    groups_data[group_id]["ending_currency_balance"] += total_amount[account_id]["ending_currency_balance"]
        group_ids = list(groups_data.keys())
        groups_data = self._get_hierarchy_groups(
            group_ids,
            groups_data,
            foreign_currency,
        )
        return groups_data

    def _compute_consolidation_accounts_data(self, consolidation_account_ids, data, accounts_data):
        chart_id = data['chart_id']
        show_hierarchy = data["show_hierarchy"]
        show_partner_details = data["show_partner_details"]
        foreign_currency = data["foreign_currency"]

        accounts_domain = [("chart_id", "=", chart_id)]
        if consolidation_account_ids:
            accounts_domain += [("id", "in", consolidation_account_ids)]
        consolidation_accounts = self.env["consolidation.account"].search(accounts_domain)

        new_accounts_data = {}

        AccountAccount = self.env['account.account']
        for key in accounts_data:
            item = accounts_data[key]
            account = AccountAccount.browse(item['id'])
            consolidation_account = account.consolidation_account_ids.filtered(lambda x: x.chart_id.id == chart_id)
            if consolidation_account and consolidation_account in consolidation_accounts:
                if not consolidation_account.id in new_accounts_data:
                    new_accounts_data[consolidation_account.id] = {
                        "id": consolidation_account.id,
                        "code": consolidation_account.code,
                        "name": consolidation_account.name,
                        "hide_account": False,
                        "group_id": consolidation_account.group_id.id,
                        "currency_id": consolidation_account.currency_id or False,
                        "currency_name": consolidation_account.currency_id.name,
                        "centralized": consolidation_account.centralized,
                    }

                    if not show_partner_details:
                        new_accounts_data[consolidation_account.id].update({
                            "initial_balance": 0.0,
                            "credit": 0.0,
                            "debit": 0.0,
                            "balance": 0.0,
                            "ending_balance": 0.0,
                            "type": "account_type",
                        })

                        if foreign_currency:
                            new_accounts_data[consolidation_account.id].update({
                                "ending_currency_balance": 0.0,
                                "initial_currency_balance": 0.0,
                            })

                    if show_hierarchy:
                        new_accounts_data[consolidation_account.id].update({
                            'complete_code': consolidation_account.group_id and (consolidation_account.group_id.complete_code + " / " + consolidation_account.code) or ''
                        })

                if not show_partner_details:
                    new_accounts_data[consolidation_account.id].update({
                        "initial_balance": new_accounts_data[consolidation_account.id]["initial_balance"] + item["initial_balance"],
                        "credit": new_accounts_data[consolidation_account.id]["credit"] + item["credit"],
                        "debit": new_accounts_data[consolidation_account.id]["debit"] + item["debit"],
                        "balance": new_accounts_data[consolidation_account.id]["balance"] + item["balance"],
                        "ending_balance": new_accounts_data[consolidation_account.id]["ending_balance"] + item["ending_balance"],
                    })

                    if foreign_currency:
                        new_accounts_data[consolidation_account.id].update({
                            "ending_currency_balance": new_accounts_data[consolidation_account.id]["ending_currency_balance"] + item["ending_currency_balance"],
                            "initial_currency_balance": new_accounts_data[consolidation_account.id]["initial_currency_balance"] + item["initial_currency_balance"],
                        })

        return new_accounts_data

    def _compute_consolidation_total_amount(self, consolidation_account_ids, data, accounts_data, total_amount):
        chart_id = data['chart_id']
        show_partner_details = data["show_partner_details"]
        foreign_currency = data["foreign_currency"]

        accounts_domain = [("chart_id", "=", chart_id)]
        if consolidation_account_ids:
            accounts_domain += [("id", "in", consolidation_account_ids)]
        consolidation_accounts = self.env["consolidation.account"].search(accounts_domain)

        new_total_amount = {}

        AccountAccount = self.env['account.account']
        for key in total_amount:
            item = total_amount[key]
            account = AccountAccount.browse(key)
            consolidation_account = account.consolidation_account_ids.filtered(lambda x: x.chart_id.id == chart_id)
            if consolidation_account and consolidation_account in consolidation_accounts:
                if not consolidation_account.id in new_total_amount:
                    new_total_amount[consolidation_account.id] = {
                        "initial_balance": 0.0,
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": 0.0,
                        "ending_balance": 0.0,
                    }

                if foreign_currency:
                    new_total_amount[consolidation_account.id].update({
                        "initial_currency_balance": 0.0,
                        "ending_currency_balance": 0.0,
                    })

                new_total_amount[consolidation_account.id].update({
                    "initial_balance": new_total_amount[consolidation_account.id]["initial_balance"] + item["initial_balance"],
                    "credit": new_total_amount[consolidation_account.id]["credit"] + item["credit"],
                    "debit": new_total_amount[consolidation_account.id]["debit"] + item["debit"],
                    "balance": new_total_amount[consolidation_account.id]["balance"] + item["balance"],
                    "ending_balance": new_total_amount[consolidation_account.id]["ending_balance"] + item["ending_balance"],
                })
                if foreign_currency:
                    new_total_amount[consolidation_account.id].update({
                        "initial_currency_balance": new_total_amount[consolidation_account.id]["initial_currency_balance"] + item["initial_currency_balance"],
                        "ending_currency_balance": new_total_amount[consolidation_account.id]["ending_currency_balance"] + item["ending_currency_balance"],
                    })

                if show_partner_details:
                    for key in item:
                        if isinstance(item[key], dict):
                            partner_item = item[key]
                            if not new_total_amount[consolidation_account.id].get(key):
                                new_total_amount[consolidation_account.id].update({
                                    key: {
                                        'credit': 0.0,
                                        'debit': 0.0,
                                        'balance': 0.0,
                                        'initial_balance': 0.0,
                                        'ending_balance': 0.0,
                                    },
                                })
                                if foreign_currency:
                                    new_total_amount[consolidation_account.id][key].update({
                                        'initial_currency_balance': 0.0,
                                        'ending_currency_balance': 0.0,
                                    })

                            new_total_amount[consolidation_account.id][key].update({
                                'credit': new_total_amount[consolidation_account.id][key]['credit'] + partner_item['credit'],
                                'debit': new_total_amount[consolidation_account.id][key]['debit'] + partner_item['debit'],
                                'balance': new_total_amount[consolidation_account.id][key]['balance'] + partner_item['balance'],
                                'initial_balance': new_total_amount[consolidation_account.id][key]['initial_balance'] + partner_item['initial_balance'],
                                'ending_balance': new_total_amount[consolidation_account.id][key]['ending_balance'] + partner_item['ending_balance'],
                            })
                            if foreign_currency:
                                new_total_amount[consolidation_account.id][key].update({
                                    'initial_currency_balance': new_total_amount[consolidation_account.id][key]['initial_currency_balance'] + partner_item['initial_currency_balance'],
                                    'ending_currency_balance': new_total_amount[consolidation_account.id][key]['ending_currency_balance'] + partner_item['ending_currency_balance'],
                                })

        if show_partner_details and foreign_currency:
            for account_id in accounts_data.keys():
                new_total_amount[account_id]["currency_id"] = accounts_data[account_id]["currency_id"]
                new_total_amount[account_id]["currency_name"] = accounts_data[account_id]["currency_name"]

        return new_total_amount

    def _compute_consolidation_trial_balance(self, data, accounts_data, total_amount):
        show_hierarchy = data["show_hierarchy"]
        foreign_currency = data["foreign_currency"]
        show_partner_details = data["show_partner_details"]

        new_trial_balance = []
        if not show_partner_details:
            for account_id in accounts_data.keys():
                accounts_data[account_id].update(
                    {
                        "initial_balance": total_amount[account_id]["initial_balance"],
                        "credit": total_amount[account_id]["credit"],
                        "debit": total_amount[account_id]["debit"],
                        "balance": total_amount[account_id]["balance"],
                        "ending_balance": total_amount[account_id]["ending_balance"],
                        "type": "account_type",
                    }
                )
                if foreign_currency:
                    accounts_data[account_id].update(
                        {
                            "ending_currency_balance": total_amount[account_id][
                                "ending_currency_balance"
                            ],
                            "initial_currency_balance": total_amount[account_id][
                                "initial_currency_balance"
                            ],
                        }
                    )
            if show_hierarchy:
                groups_data = self._get_consolidation_groups_data(
                    accounts_data, total_amount, foreign_currency
                )
                new_trial_balance = list(groups_data.values())
                new_trial_balance += list(accounts_data.values())
                new_trial_balance = sorted(new_trial_balance, key=lambda k: k["complete_code"])
                for trial in new_trial_balance:
                    counter = trial["complete_code"].count("/")
                    trial["level"] = counter
            else:
                new_trial_balance = list(accounts_data.values())
                new_trial_balance = sorted(new_trial_balance, key=lambda k: k["code"])

        return new_trial_balance

    def _get_report_values(self, docids, data):
        res = super(TrialBalanceReport, self)._get_report_values(docids, data)
        if data['schema_type'] == 'consolidation':
            res['accounts_data'] = self._compute_consolidation_accounts_data(data['consolidation_account_ids'], data, res['accounts_data'])
            res['total_amount'] = self._compute_consolidation_total_amount(data['consolidation_account_ids'], data, res['accounts_data'], res['total_amount'])
            res['trial_balance'] = self._compute_consolidation_trial_balance(data, res['accounts_data'], res['total_amount'])
        return res
