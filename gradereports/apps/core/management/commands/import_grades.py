import csv
import os
import re

from string import split
from django.core.management.base import BaseCommand

from apps.classes.models import *
from settings.common import SITE_ROOT
from nameparser.parser import HumanName


"""
  1: Semester
  2: Year
  3: Subject
  4: Course
  5: CRN
  6: Course Title
  7: A+
  8: A
  9: A-
 10: B+
 11: B
 12: B-
 13: C+
 14: C
 15: C-
 16: D+
 17: D
 18: D-
 19: F
 20: W
 21: Primary Instructor
"""
def prof_getter(full_name, section):
	section_key = section.pk
	print section_key
	meetings = Meeting.objects.filter(section__pk = section_key)
	print meetings
	contenders = []
	for m in meetings:
		print "Something is here!"
		print m
		#instructors = m.instructor
		for i in m.instructor.all():
			print i
			contenders.append(m.i)
	print contenders
	name = HumanName(full_name)
	print name
	first_initial = name.first[0]
	print first_initial
	prof_found = False
	for p in contenders:
		if p.last_name == name.last and p.first_initial == first_initial:
			p.first_name = name.first
			p.save()
			prof_found = True
	if not prof_found:
		print "No Prof Found oh ruohruh"

class Command(BaseCommand):
	def handle(self, *args, **options):
		working_dir = os.path.join(SITE_ROOT, '../data')
		file_path = os.path.join(working_dir, 'allyears.csv')

		handle = csv.reader(open(file_path, 'rU'), delimiter=',')
		handle.next()

		for index, h in enumerate(handle):
			subject = h[2].strip()
			print subject

			subject_import, subject_created = Subject.objects.get_or_create(
				code = subject
				)
			print subject_import
			course_number = h[3].strip()
			course_title = h[5].strip()
			super_course_import, super_course_created = CourseSuper.objects.get_or_create(
				subject = subject_import,
				number = course_number,
				name = course_title
			)
			year = h[1].strip()
			semester = h[0].strip()
			term = semester + " " + year

			course_import, course_created = Course.objects.get_or_create(
				super_course = super_course_import,
				year = year,
				term = term
			)
			unparsed_name = h[20].strip()
			

			section_number = h[4].strip()
			section_import, section_created = Section.objects.get_or_create(
				course = course_import,
				sectionNumber = section_number
				)
			prof_getter(unparsed_name, section_import)

			if h[6].strip() != "N/A":
				print "here are things"
				section_import.Aplus = h[6].strip()
				section_import.As = h[7].strip()
				section_import.Aminus = h[8].strip()
				section_import.Bplus = h[9].strip()
				section_import.B = h[10].strip()
				section_import.Bminus = h[11].strip()
				section_import.Cplus = h[12].strip()
				section_import.Cs = h[13].strip()
				section_import.Cminus = h[14].strip()
				section_import.Dplus = h[15].strip()
				section_import.Ds = h[16].strip()
				section_import.Dminus = h[17].strip()
				section_import.F = h[18].strip()
				section_import.W = h[19].strip()

				section_import.save()
