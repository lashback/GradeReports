#!/usr/bin/env python
import requests
from BeautifulSoup import BeautifulStoneSoup
from apps.classes.models import *
from django.core.management.base import BaseCommand
import os
import re


url = 'http://courses.illinois.edu/cisapp/explorer/schedule.xml'
r = requests.get(url)
soup = BeautifulStoneSoup(r.text)

label = soup.find('ns2:schedule').find('label').text

year_list = soup.find('ns2:schedule').find('calendaryears').findAll('calendaryear')

for year in year_list:
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
        for subject in subject_list:
            subject_url = subject['href']
            subject_id = subject['id']
            subject_label = subject.text
            print subject_label
            r4 = requests.get(subject_url)
            soup4 = BeautifulStoneSoup(r4.text)
            course_list = soup4.find('ns2:subject').find('courses').findAll('course')
            for course in course_list:
                course_url = course['href']
                course_id = course['id']
                course_label = course.text
                print course_label
                r5 = requests.get(course_url)
                soup5 = BeautifulStoneSoup(r5.text)
                section_list = soup5.find('ns2:course').find('sections').findAll('section')
                for section in section_list:
                    section_url = section['href']
                    section_crn = section['id']
                    section_label = section.text
                    print section_label
                    print section_url
                    r6 = requests.get(section_url)
                    soup6 = BeautifulStoneSoup(r6.text)
                    meetings_list = soup6.find('ns2:section').find('meetings').findAll('meeting')
                    for meeting in meetings_list:
                        meeting_scrape, meeting_made = Meeting.objects.get_or_create(
                            typecode = meeting.find('type').text,
                            #start = meeting['start'].text,
                            #end = meeting['end'].text,
                            #daysoftheweek = meeting['daysoftheweek'].text,
                            #roomNumber = meeting['roomNumber'].text,
                            #buildingName = meeting['buildingName'].text
                            )