from django.test import TestCase
from customer.models import *
from .models import *
from django.contrib.auth.models import User

# Create your tests here.

class TicketTypeTestClass(TestCase):
    #setup method
    def setUp(self):
        self.elec=TicketType(name='Electricity',priority=1)

    def test_instance(self):
        self.assertTrue(isinstance(self.elec,TicketType)) 

    def test_save_method(self):
        self.elec.save()
        ticketypes=TicketType.objects.all()
        self.assertTrue(len(ticketypes) > 0)

    def test_save_multiple_tickettypes(self):
        self.elec.save()

        self.water=TicketType(name='water',priority=2) 
        self.water.save()

        ticketypes=TicketType.objects.all()
        self.assertEqual(len(ticketypes),2)     

    def test_delete_ticketype(self):
        self.elec.save()

        self.garbage=TicketType(name='garbage',priority=3)
        self.garbage.save()

        self.garbage.delete()
        ticketypes=TicketType.objects.all()

        self.assertEqual(len(ticketypes),1)     


class TicketSubTypeTestClass(TestCase):
    #setup method
    def setUp(self):
    
        self.pole=TicketSubType(subtype='Fallen Pole')

    def test_instance(self):
        self.assertTrue(isinstance(self.pole,TicketSubType)) 

    def test_save_method(self):
        self.pole.save()
    
        subtypes=TicketSubType.objects.all()
        self.assertTrue(len(subtypes) > 0)

    def test_save_multiple_subtypes(self):
        self.pole.save()

        self.trans=TicketSubType(subtype='transformer') 
        self.trans.save()

        subtypes=TicketSubType.objects.all()
        self.assertEqual(len(subtypes),2)     


class DepartmentTestClass(TestCase):
    #setup method
    def setUp(self):
        self.water=Department(department_name='Water',department_description='deals with water issues')

    def test_instance(self):
        self.assertTrue(isinstance(self.water,Department)) 

    def test_save_method(self):
        self.water.save()
        departments=Department.objects.all()
        self.assertTrue(len(departments) > 0)

    def test_save_multiple_tickettypes(self):
        self.water.save()

        self.garbage=Department(department_name='Garbage',department_description='deals with garbage')
        self.garbage.save()

        departments=Department.objects.all()
        self.assertEqual(len(departments),2)     

    def test_delete_ticketype(self):
        self.water.save()

        self.garbage=Department(department_name='Garbage',department_description='deals with garbage')
        self.garbage.save()

        self.garbage.delete()
        departments=Department.objects.all()

        self.assertEqual(len(departments),1)         


