import json
import os
import re
import requests

from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import date, datetime


class ClasschartsHomework:
    def __init__(self, classcharts_dict):
        self.raw = classcharts_dict
        self._parse_classcharts_dict()
        
    def _parse_classcharts_dict(self):
        self.lesson = self.raw['lesson']['subject']['name']
        self.title = self.raw['title']
        self.student = '{} {}'.format(
            self.raw['pupil_homework']['lesson_pupil']['pupil']['first_name'],
            self.raw['pupil_homework']['lesson_pupil']['pupil']['last_name']
        )
        self.ticked = self.raw['pupil_homework']['ticked'] == 'yes'
        
        self.due_date = self._parse_due_date()
        self.completion_time_minutes = self._parse_completion_time()
        self.description = self._parse_description()
        
    def _parse_completion_time(self):
        time_unit = self.raw['completion_time_unit']

        if time_unit not in ('minutes', 'hours'):
            raise ValueError('Cannot parse time unit: {}'.format(time_unit))
        
        completion_time_value = self.raw['completion_time_value']

        if not completion_time_value:
            return 0

        # Times can be expressed as 30+ to indicate greater than 30 minutes
        if completion_time_value[-1] == '+':
            completion_time_value = completion_time_value[:-1]
            scale = 1.5
        else:
            scale = 1
        completion_time_value = float(completion_time_value) * scale
        if time_unit == 'hours':
            completion_time_value *= 60
        return int(completion_time_value)
            
    def _parse_due_date(self):
        due_date = self.raw['due_date']
        if not due_date:
            return None
        
        return datetime.strptime(due_date[:10], '%Y-%m-%d').date()
    
    def _parse_description(self):
        soup = BeautifulSoup(self.raw['description'], 'html.parser')
        return soup.text.strip()
       
    @property
    def done(self):
        """This definition may change."""
        return self.ticked
    
    @property
    def _key(self):
        return (
            self.lesson,
            self.title,
            self.student,
            self.ticked,
            self.completion_time_minutes,
            self.due_date
        )
    
    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self._key == other._key
    
    def __repr__(self):
        return "<{} {} Homework ({}): {}, Due: {}, Time: {} mins>".format(
            self.student,
            self.lesson,
            'DONE' if self.done else 'TODO',
            self.title,
            self.due_date,
            self.completion_time_minutes
        )


class ClasschartsClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.cookies = None
        self.csrf_token = None
        
    def query_due_range(self, from_date, to_date):
        if not self.cookies:
            self._set_cookies()
        
        if not self.csrf_token:
            self._set_csrf_token()
            
        homework_url = 'https://www.classcharts.com/parent/homeworkcalendar'
        homework_payload = {
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'homework_display_date': 'due_date',
            'csrf': self.csrf_token
        }
    
        req = requests.post(
            homework_url,
            cookies=self.cookies,
            data=homework_payload
        )
        
        homework_items = json.loads(req.text)['data']
        
        return [ClasschartsHomework(homework) for homework in homework_items]


    def _set_cookies(self):
        login_url = 'https://www.classcharts.com/parent/login'
        login_payload = {
            '_method': 'POST',
            'email': self.username,
            'logintype': 'existing',
            'password': self.password,
            'login': 'Log In',
        }

        req = requests.post(
            login_url,
            data=login_payload,
            allow_redirects=False
        )

        self.cookies = req.cookies

    def _set_csrf_token(self):
        csrf_re = re.compile(r".*csrf_session = '([0-9a-f]+)'.*")

        csrf_url = 'https://www.classcharts.com/parent/homework'
        csrf_req = requests.get(csrf_url, cookies=self.cookies)

        # CSRF token is in javascript in the header
        soup = BeautifulSoup(csrf_req.text, 'html.parser')
        header_js = soup.head.script.text.replace('\n', ',')

        match = csrf_re.match(header_js)
        if not match:
            raise ValueError('Cannot find CSRF token in {}'.format(header_js))

        self.csrf_token = match.groups()[0]
     