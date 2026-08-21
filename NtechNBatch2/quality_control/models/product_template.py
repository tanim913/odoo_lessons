from odoo import models, fields, api
import requests

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    isbn = fields.Char(string='ISBN')
    
    # Stored so we can filter by valid books
    isbn_valid = fields.Boolean(
        string='Is Valid Book?', 
        compute='_compute_isbn_valid', 
        store=True
    )
    
    book_name = fields.Char(
        string='Book Name',
        compute='_compute_isbn_valid',
        store=True
    )
    
    # # 9780451524935 — 1984, George Orwell
    # # 9780743273565 — The Great Gatsby, F. Scott Fitzgerald
    # # 9780060935467 — To Kill a Mockingbird, Harper Lee
    # # 9780062316097 — Sapiens, Yuval Noah Harari
    # # 9780141439518 — Pride and Prejudice, Jane Austen
    
    # invalid book:
    #     9780306406153
    
    def write(self, vals):
        # super() calls the original write method
        result = super(ProductTemplate, self).write(vals)
        
        # Now run our custom logic
        if 'isbn' in vals:
            print(f"ISBN was updated to {vals['isbn']}!")
            
        return result

    @api.depends('isbn')
    def _compute_isbn_valid(self):
        for record in self:
            if not record.isbn:
                record.isbn_valid = False
                continue
                
            try:
                # Call the API
                url = f"https://openlibrary.org/isbn/{record.isbn}.json"
                response = requests.get(url, timeout=5)
                # response.json()
                # If we get a 200 Success, the book exists!
                if response.status_code == 200:
                    data = response.json()
                    record.isbn_valid = True
                    record.book_name = data.get('title')
                else:
                    record.isbn_valid = False
                    record.book_name = False
                    
            except Exception as e:
                # Catch timeouts and network errors
                record.isbn_valid = False
                record.book_name = False

    def action_check_isbn(self):
        """Called by a button to force a fresh API check."""
        for record in self:
            # We clear the field, which forces the compute method to run again
            record.isbn_valid = False
            record._compute_isbn_valid()
