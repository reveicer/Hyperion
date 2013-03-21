from django.core.management.base import BaseCommand, CommandError
import trading.models
import gdata.spreadsheet.service

email = 'hzhong62@gmail.com'
password = 'hzhong0625'
title = 'mTurk Industry/Type'


class Command(BaseCommand):
	
	def handle(self, *args, **options):
		gd_client = gdata.spreadsheet.service.SpreadsheetsService()		
		gd_client.ClientLogin(email, password)

		query = gdata.spreadsheet.service.DocumentQuery()
		query.title = title
		feed = gd_client.GetSpreadsheetsFeed(query=query)

		if len(feed.entry) != 0:
			self.stdout.write('\'%s\' is not found...' % title)
		sdsht_entry = feed.entry[0]
		sdsht_id = self.get_id(sdsht_entry)

		# get all worksheets
		self.stdout.write('loading worksheets in %s...' % sdsht_entry.title.text)
		wksht_feed = gd_client.GetWorksheetsFeed(sdsht_id)
		self.stdout.write('...found %d worksheets in %s' % (len(wksht_feed.entry), sdsht_entry.title.text))
		for wksht_entry in wksht_feed.entry:
			self.stdout.write('handling worksheet %s...' % wksht_entry.title.text)
			wksht_id = self.get_id(wksht_entry)
			list_feed = gd_client.GetListFeed(sdsht_id, wksht_id)
			# processing lists
			for list_entry in list_feed.entry:
				print '-------------'
				for key in list_entry.custom:
					print '%s: %s' % (key, list_entry.custom[key].text)

	def get_id(self, entry):
		return entry.id.text.split('/')[-1]