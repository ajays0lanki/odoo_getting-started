from odoo import models, fields, api


class EstatePropertyTag(models.Model):
	_name = "estate.property.tag"
	_description = "Estate Property Tag"
	_order = "name"



	name = fields.Char(required = True)
	color = fields.Integer()
	