

class Item:

    def save(self, filename=0):
	
	import cPickle

	if filename==0:
            filename = self.name

	ext = filename.split('.')[-1]
	if ext == filename:
	    filename += self.extension

	file = open(filename, 'wb')

	cPickle.dump(file, self, -1)

	file.close()

    def changeName(self, newName):

        self.project.delItem(self.name)	
	self.name = newName
	self.project.addItem(self)


    def register(self):

        try:
            self.project.getIten(self.name)
        except KeyError:
            self.project.addItem(self)


seqnoname = 0
class SequenceItem(Item):
    
    
    def __init__(self, project, seq=None, name=0, typ=None):
	"""name is the name of the seq object, if none then
	an automatic name is assigned
	seq is a Bio.Seq.Seq object or a string
	and type is the type of the seq either DNA RNA or protein
	"""
	global seqnoname

	self.extension = '.seq'

	self.project = project

	if type(seq)==str:
	    from Bio.Seq import Seq
	    self.seq = Seq(seq.upper())
	else:
	    self.seq = seq

	if name == 0:
	    self.name = 'seq'+str(seqnoname)
	    seqnoname += 1
	else:
	    self.name = name

	if typ:
	    self.chgAlpha(typ)
	else:
	    typ = self.seq.alphabet

	self.checkAlpha()

	self.project.addItem(self)

    
    def checkAlpha(self):

	#here's a check to make sure the user is sane
	s = self.seq.tostring()
	for letter in self.seq.alphabet.letters:
	    s = s.replace(letter, '')
	if s:
	    raise NameError, 'Your input included letters not in the alphabet'
	

    def transcribe(self, name=0):
	
	from Bio import Transcribe

	out = None
	
	transcribers = ['ambiguous_transcriber', 'generic_transcriber', 
			'unambiguous_transcriber']

	for transcriber in transcribers:
	    try:
		exec('out = Transcribe.'+transcriber+'.transcribe(self.seq)')
	    except AssertionError:
		pass
	    else:
		seqItem = SeqenceItem(self.project, seq=out, name=name)
		return seqItem
	    
	return out


    def transpose(self, name=0):

	from Bio import Translate

	out = None

	translators = ['ambiguous_dna_by_id', 'ambiguous_dna_by_name',
		       'ambiguous_rna_by_id', 'ambiguous_rna_by_name', 
		       'unambiguous_dna_by_id', 'unambiguous_dna_by_name',
		       'unambiguous_rna_by_id', 'unambiguous_rna_by_name']

	for translator in translators:
	    try:
		exec('out = Translate.'+translator+'.translate(self.seq)')
	    except AssertionError:
		pass
	    else:
		seqItem = SeqenceItem(self.project, seq=out, name=name)
		return seqItem

	return out



    def chgAlpha(self, newAlpha):
	"""Accepts 'DNA' 'RNA' or 'protein' or an 
	alphabet object"""

	from Bio.Seq import Seq
	from Bio.Alphabet import IUPAC

	alpha = None
	if newAlpha=="DNA":
	    alpha = IUPAC.IUPACUnambiguousDNA()
	    self.typ = alpha
	elif newAlpha=="RNA":
	    alpha = IUPAC.IUPACUnambiguousDNA()
	    self.typ = alpha
	elif newAlpha=="protein":
	    alpha = IUPAC.IUPACProtein()
	    self.typ = alpha
	else:
	    raise NameError, "type not 'DNA', 'RNA', or 'protein'"

	if not alpha:
	    alpha = newAlpha

        self.seq = Seq(self.seq.tostring(), alpha)

	self.checkAlpha()

    
    def copy(self, name=0):
	
	from Bio.Seq import Seq

	return SequenceItem(seq=Seq(self.seq.tostring, self.seq.alphabet),
			    name=name, type=self.type, project=self.project)



dbitemnoname = 0
class DBItem(Item):

    def __init__(self, project, title='', seq=None, id='', descript='',
		 abstract='', record=None, name=0):
	global dbitemnoname

	self.extension = '.dbi'

	self.project = project

	if name==0:
	    self.name = 'dbitem'+str(dbitemnoname)
	    dbitemnoname += 1
	else:
	    self.name = name

	if record:
	    if not title:
		title = record.title
	    if not id:
		id = record.id
	    if not abstract:
		abstract = record.abstract

	self.abstract = abstract.replace('\n', '')
	self.seq = seq
	self.title = title
	self.id = id
	self.descript = descript
	self.record = record

	self.project.addItem(self)

	seqItem = SequenceItem(self.project, seq, name=id)

    def getAbstract(self):
	return self.abstract

    def getSequence(self):
	return self.seq

    def getTitle(self):
	return self.title

    def getID(self):
	return self.id

    def getDescription(self):
	return descript


    def copy(self, name=0):

	return DBItem(self.project, title=self.title, seq=self.seq, id=self.id,
		      descript=self.descript, abstract=self.abstract, 
		      record=self.record, name=name)


dbquerynoname = 0
class DBQuery(Item):

    def __init__(self, project, searchTerm='', database='PubMed',
		 type='nucleotide', maxResults=5, name=0):
	global dbquerynoname

	self.extension = '.dbq'

	self.project = project
	
	if name==0:
	    self.name = 'dbquery'+str(dbquerynoname)
	    dbquerynoname += 1
	else:
	    self.name = name

	self.items = {}

	self.searchTerm = searchTerm

	database = database.upper()
	if database == 'PUBMED' or database=='GENBANK':
	    self.database = 'PubMed'
	else:
	    raise NameError, 'No such database as '+database
	
	self.type = type
	
	self.maxResults = maxResults

	self.project.addItem(self)

    def search(self):

	if self.database=='PubMed':
	    from Bio import PubMed
	    from Bio import GenBank
	
	searchIds = PubMed.search_for(self.searchTerm, max_ids=self.maxResults)

	GBrecParser = GenBank.FeatureParser()
	ncbiDict = GenBank.NCBIDictionary(self.type, 'genbank',
					  parser=GBrecParser)
	

	from Bio import Medline
	
	MLrecParser = Medline.RecordParser()
	medlineDict = PubMed.Dictionary(delay=1.0, parser=MLrecParser)
	for id in searchIds:
	    MLrecord = medlineDict[id]
	    GBrecord = ncbiDict[id]
	    newDBItem = DBItem(self.project, seq=GBrecord.seq,
			       descript=GBrecord.description, id=id,
			       record=MLrecord)
	    self.items[id] = newDBItem


    def getItems(self):
	return self.items

    def copy(self, name=0):
	
	return DBQuery(self.project, searchTerm=self.searchTerm,
		       database=self.database, maxResults=self.maxResults,
		       type=self.type, name=name)
