
var TomboyWeb = {
    root_uri: '{{ root_uri }}',
    notes_uri: null,

    _get_notes: function(params, callback) {
        if(this.notes_uri == null) {
            var that = this;
            $.getJSON(this.root_uri, null, function(root) {
                $.getJSON(root['user-ref']['api-ref'], null, function(user) {
                    that.notes_uri = user['notes-ref']['api-ref'];
                    that._get_notes(params, callback);
                });
            });
        } else {
            // TODO: On certain errors, set notes_uri to null and
            //       start from scratch
            $.getJSON(this.notes_uri, params, callback);
        }
    },

    get_updates_since: function(version, noteJsonCallback) {
        this._get_notes({include_notes:true, since:version},
                        noteJsonCallback);
    },

    get_note_list: function(minimalNoteJsonCallback) {
        this._get_notes(null, minimalNoteJsonCallback);
    }
};

var OfflineNotesDatabase = {
    db: null,

    init_db: function() {
        // NOTE: openDatabase can only be called once, so init_db should
        //       also only be called once (could protect against this?)
        this.db = openDatabase('Notes', 0.1, 'Tomboy Online Notes', 5*1024*1024);
        this.check_db();
    },

    check_db: function() {
        // TODO: Error-checking, encapuslation, etc
        this.db.transaction(function(tx) {
            tx.executeSql('CREATE TABLE IF NOT EXISTS ' +
                          'notes(guid TEXT PRIMARY KEY ON CONFLICT REPLACE, title TEXT, content TEXT)',
                          []);
        });
    },

    wipe_db: function() {
        this.db.transaction(function(tx) {
            tx.executeSql('DROP TABLE notes');
        });
    },

    transaction: function(callback) {
        this.db.transaction(function(tx) {
            callback(tx);
        });
    },

    insert_note: function(guid, title, content, insertedRowCallback, currentTx) {
        // TODO: Should we handle case where there is no desired callback?
        var f = function(tx) {
            tx.executeSql('INSERT INTO notes(guid, title, content) VALUES (?,?,?)',
                          [guid, title, content],
                          insertedRowCallback,
                          OfflineNotesDatabase.on_error);
        };
        if(currentTx)
            f(currentTx);
        else
            this.db.transaction(f);
    },

    _select_from_notes: function(params, where, selectedRowCallback, currentTx) {
        var sql = "SELECT " + params + " FROM notes";
        if(where) {
            sql += " WHERE " + where;
        }
        var selection_processor = function(tx, rs) {
            for(var i=0; i < rs.rows.length; i++) {
                var note = rs.rows.item(i);
                selectedRowCallback(note);
            }
        };
        var f = function(tx) {
            tx.executeSql(sql,
                          [],
                          selection_processor,
                          OfflineNotesDatabase.on_error);
        };
        if(currentTx)
            f(currentTx);
        else
            this.db.transaction(f);
    },

    select_notes: function(selectedRowCallback, currentTx) {
        this._select_from_notes("*", null, selectedRowCallback, currentTx);
    },

    select_note_guids: function(selectedRowCallback, currentTx) {
        this._select_from_notes("guid", null, selectedRowCallback, currentTx);
    },

    deleteAtGuid: function(guid, onSuccess, currentTx) {
        var f = function(tx) {
            tx.executeSql("DELETE FROM notes WHERE guid=?", [guid],
                          onSuccess,
                          OfflineNotesDatabase.on_error);
        };
        if(currentTx)
            f(currentTx);
        else
            this.db.transaction(f);
    },

    on_error: function(tx, e) {
        alert("There has been a db error: " + e.message);
    }
};

