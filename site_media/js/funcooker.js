/*
 * Copyright (c) 2009 Brad Taylor <brad@getcoded.net>
 *
 * Permission is hereby granted, free of charge, to any person obtaining 
 * a copy of this software and associated documentation files (the 
 * "Software"), to deal in the Software without restriction, including 
 * without limitation the rights to use, copy, modify, merge, publish, 
 * distribute, sublicense, and/or sell copies of the Software, and to 
 * permit persons to whom the Software is furnished to do so, subject to 
 * the following conditions: 
 *  
 * The above copyright notice and this permission notice shall be 
 * included in all copies or substantial portions of the Software. 
 *  
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
 *
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

    boldSelection: function() {
    },

    wrapSelection: function(wrapper) {
        var range = this.getDocumentSelection();
        if (range) {
            // insure that the selection range is inside of the editor
            var parent = this.findParentById(range.commonAncestorContainer,
                                             target.id);
            if (!parent) {
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
