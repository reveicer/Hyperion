from django.core.management.base import BaseCommand, CommandError
from hyperion_site.settings import PROJECT_DIR
import gdata.docs.service
import gdata.spreadsheet.service
import os.path
import re

import sys
import getopt
import getpass

source = 'hyperion.capiq'
email = 'hzhong62@gmail.com'
password = 'hzhong0625'
mTurk_file_title = 'mTurk Industry/Type'
template_path = PROJECT_DIR + '/../externals/templates/ProfileTemplate.xlsx'

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		if self._VerifyTemplateMediaSource() is False:
			self.stderr.write('Fatal: Exiting due to Template Error.')
			return

		gd_client = gdata.docs.service.DocsService()
		gd_client.ClientLogin(email, password, source=source)
		gs_client = gdata.spreadsheet.service.SpreadsheetsService()		
		gs_client.ClientLogin(email, password, source=source)

		sdsht_entry = self._GetSpreadsheet(gs_client, mTurk_file_title)
		wksht_feed = gs_client.GetWorksheetsFeed(self._GetEntryID(sdsht_entry))
		
		for wksht_entry in wksht_feed.entry:
			list_feed = gs_client.GetListFeed(self._GetEntryID(sdsht_entry), self._GetEntryID(wksht_entry))
			self.stdout.write('> Processing %d company profiles from %s/%s...' % (len(list_feed.entry), sdsht_entry.title.text, wksht_entry.title.text))
			for list_entry in list_feed.entry:
				company_name = list_entry.custom['name'].text
				company_website = list_entry.custom['website'].text
				company_description = list_entry.custom['description'].text
				raw_address = list_entry.custom['address'].text
				company_contact_book = self._ParseRawAddress(raw_address)

				if self._UploadTemplate(gd_client, company_name) is True:
					profile_sdsht_entry = self._GetSpreadsheet(gs_client, company_name)
					profile_wksht_id = 'od6'
					company_name_cell = gs_client.UpdateCell(row='7', col='2', inputValue=company_name, key=self._GetEntryID(profile_sdsht_entry), wksht_id=profile_wksht_id)
					company_website_cell = gs_client.UpdateCell(row='8', col='2', inputValue=company_website, key=self._GetEntryID(profile_sdsht_entry), wksht_id=profile_wksht_id)
					company_description_cell = gs_client.UpdateCell(row='17', col='2', inputValue=company_description, key=self._GetEntryID(profile_sdsht_entry), wksht_id=profile_wksht_id)
					if company_contact_book.has_key('address'):
						company_address_cell = gs_client.UpdateCell(row='9', col='2', inputValue=company_contact_book['address'], key=self._GetEntryID(profile_sdsht_entry), wksht_id=profile_wksht_id)
					if company_contact_book.has_key('phones'):
						company_phones_cell = gs_client.UpdateCell(row='10', col='2', inputValue=company_contact_book['phones'], key=self._GetEntryID(profile_sdsht_entry), wksht_id=profile_wksht_id)
					if company_contact_book.has_key('faxes'):
						company_faxes_cell = gs_client.UpdateCell(row='11', col='2', inputValue=company_contact_book['faxes'], key=self._GetEntryID(profile_sdsht_entry), wksht_id=profile_wksht_id)


	def _GetSpreadsheet(self, gs_client, spreadsheet_title):
		query = gdata.spreadsheet.service.DocumentQuery()
		query.title = spreadsheet_title
		query.title_exact = 'True'
		sdsht_feed = gs_client.GetSpreadsheetsFeed(query=query)
		if len(sdsht_feed.entry) == 0:
			self.stderr.write('Error: cannot find spreadsheet %s.' % spreadsheet_title)
			return False
		return sdsht_feed.entry[0]

	def _GetWorksheet(self, gs_client, sdsht_entry, worksheet_title):
		query = gdata.spreadsheet.service.DocumentQuery()
		query.title = worksheet_title
		query.title_exact = 'True'
		wksht_feed = gs_client.GetWorksheetsFeed(self._GetEntryID(sdsht_entry), query=query)
		if len(wksht_feed.entry) == 0:
			self.stderr.write('Error: cannot find worksheet %s.' % worksheet_title)
			return False
		return wksht_feed.entry[0]

	def _VerifyTemplateMediaSource(self):
		if not os.path.isfile(template_path):
			self.stderr.write('Template Error: Not a valid file.')
			return False
		
		file_name = os.path.basename(template_path)
		ext = self._GetFileExtension(file_name)
		if not ext or ext not in gdata.docs.service.SUPPORTED_FILETYPES:
			self.stderr.write('Template Error: File type not supported. Check the file extension.')
			return False
		if ext not in ['XLS', 'XLSX']:
			self.stderr.write('Template Error: Please choose a spreadsheet template, i.e. XLS or XLSX.')
			return False
		else:
			return True

	def _UploadTemplate(self, gd_client, name):
		file_name = os.path.basename(template_path)
		ext = self._GetFileExtension(file_name)
		content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]
		try:
			ms = gdata.MediaSource(file_path=template_path, content_type=content_type)
			entry = gd_client.Upload(ms, name)
			if entry:
				self.stdout.write('Upload Success: spreadsheet \'%s\'' % name)
				return True
			else:
				self.stderr.write('Upload Error: spreadsheet \'%s\'' % name)
				return False
		except IOError:
			self.stderr.write('Upload Error: Problems reading template. Check permissions.')
			return False		

	def _ParseRawAddress(self, raw_address):
		contact_book = {}
		address = None
		phones = None
		faxes = None
		lines = raw_address.split('\n')
		for line in lines:			
			if 'Phone' in line:
				phone = self._GetContactNumber(line)
				if phone is not False:
					if phones is None:
						phones = phone
					else:
						phones += ('\n' + phone)
			elif 'Fax' in line:
				fax = self._GetContactNumber(line)
				if fax is not False:
					if faxes is None:
						faxes = fax
					else:
						faxes += ('\n' + fax)
			elif line != 'Headquarters':
				if address is None:
					address = line
				else:
					address += ('\n' + line)

		if address is not None:
			contact_book['address'] = address
		if phones is not None:
			contact_book['phones'] = phones
		if faxes is not None:
			contact_book['faxes'] = faxes

		return contact_book

	def _GetContactNumber(self, line):
		if ':' not in line:
			self.stderr.write('Parse Error: %s has undesired format...' % line)
			return false
		return line[line.find(':')+1:]

	def _GetFileExtension(self, file_name):
		match = re.search('.*\.([a-zA-Z]{3,}$)', file_name)
		if match:
			return match.group(1).upper()
		return False

	def _GetEntryID(self, entry):
		return entry.id.text.split('/')[-1]