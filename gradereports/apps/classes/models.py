from django.db import models
from django.db.models import Sum
from django.utils import simplejson as json


class College(models.Model):
	name = models.CharField(max_length = 255)
	code = models.CharField(max_length = 5)
	#I wanna load in a year-by-year aggregates on their budget
	#Solution: CollegeBudget class has an annual

	#we should probably find some way 

class CollegeDetail(models.Model):
	college = models.ForeignKey(College)
	term = models.CharField(max_length=10)
	#total_budget = models.IntegerField(default = 0)
	#and so on and so forth. Scraper!
	
class Department(models.Model):
	name = models.CharField(max_length = 255)
	code = models.CharField(max_length = 5)
	college = models.ForeignKey(College)


class DepartmentDetail(models.Model):
	college = models.ForeignKey(College)
	year = models.IntegerField(default = 0)
	total_budget = models.IntegerField(default = 0)
	#and so on.

class Subject(models.Model):
	name = models.CharField(max_length = 255)
	code = models.CharField(max_length = 5)

class CourseSuper(models.Model):
	name = models.CharField(max_length=255)
	number = models.IntegerField(default = 0)
	subject = models.ForeignKey(Subject)
	description = models.TextField()

class GenEd(models.Model):
	description = models.CharField(max_length = 255)
	categoryID = models.CharField(max_length=10)
	attribute = models.CharField(max_length = 50)
	attributecode = models.CharField(max_length = 5)

class Course(models.Model):
	super_course = models.ForeignKey(CourseSuper)
	year = models.IntegerField()
	term = models.CharField(max_length=20)
	gened = models.ManyToManyField(GenEd)
	sectionDegreeAttributes = models.CharField(max_length = 100)

	#write out model methods that evaluate the stats we want on the course that semester.
	#return the aver
	def __unicode__(self):
		return self.super_course.name

	def save(self, *args, **kwargs):
		super(Course, self).save(*args, **kwargs)		


#ICES are released every semester.

class ProfSuper(models.Model):
	first_name = models.CharField(max_length =255)
	first_initial = models.CharField(max_length = 1)
	last_name = models.CharField(max_length = 255)


class CourseInstructor(models.Model):
	identity = models.ForeignKey(ProfSuper)
	year = models.IntegerField(default = 0)
	position = models.CharField(max_length = 255)
	salary = models.IntegerField(default = 0)
	
	@property
	def numberofclasses(self):
		return self.courselecture_set.count()
	#everything foreignkeys into instructors...
	#commence random fuckign stats:

class ICES(models.Model):
	instructor = models.ForeignKey(CourseInstructor)
	semester = models.CharField(max_length = 20)
	RATING_CHOICES = (
		('Excellent', 'E'),
		('Filler', 'F')
		#todo: fill these with the relevant things. Excellent.
		)
	rating_type = models.CharField(max_length = 20, choices = RATING_CHOICES)
	# there's going to have to be an easier way to accomplish this shit.

class Section(models.Model):
	#from scrape
	#see /core/management/commands/do_it.py
	course = models.ForeignKey(Course)
	sectionNumber = models.CharField(max_length = 10)
	statusCode = models.CharField(max_length = 5, blank = True, null = True)
	partOfTerm = models.CharField(max_length = 10, blank = True, null = True)
	enrollment_status = models.CharField(max_length = 30, blank = True, null = True)
	start_date = models.DateTimeField(blank = True, null = True)
	end_date = models.DateTimeField(blank = True, null = True)
	

	Aplus = models.IntegerField(default=0)
	As = models.IntegerField(default=0)
	Aminus = models.IntegerField(default=0)
	Bplus = models.IntegerField(default=0)
	B = models.IntegerField(default=0)
	Bminus = models.IntegerField(default=0)
	Cplus = models.IntegerField(default=0)
	Cs = models.IntegerField(default=0)
	Cminus = models.IntegerField(default=0)
	Dplus = models.IntegerField(default=0)
	Ds = models.IntegerField(default=0)
	Dminus = models.IntegerField(default=0)
	F = models.IntegerField(default=0)
	W = models.IntegerField(default=0)
	
	def save(self, *args, **kwargs):
		super(Section, self).save(*args, **kwargs)		

	#the bread and butter of this hurr app

class Meeting(models.Model):
	typecode = models.CharField(max_length=20)
	section = models.ForeignKey(Section)

	daysoftheweek = models.CharField(max_length=5, blank = True, null = True)

	start = models.TimeField(blank = True,  null = True)
	end = models.TimeField(blank = True, null = True)

	roomNumber = models.CharField(max_length=20)
	buildingName = models.CharField(max_length = 100, blank = True, null = True)

	instructor = models.ManyToManyField(ProfSuper)
	
	redacted = models.BooleanField(default = True)

	def save(self, *args, **kwargs):
		super(Meeting, self).save(*args, **kwargs)		


