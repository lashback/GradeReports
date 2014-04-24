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
def prof_getter(full_name, course):
	contenders = 
	name = HumanName(full_name)






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

			course_number = 
			course_title = h[5]
			super_course_import, super_course_created = CourseSuper.objects.get_or_create(
				
			)
#		course_import, course_created = Course.objects.get_or_create(
#
#		)
		#This is harder. Actual scripting neccesary. 

			unparsed_name = h[20].strip()
			name = HumanName(unparsed_name)
			print "%s %s" % (name.first, name.last)
#
#		course_instructor_import, couse_instructor_created = Course.objects.get_or_create(
#        )