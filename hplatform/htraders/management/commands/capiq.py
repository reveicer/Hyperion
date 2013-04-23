from django.core.management.base import BaseCommand, CommandError
import gdata.docs.client
import gdata.docs.data
import gdata.docs.service
import gdata.spreadsheet.service
import os.path, re, sys, string
from optparse import make_option

class Command(BaseCommand):
	
	option_list = BaseCommand.option_list + (
            make_option('--u',
                        type=str,
                        help="username"
            ),
            make_option('--p',
                        type=str,
                        help='password'
            ),
            make_option('--s',
                        type=str,
                        default='hyperion.capiq',
                        help='APP_NAME'
            ),
            make_option('--source',
                        type=str,
                        help='capiq source file'
            ),
            make_option('--output',
                        type=str,
                        help='output folder'
            ),
            make_option('--template',
                        type=str,
                        default=os.path.dirname(__file__) + '/excel_templates/ProfileTemplate.xlsx',
                        help='profile template directory'
            )
        )

	def handle(self, *args, **options):
		if options['u'] is None or options['p'] is None or options['source'] is None or options['output'] is None:
			self.stderr.write('Usage: python manage.py capiq --u [your username] --p [your password] --source [CapIQ file] --output [Output Folder (must not exist)]')
			self.stderr.write('Example: python manage.py capiq --u hzhong62@gmail.com --p hzhong0625 --source \'mTurk Industry/Type\' --output output')
			return
		if self._VerifyTemplateMediaSource(options['template']) is False:
			self.stderr.write('...Quiting')
			return

		gl_client = gdata.docs.client.DocsClient()
		gl_client.ClientLogin(options['u'], options['p'], source=options['s'])
		gs_client = gdata.spreadsheet.service.SpreadsheetsService()		
		gs_client.ClientLogin(options['u'], options['p'], source=options['s'])

		self.stdout.write('> Locating spreadsheet: %s...' % options['source'])
		sdsht_entry = self._GetSpreadsheet(gs_client, options['source'])
		if sdsht_entry:
			self.stdout.write('> ...Successful')
		else:
			self.stderr.write('...Quiting')		
		
		wksht_feed = gs_client.GetWorksheetsFeed(self._GetEntryID(sdsht_entry))
		if len(wksht_feed.entry) > 0:
			col = gdata.docs.data.Resource(type='folder', title=options['output'])
  			col = gl_client.CreateResource(col)
  			if col:
				self.stdout.write('> Creating Folder: %s... Successful' % options['output'])
			else:
				self.stderr.write('Failed to create Folder: %s... Quiting' % options['output'])
				return
		else:
			self.stderr.write('Failed to find worksheet in %s... Quiting' % options['source'])
			return

		for wksht_entry in wksht_feed.entry:
			list_feed = gs_client.GetListFeed(self._GetEntryID(sdsht_entry), self._GetEntryID(wksht_entry))
			self.stdout.write('> Processing %d company profiles from worksheet: %s...' % (len(list_feed.entry), wksht_entry.title.text))
			for list_entry in list_feed.entry:
				company_name = list_entry.custom['name'].text
				company_website = list_entry.custom['website'].text
				company_description = list_entry.custom['description'].text
				raw_address = list_entry.custom['address'].text
				company_contact_book = self._ParseRawAddress(raw_address)

				#if self._UploadTemplate(gl_client, col, company_name):
				profile_sdsht_resource_id = self._UploadTemplate(gl_client, col, company_name, options['template'])
				#self.stderr.write('upload resource id: %s' % profile_sdsht_resource_id)
				if profile_sdsht_resource_id:
					profile_sdsht_entry = self._GetSpreadsheet(gs_client, company_name)
					#self.stderr.write('real doc id: %s' % self._GetEntryID(profile_sdsht_entry))
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


	# Handle multiple file
	def _GetSpreadsheet(self, gs_client, spreadsheet_title, resource_id=None):
		query = gdata.spreadsheet.service.DocumentQuery()
		query.title = spreadsheet_title.encode('utf8') 
		query.title_exact = 'True'
		if resource_id is not None:
			print resource_id
			query.resource_id = resource_id
		sdsht_feed = gs_client.GetSpreadsheetsFeed(query=query)
		if len(sdsht_feed.entry) == 0:
			self.stderr.write('> Failed to locate spreadsheet: %s...' % spreadsheet_title)
			return False
		else:
			sdsht_entry = sdsht_feed.entry[0]
			#self.stderr.write('find resource id: %s' % sdsht_entry.ResourceId())
			return sdsht_entry

	def _GetWorksheet(self, gs_client, sdsht_entry, worksheet_title):
		query = gdata.spreadsheet.service.DocumentQuery()
		query.title = worksheet_title
		query.title_exact = 'True'
		wksht_feed = gs_client.GetWorksheetsFeed(self._GetEntryID(sdsht_entry), query=query)
		if len(wksht_feed.entry) == 0:
			self.stderr.write('Error: cannot find worksheet %s.' % worksheet_title)
			return False
		return wksht_feed.entry[0]

	def _VerifyTemplateMediaSource(self, template):
		if not os.path.isfile(template):
			self.stderr.write('Template Error: Not a valid file.')
			return False
		
		file_name = os.path.basename(template)
		ext = self._GetFileExtension(file_name)
		if not ext or ext not in gdata.docs.service.SUPPORTED_FILETYPES:
			self.stderr.write('Template Error: File type not supported. Check the file extension.')
			return False
		if ext not in ['XLS', 'XLSX']:
			self.stderr.write('Template Error: Please choose a spreadsheet template, i.e. XLS or XLSX.')
			return False
		else:
			return True

	# TODO return upload_sdsht
	def _UploadTemplate(self, gl_client, col, name, template):
		file_name = os.path.basename(template)
		ext = self._GetFileExtension(file_name)
		content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]
		try:
			ms = gdata.MediaSource(file_path=template, content_type=content_type)
			sdsht = gdata.docs.data.Resource(type='spreadsheet', title=name.encode('utf8'))
			upload_sdsht = gl_client.CreateResource(sdsht, collection=col, media=ms)
			if upload_sdsht:
				self.stdout.write('> Generating spreadsheet: %s... Successful' % name)
				return upload_sdsht.resource_id
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
		if raw_address is None:
			return contact_book
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