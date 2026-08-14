from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QualityCheckLine(models.Model):
    _name = "quality.check.line"
    _description = "Quality Control Check Line"

    product_id = fields.Many2one('product.product', 'Product', required=True)
    rec_qty = fields.Float('Receive Qty', required=True, default=0.0)
    damage_qty = fields.Float('Damage Qty', required=True, default=0.0)
    remain_qty = fields.Float('Remain Qty', compute='_compute_remain_qty', store=True)
    line_id = fields.Many2one('quality.check', 'Line', required=True)

    @api.depends('rec_qty', 'damage_qty')
    def _compute_remain_qty(self):
        for line in self:
            line.remain_qty = line.rec_qty - line.damage_qty

    @api.onchange('damage_qty', 'rec_qty')
    def _onchange_damage_qty(self):
        if self.damage_qty > self.rec_qty:
            return {
                'warning': {
                    'title': 'Invalid Damage Quantity',
                    'message': 'Damage quantity cannot exceed receive quantity.'
                }
            }