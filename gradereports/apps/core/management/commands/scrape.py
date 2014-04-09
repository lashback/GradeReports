from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulStoneSoup as Soup
import requests
import lxml
from lxml import etree
from StringIO import StringIO

from apps.classes.models import *


class Command(BaseCommand):
	def handle(self, *args, **options):
		base_url = "http://courses.illinois.edu/cisapp/explorer/schedule.xml"

		r = requests.get(base_url)
		
		xmlz = r.content
		stringthing = str(xmlz)
		self.stdout.write(stringthing)
#		root = etree.tostring(xmlz, encoding=unicode)
		root = etree.tostring(r, encoding='UTF-8', xml_declaration=True)
#		utf8_parser = etree.XMLParser(encoding='utf-8')
#		def parse_from_unicode(unicode_str):
#		    s = unicode_str.encode('utf-8')
 #   		return etree.fromstring(s, parser=utf8_parser)

#		toparse = parse_from_unicode(stringthing)
#		tosoup = etree.tostring(toparse)
		soup = Soup(root, "lxml")
		print soup
#		parser = etree.XMLParser(ns_clean=True)

#		tree = etree.parse(StringIO(xml), parser)
#		stringtest = etree.tostring(tree.getroot())


		#self.stdout(stringtest)

#		root = etree.fromstring(xml)

#	soup = BeautifulSoup(root, 'lxml')

#		self.stdout.write(soup)
		
		