#/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk

import functions
import objects


class Base:

    def __init__(self):
        """Initalizes main window and calls for menu and the view
        to be created"""

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('BioPython GUI')
        
        self.window.connect('destroy', functions.destroy)
        self.window.connect('delete_event', functions.delete_event)
	
	self.stuff = gtk.VBox(False, 0)
	self.window.add(self.stuff)
	self.stuff.show()

        self._menus()
	self.DispViewWindow()

	self.window.set_size_request(600, 800)
        self.window.show()


    def main(self):
        """calls gtk.main() to start the program"""
        gtk.main()


    def DispViewWindow(self):
        """This is the viewing window (everything but the menus)
        currently contains left panel for item view and main panel
        for Content view"""
	
	self.view_window = gtk.HPaned()
	self.stuff.pack_start(self.view_window, True, True, 0)
	self.view_window.show()

	self.contentFrame = gtk.Frame('Content View')
	self.contentFrame.show()
	self.view_window.add1(self.DispViewItems())
	self.view_window.add2(self.contentFrame)

    def DispViewItems(self):
        """This is the view for the items. Returns a widget to be packed
        by something else. Adds a tree view but does not create the
        treestore object."""

	scroller = gtk.ScrolledWindow()
	scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	scroller.show()

	self.treestore = gtk.TreeStore(str)

	self.treestoreInit()
	self.treestoreUpdate()

        self.treeview = gtk.TreeView(self.treestore)

        tvcolumn = gtk.TreeViewColumn('Items')

        self.treeview.append_column(tvcolumn)

        cell = gtk.CellRendererText()

        tvcolumn.pack_start(cell, True)

        tvcolumn.add_attribute(cell, 'text', 0)

        tvcolumn.set_sort_column_id(0)

        scroller.add(self.treeview)

        scroller.show_all()

	self.selection = self.treeview.get_selection()
	self.selection.set_mode(gtk.SELECTION_SINGLE)

	self.treeview.connect('row-activated', self.item_show)


	return scroller

    def treestoreInit(self):
    
	self.dbqueryiter = self.treestore.append(None, ['DB Query'])
	self.dbitemiter = self.treestore.append(None, ['DB Items'])
	self.seqiter = self.treestore.append(None, ['Sequences'])


    def treestoreUpdate(self):
        """This updates the treestore object"""

	for item in functions.project.getNewItemNames():
            clas = functions.project.getItem(item).__class__
            if clas == objects.SequenceItem:
                self.treestore.append(self.seqiter, [item])
            elif clas == objects.DBItem:	
                self.treestore.append(self.dbitemiter, [item])
            elif clas == objects.DBQuery:
                self.treestore.append(self.dbqueryiter, [item])


    def DispViewContent(self, widget=None):
        """Puts widget in the content window
        DOES show the widget"""

	if not widget:
	    return
	if self.contentFrame.get_children():
	    self.contentFrame.remove(self.contentFrame.get_children()[0])
	
	self.contentFrame.add(widget)
	widget.show()

	return self.contentFrame

    def item_show(self, obj=None, iter=None, path=None):
        """Content view for all items normally called by
        double-click on item, but if called other then
        obj is the item to be displayed and no iter or path
        """

        if iter and path:        
            model, iter = self.selection.get_selected()
            name = model.get_value(iter, 0)
            if name == 'Sequences' or name == 'DB Items' or name == 'DB Query':
                return

            item = functions.project.getItem(name)
        else:
            item = obj

        if item.__class__ == objects.SequenceItem:
            new = self.seqItem_show(item)
        elif item.__class__ == objects.DBItem:
            new = self.DBItem_show(item)
        else:
            new = self.DBQuery_show(item)

        vbox = gtk.VBox()

        label = gtk.Label(item.name)
        label.show()
        vbox.pack_start(label, False, False, 5)

        vbox.pack_end(new, True, True, 0)
        self.DispViewContent(vbox)

    def seqItem_show(self, item):
        """content view for specifically the Sequence item"""

        vbox = gtk.VBox()
        vbox.show()

        scroller = gtk.ScrolledWindow()
        scroller.show()
        scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_end(scroller, True, True, 2)

        label = gtk.Label(item.name)
        label.show()
        vbox.pack_start(label, False, False, 0)

        textArea = gtk.TextView()
        textArea.set_editable(False)
        textArea.show()
        scroller.add(textArea)

        textArea.set_wrap_mode(gtk.WRAP_CHAR)

        text = textArea.get_buffer()
        text.set_text(item.seq.tostring())

        return vbox

    def DBItem_show(self, item):
        """content view for specifically the DB item"""
        
        vbox = gtk.VBox()
        vbox.show()

        title = gtk.TextView()
	title.set_editable(False)
        title.show()
        title.set_wrap_mode(gtk.WRAP_WORD)
        text = title.get_buffer()
        text.set_text(item.descript)
	vbox.pack_start(title, False, True, 5)

        id = gtk.Label('ID: '+item.id)
        id.show()
        vbox.pack_start(id, False, True, 5)

	rest = gtk.Frame()
	rest.show()
	vbox.pack_end(rest, True, True, 10)

	pane = gtk.VPaned()
	pane.show()
	rest.add(pane)

        descript = gtk.TextView()
        descript.set_editable(False)
        descript.show()
        pane.add1(descript)
        descript.set_wrap_mode(gtk.WRAP_WORD)
        text = descript.get_buffer()
        text.set_text(item.descript)

	pane2 = gtk.VPaned()
	pane2.show()
	pane.add2(pane2)

        scroller1 = gtk.ScrolledWindow()
        scroller1.show()
        pane2.add1(scroller1)
        scroller1.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        abstract = gtk.TextView()
        abstract.set_editable(False)
        abstract.show()
        scroller1.add(abstract)
        abstract.set_wrap_mode(gtk.WRAP_WORD)
        abstractText = abstract.get_buffer()
        abstractText.set_text(item.abstract)
        
        scroller2 = gtk.ScrolledWindow()
        scroller2.show()
        pane2.add2(scroller2)
        scroller2.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        textArea = gtk.TextView()
        textArea.set_editable(False)
        textArea.show()
        scroller2.add(textArea)
        textArea.set_wrap_mode(gtk.WRAP_CHAR)
        text = textArea.get_buffer()
        text.set_text(item.seq.tostring())

        return vbox


    def DBQuery_show(self, item):
        """content view for specifically the DBQuery item"""
        
        vbox = gtk.VBox()
        vbox.show()

        box1 = gtk.HBox()
        box1.show()
        vbox.pack_start(box1)

        label2 = gtk.Label('Search Term')
        label2.show()
        box1.pack_start(label2)

        self.searchEntry = gtk.Entry()
        self.searchEntry.show()
        box1.pack_end(self.searchEntry, True, True, 10)
        self.searchEntry.set_text(item.searchTerm)

        box2 = gtk.HBox()
        box2.show()
        vbox.pack_start(box2)

        label3 = gtk.Label('Database')
        label3.show()
        box2.pack_start(label3)

        self.dbRadio1 = gtk.RadioButton(None, 'PubMed/GenBank')
        self.dbRadio1.show()
        box2.pack_start(self.dbRadio1)

        box3 = gtk.HBox()
        box3.show()
        vbox.pack_start(box3)

        label4 = gtk.Label('Search Type')
        label4.show()
        box3.pack_start(label4)

        box4 = gtk.VBox()
        box4.show()
        box3.pack_start(box4)

        self.typeRadio1 = gtk.RadioButton(None, 'nucleotide')
        self.typeRadio1.show()
        box4.pack_start(self.typeRadio1)
        self.typeRadio2 = gtk.RadioButton(self.typeRadio1, 'protein')
        self.typeRadio2.show()
        box4.pack_start(self.typeRadio2)
        self.typeRadio3 = gtk.RadioButton(self.typeRadio1, 'genome')
        self.typeRadio3.show()
        box4.pack_start(self.typeRadio3)

        if item.type=='nucleotide':
            self.typeRadio1.set_active(True)
        elif item.type=='protien':
            self.typeRadio2.set_active(True)
        elif item.type=='genome':
            self.typeRadio3.set_active(True)

        box5 = gtk.HBox()
        box5.show()
        vbox.pack_start(box5)

        label5 = gtk.Label('Max Results')
        label5.show()
        box5.pack_start(label5)

        self.maxEntry = gtk.Entry()
        self.maxEntry.show()
        box5.pack_end(self.maxEntry, True, True, 10)
        self.maxEntry.set_text(str(item.maxResults))

        self.searchButton = gtk.Button('Search')
        self.searchButton.show()
        vbox.pack_start(self.searchButton, False, False)
        self.searchButton.set_border_width(20)
	self.searchButton.connect('clicked', self.search_action, item)

        return vbox


    def search_action(self, widget, item):
        """Called when search is hit on the DBQuery view"""
	
	searchTerm = self.searchEntry.get_text()
	
	if self.dbRadio1.get_active():
	    db = 'PubMed'
	
	if self.typeRadio1.get_active():
	    type = 'nucleotide'
	elif self.typeRadio2.get_active():
	    type = 'protein'
	elif self.typeRadio3.get_active():
	    type = 'genome'

	max = int(self.maxEntry.get_text())

	item.searchTerm = searchTerm
	item.database = db
	item.type = type
	item.maxResults = max

	item.search()
	
    def _menus(self):
        """This makes the root menu and all of its children
        """

        #Root menu bar
        self.menu_bar = gtk.MenuBar()
        file_item = gtk.MenuItem('File')
        seq_item = gtk.MenuItem('Sequence')
        db_item = gtk.MenuItem('Database')
        self.menu_bar.append(file_item)
        self.menu_bar.append(seq_item)
        self.menu_bar.append(db_item)
        file_item.show()
        seq_item.show()
        db_item.show()

        #File menu
        self.file_menu = gtk.Menu()
        new_proj_item = gtk.MenuItem('New Project')
        save_proj_item = gtk.MenuItem('Save Project')
        save_proj_as_item = gtk.MenuItem('Save Project as ...')
        open_proj_item = gtk.MenuItem('Open Project')
        quit_item = gtk.MenuItem('Quit')
        self.file_menu.append(new_proj_item)
        self.file_menu.append(save_proj_item)
        self.file_menu.append(save_proj_as_item)
        self.file_menu.append(open_proj_item)
        self.file_menu.append(quit_item)
        new_proj_item.show()
        save_proj_item.show()
        save_proj_as_item.show()
        open_proj_item.show()
        quit_item.show()
        
        #Sequence menu
        self.seq_menu = gtk.Menu()
        new_seq_item = gtk.MenuItem('New Sequence')
        new_seq_file_item = gtk.MenuItem('New Sequence from File')
        save_seq_item = gtk.MenuItem('Save Sequence')
        open_seq_item = gtk.MenuItem('Open Sequence')
        transcribe_seq_item = gtk.MenuItem('Transcribe Sequence')
        transpose_seq_item = gtk.MenuItem('Transpose Sequence')
        chgalpha_seq_item = gtk.MenuItem('Change Alphabet')
        self.seq_menu.append(new_seq_item)
        self.seq_menu.append(new_seq_file_item)
        self.seq_menu.append(save_seq_item)
        self.seq_menu.append(open_seq_item)
        self.seq_menu.append(transcribe_seq_item)
        self.seq_menu.append(transpose_seq_item)
        self.seq_menu.append(chgalpha_seq_item)
        new_seq_item.show()
        new_seq_file_item.show()
        save_seq_item.show()
        open_seq_item.show()
        transcribe_seq_item.show()
        transpose_seq_item.show()
        chgalpha_seq_item.show()
        
        
        #New Sequence from file menu
        self.new_seq_file_menu = gtk.Menu()
        fasta_seq_item = gtk.MenuItem('FASTA file')
        genbank_seq_item = gtk.MenuItem('GenBank file')
        raw_seq_item = gtk.MenuItem('Raw file')
        self.new_seq_file_menu.append(fasta_seq_item)
        self.new_seq_file_menu.append(genbank_seq_item)
        self.new_seq_file_menu.append(raw_seq_item)
        fasta_seq_item.show()
        genbank_seq_item.show()
        raw_seq_item.show()
        new_seq_file_item.set_submenu(self.new_seq_file_menu)
        

        #Database menu
        self.db_menu = gtk.Menu()
        new_query_item = gtk.MenuItem('New Query')
        open_query_item = gtk.MenuItem('Open Query')
        save_query_item = gtk.MenuItem('Save Query')
        self.db_menu.append(new_query_item)
        self.db_menu.append(open_query_item)
        self.db_menu.append(save_query_item)
        new_query_item.show()
        open_query_item.show()
        save_query_item.show()

        
	
        self.stuff.pack_start(self.menu_bar, False, False, 2)
        self.menu_bar.show()

        file_item.set_submenu(self.file_menu)
        seq_item.set_submenu(self.seq_menu)
        db_item.set_submenu(self.db_menu)

        file_item.show()
        seq_item.show()
        db_item.show()


        #Now we connect everything
        new_proj_item.connect('activate', functions.new_proj)
        open_proj_item.connect('activate', functions.open_proj)
        save_proj_item.connect('activate', functions.save_proj)
        save_proj_as_item.connect('activate', functions.save_proj_as)
        quit_item.connect('activate', functions.destroy)
        
        new_seq_item.connect('activate', functions.new_seq)
        open_seq_item.connect('activate', functions.open_seq)
        save_seq_item.connect('activate', functions.save_seq)
        transcribe_seq_item.connect('activate', functions.transcribe_seq)
        transpose_seq_item.connect('activate', functions.transpose_seq)
        chgalpha_seq_item.connect('activate', functions.chgalpha_seq)

        fasta_seq_item.connect('activate', functions.fasta_seq)
        genbank_seq_item.connect('activate', functions.genbank_seq)
        raw_seq_item.connect('activate', functions.raw_seq)

        new_query_item.connect('activate', functions.new_query)
        save_query_item.connect('activate', functions.save_query)
        open_query_item.connect('activate', functions.open_query)
        
        
        

if __name__=='__main__':
    base = Base()
    functions.project.base = base
    base.main()
