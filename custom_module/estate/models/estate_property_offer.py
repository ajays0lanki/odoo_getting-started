from odoo import models, fields,api
from datetime import date 
from dateutil.relativedelta import relativedelta
from odoo import exceptions



class Estatepropertyoffer(models.Model):
	_name = 'estate.property.offer'
	_description = 'Estate Property offer'
	_order = "price desc"


	price = fields.Float()
	validity = fields.Integer(default = 7)
	create_date = fields.Date(default = date.today())
	date_deadline = fields.Date(compute = '_compute_date_deadline',inverse = '_inverse_deadline',copy = False)
	status = fields.Selection(selection=[('accept','Accepted'),('refuse','Refused')], copy = False)
	partner_id = fields.Many2one('res.partner',required = True)
	property_id = fields.Many2one('estate.property', required = True)
	property_type_id = fields.Many2one(related = 'property_id.property_type_id',store= True)



	@api.depends('validity')
	def _compute_date_deadline(self):
		for record in self:
			record.date_deadline = record.create_date +relativedelta(days = record.validity)




	def _inverse_deadline(self):
		for record in self:
			temp_var = record.date_deadline - record.create_date
			record.validity = temp_var.days




	def accept_btn(self):
		for record in self:
			if record.status == False:
				record.status = 'accept'
				for rec in record.property_id:
					if record.status == 'accept':
						rec.state = 'accept'
						rec.buyer_id = record.partner_id
						rec.selling_price = record.price
			

	def refuse_btn(self):
		for record in self:
			if record.status == False or record.status == 'refuse':
				record.status = 'refuse'
			


	@api.constrains('price')
	def _check_price(self):
		for record in self:
			if record.price < 0:
				raise exceptions.UserError('Price must be positive value')


	@api.model
	def create(self,vals):
		x = self.env['estate.property'].browse(vals['property_id'])
		if vals['price'] < x.best_price:
			raise exceptions.UserError('price should not be lower than existing offer')
		x.state = 'received'	
		res = super(Estatepropertyoffer,self).create(vals)
		return res
