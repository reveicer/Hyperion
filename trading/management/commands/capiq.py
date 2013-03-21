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
title = 'mTurk Industry/Type'
template_path = PROJECT_DIR + '/../externals/templates/ProfileTemplate.xlsx' # need to change

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		gd_client = gdata.docs.service.DocsService()
		gd_client.ClientLogin(email, password, source=source)
		gs_client = gdata.spreadsheet.service.SpreadsheetsService()		
		gs_client.ClientLogin(email, password, source=source)
		query = gdata.spreadsheet.service.DocumentQuery()
		query.title = title
		feed = gs_client.GetSpreadsheetsFeed(query=query)

		if len(feed.entry) == 0:
			self.stderr.write('\'%s\' is not found...' % title)
		sdsht_entry = feed.entry[0]
		sdsht_id = self._GetID(sdsht_entry)

		# get all worksheets
		self.stdout.write('loading worksheets in %s...' % sdsht_entry.title.text)
		wksht_feed = gs_client.GetWorksheetsFeed(sdsht_id)
		self.stdout.write('...found %d worksheets in %s' % (len(wksht_feed.entry), sdsht_entry.title.text))
		for wksht_entry in wksht_feed.entry:
			self.stdout.write('handling worksheet %s...' % wksht_entry.title.text)
			wksht_id = self._GetID(wksht_entry)
			list_feed = gs_client.GetListFeed(sdsht_id, wksht_id)
			# processing lists
			for list_entry in list_feed.entry:				
				self.stdout.write('-------------')
				for key in list_entry.custom:
					self.stdout.write('%s: %s' % (key, list_entry.custom[key].text))
				self._UploadTemplate(list_entry.custom['name'].text, gd_client)


	def _GetID(self, entry):
		return entry.id.text.split('/')[-1]

	def _UploadTemplate(self, name, gd_client):
		if not os.path.isfile(template_path):
			self.stderr.write('Not a valid file.')
			return
		
		file_name = os.path.basename(template_path)
		ext = self._GetFileExtension(file_name)
		if not ext or ext not in gdata.docs.service.SUPPORTED_FILETYPES:
			self.stderr.write('File type not supported. Check the file extension.')
			return
		else:
			content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]
		try:
			ms = gdata.MediaSource(file_path=template_path, content_type=content_type)
		except IOError:
			self.stderr.write('Problems reading file. Check permissions.')
			return

		entry = gd_client.Upload(ms, name)
		if entry:
			self.stdout.write('Spreadsheet \'%s\'. Upload successful!' % name)
		else:
			self.stderr.write('Spreadsheet \'%s\'. Upload error.' % name)

	def _GetFileExtension(self, file_name):
		match = re.search('.*\.([a-zA-Z]{3,}$)', file_name)
		if match:
			return match.group(1).upper()
		return False