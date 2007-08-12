import objects
import BioPythonGUI

class Project:

    def __init__(self, name='New proj'):
	
	self.projectName = ''
	self.items = {}
	self.newItems = {}
	self.delItems = {}
	self.changed = False
	self.filename = ''
	self.base = None
	self.currentItem = None

    def addItem(self, item):
	
	self.items[item.name] = item
	self.newItems[item.name] = item
	self.changed = True
	try:
	    self.base.treestoreUpdate()
	except:
	    pass

    def getItem(self, item):
	
	if type(item)==str:
	    return self.items[item]
	else:
	    return self.items[item.name]
	self.changed = True

    def delItem(self, item):

	if type(item)==str:
	    self.delItems[item] = self.items[item]
	    del self.items[item]
	else:
	    self.delItems[item.name] = item
	    del self.items[item.name]
	self.changed = True
	self.base.treestoreUpdate()

    def getDBItems(self):
	
	out = []
	for item in self.items.values():
	    if item.__class__ == objects.DBItem:
		out.append(item)
	
	return out

    def getDBItemNames(self):
	
	out = []
	for item in self.items.values():
	    if item.__class__ == objects.DBItem:
		out.append(item.name)

	return out

    def getSequenceItems(self):

	out = []
	for item in self.items.values():
	    if item.__class__ == objects.SequenceItem:
		out.append(item)

	return out

    def getSequenceItemNames(self):

	out = []
	for item in self.items.values():
	    if item.__class__ == objects.SequenceItem:
		out.append(item.name)

	return out

    def getDBQueries(self):

	out = []
	for item in self.items.values():
	    if item.__class__ == objects.DBQuery:
		out.append(item)

	return out

    def getDBQueryNames(self):

	out = []
	for item in self.items.values():
	    if item.__class__ == objects.DBQuery:
		out.append(item.name)

	return out

    def getNames(self):
	return self.items.keys()

    def getNewItemNames(self):
        temp = self.newItems.keys()
        self.newItems = {}
        return temp

    def getDelItemNames(self):
	temp = self.delItems.values()
	self.delItems = {}
	return temp

    
    def save(self, filename=0):
	
	if filename==0:
	    filename=self.filename
	
	import cPickle

	ext = filename.split('.')[-1]
	if ext == filename:
	    filename += '.gbp'

	self.filename = filename

	file = open(filename, 'wb')

	cPickle.dump(self, file, -1)

	file.close()

	self.changed = False
