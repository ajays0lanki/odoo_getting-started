from odoo import models,fields, Command



class EstatePropertyAccount(models.Model):
	_inherit = "estate.property"




	def sold_property(self):
		res= super(EstatePropertyAccount,self).sold_property()
		self.env['account.move'].create(
	        {
	            "partner_id": self.buyer_id.id,
	            "move_type" : "out_invoice",
	            "invoice_line_ids": [
	                Command.create({
	                    "name": self.name,
	                    "quantity": 1,
	                    "price_unit": (self.selling_price*0.06)+100,

	                }),

	               
	            ],
	        }
	    )


		return res
