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
        return true;
    },

    normalStyle: function() {
        var range = this._getSelectionRange();
        if (range) {
            this._flattenHierarchy(range.startContainer,
                                   range.endContainer);
            this.target.focus();
        }
    },

    bold: function() {
        this._wrapSelection(document.createElement("b"));
        this.target.focus();
    },

    strikethrough: function() {
        this._wrapSelection(document.createElement("strike"));
        this.target.focus();
    },

    highlight: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-highlight");

        this._wrapSelection(elm);
        this.target.focus();
    },

    fixedWidth: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-monospace");

        this._wrapSelection(elm);
        this.target.focus();
    },

    small: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-size-small");

        this._wrapSelection(elm);
        this.target.focus();
    },

    normalSize: function() {
        var range = this._getSelectionRange();
        if (range) {
            this._flattenHierarchy(
                range.startContainer, range.endContainer,
                function(item) {
                    return (item.tagName == "SPAN"
                            && item.className.indexOf("note-size") > -1);
                }
            );
            this.target.focus();
        }
    },

    large: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-size-large");

        this._wrapSelection(elm);
        this.target.focus();
    },

    huge: function() {
        var elm = document.createElement("span");
        $(elm).addClass("note-size-huge");

        this._wrapSelection(elm);
        this.target.focus();
    },

    _flattenHierarchy: function(start, end, discard_fn) {
        if (start == end) {
            return;
        }

        var trash = [];
        var iter = start;
        do {
            iter = iter.nextSibling;
            if (!iter) {
                break;
            }

            if (!iter.innerHTML) {
                continue;
            }

            if (!discard_fn || discard_fn(iter)) {
                start.nodeValue += iter.innerHTML;
                trash.push(iter);
            }
        } while (iter != end);

        for (var i = 0; i < trash.length; i++) {
            $(trash[i]).remove();
        }
    },

    _wrapSelection: function(wrapper) {
        var range = this._getSelectionRange();
        if (range) {
            // insure that the selection range is inside of the editor
            var parent = this._findParentById(range.commonAncestorContainer,
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

    _getDocumentSelection: function() {
        if (window.getSelection) {
            return window.getSelection();
        } else if (document.selection) { // IE
            return document.selection.createRange();
        }
    },

    _getSelectionRange: function() {
        var selection = this._getDocumentSelection();
        if (selection.getRangeAt) {
            return window.getSelection().getRangeAt(0);
        } else { // Safari
            var range = document.createRange();
            range.setStart(selection.anchorNode, selection.anchorOffset);
            range.setEnd(selection.focusNode, selection.focusOffset);
            return range;
        }
    },

    _findParentById: function(subject, parentId) {
        if (subject == null || subject.tagName == "BODY") {
            return false;
        }
        
        if (subject.id == parentId) {
            return subject;
        }
        
        return this._findParentById(subject.parentNode, parentId); 
    },
});
