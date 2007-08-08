import gtk
from proj import Project
import objects

project = Project()

#for debugging purposes:
seq = objects.SequenceItem(project, 'gtagatgatg', typ='DNA')


dead = False
def destroy(widget):
    global dead
    global project
    
    if dead:
        return
    else:
        dead = True

    if project.changed:
        quit_dialog = gtk.Dialog('Save on close')
	quit_dialog.add_button(gtk.STOCK_YES, gtk.RESPONSE_YES)
        quit_dialog.add_button(gtk.STOCK_NO, gtk.RESPONSE_NO)
	quit_dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NONE)

        label = gtk.Label('Do you want to save your project?')
	quit_dialog.vbox.pack_start(label, True, True, 0)
        label.show()

	response = quit_dialog.run()

        if response == gtk.RESPONSE_YES:
	    save_proj(widget)
	    gtk.main_quit()
        elif response == gtk.RESPONSE_NO:
	    gtk.main_quit()
        elif response == gtk.RESPONSE_NONE:
	    quit_dialog.destroy()
	    dead = False
	    return 1

	quit_dialog.destroy()
    gtk.main_quit()

def delete_event(widget, event=None):
    
    if destroy(widget):
        return True
    return False


def new_proj(widget):
    global project
    
    if project.changed:
        a = raw_input('Would you like to save? (y/n) ')
        if a:
            save_proj(widget)
    project = Project()


def open_proj(widget):
    global project

    filename = raw_input('What is the filename? ')

    if project.changed:
        a = raw_input('Would you like to save? (y/n) ')
        if a:
            save_proj(widget)

    import cPickle
    file = open(filename, 'rb')
    oldProj = project
    project = cPickle.load(file)
    project.base = oldProj.base

    project.base.treestoreUpdate()

def save_proj(widget):
    global project
    
    if not project.filename:
	save_proj_as(widget)
    else:
	project.save()
	

def save_proj_as(widget):
    global project

    filename = raw_input('What is the filename? ')

    project.save(filename)

def new_seq(widget):
    global project

    name = raw_input('Name? ')
    seq = raw_input('Seq? ')
    typ = raw_input('Type? ')

    sequence = objects.SequenceItem(project, name=name, seq=seq, typ=typ)
    

def open_seq(widget):
    global project

    filename = raw_input('What is the filename? ')
    
    import cPickle
    file = open(filename, 'rb')
    seq = cPickle.load(file)
    seq.register()

def save_seq(widget):
    global project
    
    seq = project.getItem(raw_input('What seq to save? '))
    
    seq.save()
    

def transcribe_seq(widget):
    global project

    seq = project.getItem(raw_input('What seq to transcribe? '))
    name = raw_input('What is the new name? ')
    if name == '':
        name = 0

    newSeq = seq.transcribe(name)
    

def transpose_seq(widget):
    global project

    seq = project.getItem(raw_input('What seq to transpose? '))
    name = raw_input('What is the new name? ')
    if name == '':
        name = 0

    newSeq = seq.transpose(name)

def chgalpha_seq(widget):
    global project

    seq = project.getItem(raw_input('What seq to change alpha? '))
    newAlpha = raw_input('What is the new Alpha? ')

    seq.chgAlpha(newAlpha)

def fasta_seq(widget):
    global project

    print widget

def genbank_seq(widget):
    global project

    print widget

def raw_seq(widget):
    global project

    print widget

def new_query(widget):
    global project

    query = objects.DBQuery(project)
    project.base.item_show(query)

def search_query(widget):
    global project

    query = project.getItem(raw_input('What query to search? '))

    query.search()

def save_query(widget):
    global project

    query = project.getItem(raw_input('What query to save? '))

    query.save()

def open_query(widget):
    global project

    filename = raw_input('What is the filename? ')
    
    import cPickle
    file = open(filename, 'rb')
    query = cPickle.load(file)
    query.register()





