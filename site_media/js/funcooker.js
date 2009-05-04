/*
 * Copyright (c) 2009 Brad Taylor <brad@getcoded.net>
 *
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU Affero General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option) any
 * later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/* Here comes the funcooker! */
var FunCooker = DUI.Class.create({
    target: null,

    init: function(target) {
        this.target = $(target);

        if (this.editingEnabled()) {
            this.target.attr('contenteditable', true);
        }
    },

    editingEnabled: function() {
        // TODO: Support other platforms
        return $.browser.mozilla;
    },

    normalStyle: function() {
        // TODO:
    },

    bold: function() {
        this.wrapSelection(document.createElement("b"));
        this.target.focus();
    },

    strikethrough: function() {
        this.wrapSelection(document.createElement("strike"));
        this.target.focus();
    },

    highlight: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-highlight");

        this.wrapSelection(elm);
        this.target.focus();
    },

    fixedWidth: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-monospace");

        this.wrapSelection(elm);
        this.target.focus();
    },

    small: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-size-small");

        this.wrapSelection(elm);
        this.target.focus();
    },

    normalSize: function() {
        // TODO:
    },

    large: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-size-large");

        this.wrapSelection(elm);
        this.target.focus();
    },

    huge: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-size-huge");

        this.wrapSelection(elm);
        this.target.focus();
    },

    wrapSelection: function(wrapper) {
        var range = this.getDocumentSelection();
        if (range) {
            // insure that the selection range is inside of the editor
            var parent = this.findParentById(range.commonAncestorContainer,
                                             this.target.id);
            if (!parent) {
		// TODO: Fallback behavior should be to move the caret to the
		// end of the div and wrap it.
                return;
            }

	    // TODO: make this work in the general case, e.g.: when sel spans
	    // multiple elements (<li>, <p>, etc)
            range.surroundContents(wrapper);
        }
    },

    getDocumentSelection: function() {
        if ($.browser.mozilla) {
            return window.getSelection().getRangeAt(0);
        }
    },

    findParentById: function(subject, parentId) {
        if (subject == null || subject.tagName == "BODY") {
            return false;
        }
        
        if (subject.id == parentId) {
            return subject;
        }
        
        return this.findParentById(subject.parentNode, parentId); 
    },
});
