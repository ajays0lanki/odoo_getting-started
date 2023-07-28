from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import exceptions

class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "Estate Property "
	_order = "id desc"


	name =fields.Char(default = "My New House",required = True)
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date(default = lambda self : date.today()+relativedelta(months=3),copy = False)
	selling_price = fields.Float(readonly = True, copy = False)
	expected_price = fields.Float(required = True)
	bedrooms = fields.Integer(default = 2)
	living_area = fields.Integer()
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection(selection = [('north','North'),('south','South'),('east','East'),('west','West')],string = "Garden Orientation")
	active = fields.Boolean(default = True)
	state = fields.Selection(selection = [('new','New'),('received','Offer Received'),('accept','Offer Accepted'),('sold','Sold'),('cancel','Canceled')], string = "Status")
	property_type_id = fields.Many2one('estate.property.type', string = "Property Types")
	buyer_id = fields.Many2one('res.partner',string = "Buyers", copy = False)
	salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
	tag_ids = fields.Many2many('estate.property.tag', string = "Name")
	offer_ids = fields.One2many('estate.property.offer','property_id')
	total_area = fields.Integer(compute = '_compute_total')
	best_price = fields.Float(compute = '_compute_best_price')




	# _sql_constraints = [('check_expected_price','CHECK(expected_price >= 0)','must be positive value'),('check_selling_price,', 'CHECK(selling_price >= 0 )','must be positive value'),]
	# _sql_constraints = [('check_expected_price,', 'CHECK(expected_price >= 0 )','must be positive value'), ('check_selling_price,', 'CHECK(selling_price >= 0 )','must be positive value'),]



	@api.depends('garden_area')
	def _compute_total(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area


	@api.depends('offer_ids.price')
	def _compute_best_price(self):
		for record in self:
			record.best_price= max(record.offer_ids.mapped('price'),default= 0)




	@api.onchange('garden')
	def _onchange_garden_area(self):
		for record in self:
			if self.garden == True:
				self.garden_area = 10
				self.garden_orientation = 'north'
			else :
				self.garden_area = 0
				self.garden_orientation = ''

	def sold_property(self):
		for record in self:
			if record.state == False or record.state == 'new' or record.state == 'received' or record.state == 'accept'or record.state == 'sold':
				record.state = 'sold'
			else:
				raise exceptions.UserError('Cancel property can not be sold')

	def cancel_property(self):
		for record in self:
			if record.state == False or record.state == 'new' or record.state == 'received' or record.state == 'accept'or record.state == 'cancel':
				record.state = 'cancel'
			else:
				raise exceptions.UserError('Sold property can not be cancel')			


	@api.constrains('expected_price')
	def _check_price(self):
		for record in self:
			if record.expected_price < 0:
				raise exceptions.UserError('Expected price must be positive value')

	@api.constrains('selling_price')
	def _check_selling_price(self):
		for record in self:
			if record.selling_price < (record.expected_price*90/100):
				raise exceptions.UserError('selling price cannot be lower than 90% of the expected price.')

	@api.ondelete(at_uninstall=False)
	def _unlink_state(self):
		for record in self:
			if record.state != 'new' or record.state != 'cancel':
				raise exceptions.UserError('You can not delete that not new and cancel property')