var NoteSynchronizer = {
    sync: function(noteAddedCallback) {
        OfflineNotesDatabase.check_db(noteAddedCallback);
        var lastSyncRev = localStorage.getItem('latest-sync-revision');
        if (lastSyncRev == null)
            lastSyncRev = -1;

        // Get note updates since last sync
        TomboyWeb.get_updates_since(lastSyncRev, function(noteUpdates) {
            // Get full note list to check for deleted notes
            TomboyWeb.get_note_list(function(noteList) {
                // Record latest sync rev on server
                var latestServerRev = noteUpdates['latest-sync-revision'];

                OfflineNotesDatabase.transaction(function(syncTx) {
                    // Check for new notes (new guid) with local title conflicts, handle
                    // TODO

                    // Process new notes and note updates, handle conflicts

                    // Check for notes deleted on server

                    // Build content for PUT for any local modificatons:
                    //      * All new and modified notes
                    //      * All deleted notes
                    //      * Set expected new sync rev to latest server sync rev + 1

                    // Set local sync rev to new latest server sync rev


                    var insertCallbackMaker = function(note) {
                        return function() {
                            // TODO: Ugh, this is gross. Calling this method
                            //       with both JSON objects and db row objects
                            note.content = note['note-content'];
                            noteAddedCallback(note);
                        };
                    };
                    for(var i=0; i < noteUpdates.notes.length; i++) {
                        var note = noteUpdates.notes[i];
                        // NOTE: Tricky ON CONFLICT REPLACE option makes this INSERT
                        //       magically turn into a DELETE+INSERT if the row already
                        //       exists.
                        // TODO: This is probably wasteful since we should most likely
                        //       prefer optimizing the UPDATE case over the new INSERT
                        //       case.
                        OfflineNotesDatabase.insert_note(note.guid, note.title, note['note-content'],
                                                         insertCallbackMaker(note), syncTx);
                    }

                    // Look for notes that have been deleted on the server
                    var allNoteGuids = [];
                    for(var i=0; i < noteList.notes.length; i++) {
                        allNoteGuids.push(noteList.notes[i].guid);
                    }
                    OfflineNotesDatabase.select_note_guids(function(noteInfo) {
                        var guid = noteInfo.guid;
                        if (allNoteGuids.indexOf(guid) == -1) {
                            OfflineNotesDatabase.deleteAtGuid(guid, function(tx,rs) {
                                // TODO: Remove this from NoteSynchronizer, should be passed in or something
                                $('#note-title-list > li#' + guid).remove();
                            }, syncTx);
                        }
                    }, syncTx);

                    // TODO: Error-handling whenever using localStorage (applies elsewhere)
                    localStorage.setItem('latest-sync-revision',
                                         noteUpdates['latest-sync-revision']);
                });

            });
        });
    }
};

$(function() {
    // Set up controls
    $('#wipe').bind('click', function(event) {
        OfflineNotesDatabase.wipe_db();
        localStorage.setItem('latest-sync-revision', -1);
        $('#note-title-list > li').remove();
    });
    $('#beginSync').bind('click', function(event) {
        NoteSynchronizer.sync(add_note_list_item);
    });

    // TODO: Refactor, move somewhere reasonable
    function add_note_list_item(note) {
        $('<li id="' + note.guid + '"><a href="#' + note.guid + '-page">' + note.title + '</a></li>').appendTo('#note-title-list');
        $('li#' + note.guid).bind('mouseenter', note, function(event) {
            $('.note-content-page').remove();
            $('.note-content-edit-page').remove();
            var note = event.data;

            // Convert content XML to HTML
            // (based on MDC example, could be cleaner)
            var parser2 = new DOMParser();
            var xsltProcessor=new XSLTProcessor();
            var req = new XMLHttpRequest();
            req.open("GET", "{{ note_xml_to_html_xsl_uri }}", false);
            req.send(null);
            var xsldoc = req.responseXML;
            xsltProcessor.importStylesheet(xsldoc);
            var dom = parser2.parseFromString('<note-content version="0.1" xmlns:link="http://beatniksoftware.com/tomboy/link" xmlns:size="http://beatniksoftware.com/tomboy/size" xmlns="http://beatniksoftware.com/tomboy">' + note.content + '</note-content>',
                                              'text/xml');
            var html = xsltProcessor.transformToFragment(dom, document);

            var pageId = note.guid + '-page';
            var editPageId = note.guid + '-edit-page';

            // Set up note viewing page
            $('<div data-role="page" class="note-content-page" id="' + pageId + '">' +
              '<div data-role="header">' +
                    '<h1>' + note.title + '</h1>' +
                    '<a href="#' + editPageId + '" data-icon="gear" id="edit-note">Edit</a>' +
              '</div>' +
              '<div data-role="content"><p></p></div>' +
              '</div>')
              .page()
              .insertAfter('#note-list-page');

            // Set up note editing page
            $('<div data-role="page" class="note-content-edit-page" id="' + editPageId + '">' +
              '<div data-role="header">' +
                    '<a href="#' + pageId + '" data-icon="delete" class="cancel-edit">Cancel</a>' +
                    '<h1>' + note.title + '</h1>' +
                    '<a href="#" data-icon="check" class="save-edit">Save</a>' +
              '</div>' +
              '<div data-role="content"><p/></div>' +
              '</div>')
              .page()
              .insertAfter('#' + pageId);

            // Inject note HTML into note viewing page
            $('div#' + pageId + ' [data-role="content"] p')
            .append(html);

            // Inject markdown editor into note editing page
            $('div#' + editPageId + ' p')  // TODO: Fix this selector, figure out why real one didn't work
            .append("<textarea>test</textarea>");
            $('div#' + editPageId + ' textarea') // TODO: Why is this the only way I can set up the textarea?
            .text(note.content);
        });
        //$('li#' + note.guid).bind('mouseleave', note, function(event) {
        //    var note = event.data;
        //    $('div#' + note.guid + '-page').remove();
        //});
        $("#note-title-list").listview('refresh');
    }

    OfflineNotesDatabase.init_db();

    // Show cached notes
    OfflineNotesDatabase.select_notes(add_note_list_item);
});
