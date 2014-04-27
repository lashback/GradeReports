#!/usr/bin/env python
import requests
from BeautifulSoup import BeautifulStoneSoup
from apps.classes.models import *
from django.core.management.base import BaseCommand
import os
import re
from time import strptime, strftime
import time
import datetime
import thread
#from threading import thread
from thready import threaded
import urllib2
class Command(BaseCommand):
	def handle(self, *args, **options): 
		url = 'http://courses.illinois.edu/cisapp/explorer/schedule.xml'
		r = requests.get(url)
		soup = BeautifulStoneSoup(r.text)

		label = soup.find('ns2:schedule').find('label').text

		year_list = soup.find('ns2:schedule').find('calendaryears').findAll('calendaryear')

		def start_subject_threads(subject_list, year_label,term_label):
			#subject_list = subject_list[134:]
			#print subject_list
			print term_label
			if term_label != "Spring 2013":
				for subject in subject_list:
					get_subject_data(subject, year_label, term_label)

		def get_subject_data(subject, year_label, term_label):
			##for testing only because I am lazy and this takes waaay too fucking long. use this to, you know, do things. 
			#if subject.text != "Committee on Inst Cooperation":
			#	pass
			#else:
		#		print subject
				subject_url = subject['href']
				subject_id = subject['id']
				subject_label = subject.text
				print subject_label
		#		print subject_url
				r4 = requests.get(subject_url)																									#REBUILD
				#r4 = urllib2.urlopen(subject_url)

		#		print r4
				if r4.status_code == 200:
					soup4 = BeautifulStoneSoup(r4.text)
		#			print soup4
					if soup4.find('ns2:subject') is not None:
						course_list = soup4.find('ns2:subject').find('courses').findAll('course')
					else:
						course_list = None
					print "Evaluating %s courses" % len(course_list)
					for course in course_list:
						course_url = course['href']
						course_id = course['id']
						course_label = course.text
					#	print course_label
					#	print course_url
						r5 = requests.get(course_url)																								#REBUILD
						#r5 = urllib2.urlopen(course_url)
						if r5.status_code == 200:
							soup5 = BeautifulStoneSoup(r5.text)
							
							subject_import, subject_created = Subject.objects.get_or_create(
								name = subject_label,
								code = subject_id
								)
							if soup5.find('ns2:course').find('description') is not None:
								course_description = soup5.find('ns2:course').find('description').text
							else:
								course_description = None

							if soup5.find('ns2:course').find('sectiondegreeattributes') is not None:
								degreeattributes = soup5.find('ns2:course').find('sectiondegreeattributes').text
							else:
								degreeattributes = None
							
							print course_description
							course_super_import, course_super_created = CourseSuper.objects.get_or_create(
								subject = subject_import,
								name = course_label,
								number =course_id,
							)

							course_import, course_created = Course.objects.get_or_create(
								super_course = course_super_import,
								year = year_label,
								term = term_label,
								sectionDegreeAttributes = degreeattributes,
								description = course_description,

								)
							if soup5.find('ns2:course').find('genedcategories') is not None:
								geneds = soup5.find('ns2:course').find('genedcategories').findAll('category')
								for gened in geneds:
									print gened('description')[0].text				
									
									attributecode =  gened('ns2:genedattributes')[0].find('genedattribute')['code']
									attribute = gened('ns2:genedattributes')[0].find('genedattribute').text
									
									gened_import, gened_created = GenEd.objects.get_or_create(
										description = gened('description')[0].text,
										categoryID = gened['id'],
										attribute = attribute,
										attributecode = attributecode
										)
									course_import.gened.add(gened_import)
									course_import.save()


							section_list = soup5.find('ns2:course').find('sections').findAll('section')
							for section in section_list:
								section_url = section['href']
								section_crn = section['id']
								section_label = section.text
								print section_label
								print section_url
								r6 = requests.get(section_url)																							#REBUILD
								#r6 = urllib2.urlopen(section_url)
								if r6.status_code == 200:
									soup6 = BeautifulStoneSoup(r6.text)
									#some OCE courses don't have terms like WHAAAT
									if soup6.find('ns2:section').find('partofterm') is not None:
										partOfTerm = soup6.find('ns2:section').find('partofterm').text
										dirty_startdate = soup6.find('ns2:section').find('startdate').text
										dirty_enddate = soup6.find('ns2:section').find('enddate').text
										
										startdate = datetime.datetime.strptime(dirty_startdate,'%Y-%m-%d-%H:%M')
										enddate = datetime.datetime.strptime(dirty_enddate,'%Y-%m-%d-%H:%M')

									else:
										partOfTerm = None
										startdate = None
										enddate = None

								#	print partOfTerm


									section_import, section_created = Section.objects.get_or_create(
											course = course_import,
											sectionNumber = section_crn,
											partOfTerm = partOfTerm,
											start_date = startdate,
											end_date = enddate,						
										)

									meetings_list = soup6.find('ns2:section').find('meetings').findAll('meeting')
									
									for meeting in meetings_list:
									
										#individual imports for different kinds of classes. If someone knows of a better way to grab this let me know.
										if meeting.find('type').text == 'Independent Study':
											meeting_import, meeting_made = Meeting.objects.get_or_create(
												typecode = meeting.find('type').text,
												section = section_import
												)

										#some arranged courses are weird.
										elif meeting('start')[0].text == 'ARRANGED':
										#	print "\n\n\n\n Arranged course \n\n\n\n"
											meeting_import, meeting_made = Meeting.objects.get_or_create(
												typecode = meeting.find('type').text,
												section = section_import,
												start = None
												)
										
										elif meeting.find('daysoftheweek') is None:

											meeting_import, meeting_made = Meeting.objects.get_or_create(
												typecode = meeting.find('type').text,
												section = section_import,
												start = meeting('start')[0].text,
												end = meeting('end')[0].text,
												#this "Null" is my solution to the stupid meeting section problem. A merge of the two meetings would be preferable.
												#in re: http://courses.illinois.edu/cisapp/explorer/schedule/2014/spring/CHEM/492/58422.xml
												#returns two objects because DUH.
												#daysoftheweek = "Null"
												)

										#some seminars don't have meeting places
										elif meeting.find('buildingname') is None or meeting.find('roomnumber') is None:
										#	"\n\n\n\n NO LOCATION FOOOL! \n\n\n\n"
											meeting_import, meeting_made = Meeting.objects.get_or_create(
												typecode = meeting.find('type').text,
												section = section_import,
												start = meeting('start')[0].text,
												end = meeting('end')[0].text,
												daysoftheweek = meeting('daysoftheweek')[0].text
												)

										else:
											meeting_import, meeting_made = Meeting.objects.get_or_create(
												typecode = meeting.find('type').text,
												section = section_import,
												start = meeting('start')[0].text,
												end = meeting('end')[0].text,
												daysoftheweek = meeting('daysoftheweek')[0].text,
												roomNumber = meeting('roomnumber')[0].text,
												buildingName = meeting('buildingname')[0].text
												)

										instructors = meeting.find('instructors').findAll()
									#	print instructors
										for instructor in instructors:
											prof_super_import, prof_super_created = ProfSuper.objects.get_or_create(
												first_initial = instructor['firstname'],
												last_name = instructor['lastname']
												)
											meeting_import.instructor.add(prof_super_import)
											meeting_import.save()

		def get_this_party_started(year):
			year_url = year['href']
			year_label = year['id']
			r2 = requests.get(year_url)
			soup2 = BeautifulStoneSoup(r2.text)
			soup2.find('ns2:calendaryear')
			print year_label
			term_list = soup2.find('ns2:calendaryear').find('terms').findAll('term')
			
			for term in term_list:
				term_url = term['href']
				term_id = term['id']
				term_label = term.text
				print term_label
				
				r3 = requests.get(term_url)
				soup3 = BeautifulStoneSoup(r3.text)
				subject_list = soup3.find('ns2:term').find('subjects').findAll('subject')
				
				start_subject_threads(subject_list, year_label, term_label)

		#threaded(year_list, get_this_party_started, num_threads =10)
		
		for year in year_list:
#			try:
#				thread.start_new_thread(get_this_party_started, (year,))	
#			except Exception:
#				import traceback; traceback.print_exc();
			if int(year.text) < 2014:
				get_this_party_started(year)
