from openerp import models, fields, api, _
from decimal import getcontext, Decimal

class product_template( models.Model ):
    _inherit = 'res.partner'

    @api.model
    def _message_count( self ):
        self.message_count = self.website_message_ids and len( self.website_message_ids ) or 0

    @api.multi
    def _get_partner_rate( self ):
        for obj in self:
            partner_rate = 0.0
            total_messages = len( [x.id for x in obj.website_message_ids if x.message_rate > 0] )
            if total_messages > 0:
                total_rate = sum( [x.message_rate for x in obj.website_message_ids] )
                getcontext().prec = 3
                # partner_rate = float(float(total_rate) / float(total_messages))
                partner_rate = Decimal( total_rate ) / Decimal( total_messages )
            obj.partner_rate = partner_rate

    partner_rate = fields.Float( compute=_get_partner_rate, store=False, string='Product Rate' )
    message_count = fields.Integer( string="Messages", compute="_message_count" )
    website_message_ids = fields.One2many( 'mail.message', 'res_id', domain=lambda self: [( 'model', '=', self._name ), ( 'type', '=', 'comment' ), ( 'website_message', '=', True )], string='Website Comments' )

    @api.multi
    def action_view_product_rating( self ):
        tree_view = self.env.ref( 'website_partner_rating.view_message_tree_for_partner_rating', False )
        form_view = self.env.ref( 'website_partner_rating.view_message_form_partner_rating', False )
        return {
            'name': _( 'Product Rating' ),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mail.message',
            'views': [( tree_view.id, 'tree' ), ( form_view.id, 'form' )],
            'view_id': tree_view.id,
            'domain': "[('id','in',[" + str( self.website_message_ids.ids ).strip( "[]" ) + "])]",
        }

