# -*- coding: utf-8 -*-
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_quality_check(self):
        for picking in self:
            msg = f"Quality Check clicked for picking: {picking.name}"
            print(msg, flush=True)
            _logger.info(msg)
        return True
