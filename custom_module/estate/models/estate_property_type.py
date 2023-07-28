from odoo import models , fields, api


class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "Estate Property Type"
	_order = "sequence"




	name = fields.Char(default = "House")
	property_ids = fields.One2many('estate.property','property_type_id')
	sequence = fields.Integer('Sequence', default=1)
	offer_ids = fields.One2many('estate.property.offer','property_type_id')
	offer_count = fields.Integer(compute = "_compute_offer_ids_count")



	@api.depends('offer_count')
	def _compute_offer_ids_count(self):
		count = 0
		for record in self:
			for rec in record.property_ids:
				count +=1
					
		self.offer_count=count


	def btn_offer_count(self):
			offers  = self.offer_ids
			return {
			'type': 'ir.actions.act_window',
			'name': 'offers',
			'view_mode': 'tree',
			'res_model': 'estate.property.offer',
			'domain': [('id','in',offers.ids)],

			}


	
		