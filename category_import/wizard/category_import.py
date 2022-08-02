# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.mail.wizard.mail_compose_message import _reopen
from odoo.tools.misc import get_lang

from odoo.exceptions import UserError, ValidationError
from io import StringIO
from io import BytesIO
import codecs
from collections import defaultdict
import datetime
import io

from odoo.exceptions import UserError, RedirectWarning

import xlrd

import base64

import urllib
import csv

import logging, traceback

_logger = logging.getLogger(__name__)

class CategoryImport(models.TransientModel):
    _name = 'category.import'



    file_path = fields.Char(string='File Path', attachment=False)
    xls_file = fields.Binary(attachment=True, string='XLS File')
    filename = fields.Char()

    def read_xlx_file(self):
        '''
         cursereate Temp xlx file
        '''
        if not self.xls_file:
            raise UserError(_('Error!', "Please Select a File"))
        else:
            work_book = xlrd.open_workbook(file_contents=base64.decodebytes(self.xls_file))
        return work_book

    def import_category_data(self):
        """
        Create new record of eCategory object.
        """
        _logger.info("\n Import Started.")
        try:
            work_book = self.read_xlx_file()
            categ_obj = self.env['product.public.category']
            skip = False
            for sheet in  work_book._sheet_list:
                sheet_values = sheet._cell_values
                
                for sheet_data in sheet_values[1:]:
                    print(sheet_data)
                    if not skip:
                        import_id = sheet_data[0]
                        parent_id = sheet_data[1]
                        name = sheet_data[2]
                        if name == "Fire Extinguisher Mount":
                            skip= True
                        data = {
                            'import_id': import_id,
                            'name': name,
                        }
                        # categ_parent_id = categ_obj.search([('import_id', '=' ,int(parent_id))], limit=1)
                        
                        # if categ_parent_id:
                        #     data.update({'parent_id': categ_parent_id.id})
                        cat_id = categ_obj.create(data)
                skip = False
                for sheet_data in sheet_values[1:]:
                    if not skip:
                        import_id = sheet_data[0]
                        parent_id = sheet_data[1]
                        name = sheet_data[2]
                        if name == "Fire Extinguisher Mount":
                            skip= True
                        data = {
                            'import_id': import_id,
                            'name': name,
                        }
                        categ = categ_obj.search([('import_id','=',import_id)])
                        categ_parent_id = categ_obj.search([('import_id', '=' ,int(parent_id))], limit=1)
                        if categ_parent_id:
                            categ.write({'parent_id': categ_parent_id.id})
                
            _logger.info("\nImport End. ")

        except Exception as e:
            _logger.info("Exception occurred while processing sheet: {}".format(e))

    # def _get_rows(self, attachment, attachment_name):
    #     bytes_data = base64.b64decode(attachment)
    #     if bytes_data.startswith(codecs.BOM_UTF8):
    #         string_data = bytes_data.decode('utf-8-sig')
    #     else:
    #         for encoding in ['utf-8', 'iso8859_15']:
    #             try:
    #                 string_data = bytes_data.decode(encoding)
    #                 if string_data:
    #                     break
    #             except ValueError:
    #                 pass
    #         if not string_data:
    #             raise UserError(_("Cannot determine the encoding for the attached file."))

    #     # Find the CSV dialect
    #     try:
    #         dialect = csv.Sniffer().sniff(string_data, delimiters=";|,\t")
    #     except csv.Error:
    #         raise UserError(_("Cannot determine the file format for the attached file."))

    #     rows = []
    #     try:
    #         incomplete_lines = []
    #         reader = csv.reader(io.StringIO(string_data), dialect=dialect)

    #         for line_no, record in enumerate(reader, 1):
    #             if line_no == 1:
    #                 header = [x.strip() for x in record]
    #                 while header and not header[-1]:
    #                     header.pop()
    #             else:
    #                 row = [x.strip() if isinstance(x, str) else x for x in record]
    #                 if row:
    #                     if len(row) >= len(header):
    #                         rows.append(dict(zip(header, row)))
    #                     else:
    #                         incomplete_lines.append(line_no)

    #     except csv.Error as e:
    #         raise UserError(_("Cannot read the attached file: %s", e.message))

    #     if incomplete_lines:
    #         raise UserError(_("Some lines do not have the same number of fields as the header.\n"
    #                           "Please check the following line numbers:\n"
    #                           "%s", incomplete_lines))

    #     return rows



    # def read_xlx_file(self):
    #     '''
    #      cursereate Temp xlx file
    #     '''
    #     if not self.xls_file:
    #         raise UserError(_('Error!', "Please Select a File"))
    #     else:
    #         work_book = xlrd.open_workbook(file_contents=base64.decodebytes(self.xls_file))
    #     return work_book

    # def import_category_data(self):
    #     """
    #     Create new record of eCategory object.
    #     """
    #     _logger.info("\n Import Started.")
    #     try:
    #         rows = self._get_rows(self.xls_file, self.filename)
    #         categ_obj = self.env['product.public.category']
    #         for row_data in rows:
    #             import_id = row_data.get('Cat_ID')
    #             parent_id = row_data.get('Parent_ID')
    #             name = row_data.get('Name')
    #             data = {
    #                 'import_id': int(import_id),
    #                 'name': name,
    #             }
    #             cat_id = categ_obj.create(data)
    #         for row_data in rows:
    #             import_id = row_data.get('Cat_ID')
    #             parent_id = row_data.get('Parent_ID')
    #             categ = categ_obj.search([('import_id','=',import_id)])
    #             categ_parent_id = categ_obj.search([('import_id', '=' ,int(parent_id))], limit=1)
                
    #             if categ_parent_id:
    #                 categ.write({'parent_id': categ_parent_id.id})
    #         _logger.info("\nImport End. ")

    #     except Exception as e:
    #         _logger.info("Exception occurred while processing sheet: {}".format(e))
