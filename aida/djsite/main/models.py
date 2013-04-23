from django.db import models as m
from django_extensions.db.fields import UUIDField
from django.contrib.auth.models import User as AuthUser 
import getpass
import aida.jobmanager.submitter
import os
import os.path
from aida.djsite.settings.settings import LOCAL_REPOSITORY
#from uuidfield import UUIDField


class User(AuthUser):
    '''
    Need to extend the User class with uuid
    '''
    uuid = UUIDField(auto=True)
        
    
quality_choice = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))     

nodetype_choice = (("calculation","calculation"), ("data","data"), ("code","code"))

calcstate_choice = (('prepared', 'prepared'),
                    ('submitted', 'submitted'), 
                    ('queued', 'queued'),
                    ('running', 'runnning'),
                    ('failed', 'failed'),
                    ('finished', 'finished'),
                    ('completed', 'completed'))


class Node(m.Model):
    uuid = UUIDField(auto=True)
    name = m.CharField(max_length=255, unique=True)
    description = m.TextField(blank=True)
    crtime = m.DateTimeField(auto_now_add=True, editable=False)
    modtime = m.DateTimeField(auto_now=True)
    computer = 
    path = m.TextField(blank=True)
    state = m.CharField(max_length=255, choices=calcstate_choice, db_index=True)
    type = m.CharField(max_length=255, db_index=True)
    user = m.ForeignKey(User)
    quality = m.IntegerField(choices=quality_choice, null=True, blank=True) 
    metadata = m.TextField(blank=True)
    class Meta:
        abstract = True
                

attrdatatype_choice = (('float', 'float'), ('int', 'int'), ('txt', 'txt'),  ('bool', 'bool'))

class Attr(m.Model):
    '''
    Attributes are annotations ONLY for storing metadata and tagging. This is only for querying convenience.
    Actual input and output data should never go here, only convenient duplicates.
    '''
    uuid = UUIDField(auto=True) 
    node = m.ForeignKey('Node')
    name = m.CharField(max_length=255, db_index=True)
    txtval = m.TextField()
    floatval = m.FloatField()
    intval = m.IntegerField()
    boolval = m.BooleanField()
    datatype = m.CharField(max_length=255, choices=attrdatatype_choice, db_index=True)
    class Meta:
        unique_together = (("node", "key")


class Comment(m.Model):
    uuid = UUIDField(auto=True)
    user = m.ForeignKey(User)
    node = m.ForeignKey('Node')
    crtime = m.DateTimeField(auto_now_add=True, editable=False)
    content = m.TextField(blank=True)
    parent = m.ForeignKey('self', blank=True, null=True)

    
grouptype_choice = (('project', 'project'), ('collection', 'collection'), ('workflow', 'workflow'))

class Group(BaseClass):  
    uuid = UUIDField(auto=True)
    nodes = m.ManyToManyField('Node', blank=True, rel)  
    crtime = m.DateTimeField(auto_now_add=True, editable=False)
    name = m.CharField(max_length=255, unique=True)
    description = m.TextField(blank=True)
    type =  m.CharField(max_length=255, choices=calcgrouptype_choice, db_index=True)
    



##############################################################

class Data(EntityClass):
    calc = m.ForeignKey('Calc', related_name='dataout')      #unique parent Calc for each data
    type = m.CharField(max_length=255, db_index=True)
    numval = m.FloatField()
    group = m.ManyToManyField('DataGroup', blank=True)
    linkdata = m.ManyToManyField('self')
    attr = m.ManyToManyField('DataAttr', through = 'DataAttrVal')

#datagrouptype_choice = (('collection', 'collection'), ('relation', 'relation'))        




class Computer(NameClass):
    """Table of computers or clusters.

    Attributes:
        hostname: Full hostname of the host
        workdir: Full path of the aida folder on the host. It can contain
            the string {username} that will be substituted by the username
            of the user on that machine.
            The actual workdir is then obtained as
            workdir.format(username=THE_ACTUAL_USERNAME)
            Example: 
            workdir = "/scratch/{username}/aida/"
    """
    hostname = m.CharField(max_length=255, unique=True)
    workdir = m.CharField(max_length=255)
    
    
#class ComputerUsername(m.Model):
#    """Association of aida users with given remote usernames on a computer.
#
#    There is an unique_together constraint to be sure that each aida user
#    has no more than one remote username on a given computer.
#
#    Attributes:
#        computer: the remote computer
#        aidauser: the aida user
#        remoteusername: the username of the aida user on the remote computer
#    NOTE: this table can be eliminated in favor of a text field in each computer containing a dict.
#    """
#    computer = m.ForeignKey('Computer')
#    aidauser = m.ForeignKey(User)
#    remoteusername = m.CharField(max_length=255)
#
#    class Meta:
#        unique_together = (("aidauser", "computer"),)
#
#    def __unicode__(self):
#        return self.aidauser.username + " => " + \
#            self.remoteusername + "@" + self.computer.hostname
#

class Code(EntityClass):
    type = m.CharField(max_length=255, db_index=True) #to identify which parser/plugin
    computer = m.ForeignKey('Computer', blank=True) #for checking computer compatibility, empty means all
    group = m.ManyToManyField('CodeGroup', blank=True)
    attr = m.ManyToManyField('CodeAttr', through='CodeAttrVal')
    def __unicode__(self):
        return self.name

class CodeGroup(NameClass):  
    pass    
    
class CodeComment(CommentClass): 
    pass


class DataAttr(NameClass):
    '''
    Attributes are annotations ONLY for storing metadata and tagging. This is only for querying convenience.
    Actual input and output data should never go here.
    '''
    data = m.ForeignKey('Data')
    key = m.CharField(max_length=255, db_index=True)
    txtval = m.TextField()
    floatval = m.FloatField()
    intval = m.IntegerField()
    boolval = m.BooleanField()
    datatype = m.CharField(max_length=255, choices=attrdatatype_choice, db_index=True)
    class Meta:
        unique_together = (("data", "key")



