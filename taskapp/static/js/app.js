var s,
App = {
    settings: {
        displayArea: $('#display-area'),
        viewButton: $('#view-btn'),
        submitButton: $('#submit-btn'),
        lastClicked: $('#view-btn'),
    },

    init: function() {
        s = this.settings;
        this.bindUIActions();
        this.updateDisplay();
    },

    bindUIActions: function() {
        s.viewButton.click(App.handleButtonClick(App.showSubmissions));
        s.submitButton.click(App.handleButtonClick(App.showSubmit));
        // TODO: add this functionality back for cluster display
        //s.deviceSelect.change(App.updateDisplay);
    },

    getValidURI: function(base, id) {
        if(typeof(id)==='undefined') 
            return base;
        if (id === null)
            return base;
        return base + '/' + id;
    },
    getEntryURI: function(id) {
        return App.getValidURI('/api/entries',id);
    },
    getAddEntryURI: function(id) {
        return App.getValidURI('/nest/addentry',id);
    },


    loadNoCache: function(elem, url, success) {
        $.ajax(url, {
            dataType: 'html',
            cache: false,
            success: function(data) {
                elem.html(data);
                success();
            }
        });
    },

    getActiveDeviceId: function() {
        return s.deviceSelect.val();
    },

    updateDisplay: function() {
        s.lastClicked.click();
    },

    handleButtonClick: function(displayCallback) {
        return function(e) {
            $(this).siblings().removeClass('active');
            $(this).addClass('active');
            s.lastClicked = this;
            return displayCallback();
        }
    },

    showEntryText: function(e) {
        id = $(this).data('entryId');
        App.loadNoCache(s.entryTextModalBody, '/api/entries/text/' + id, function() {
            s.entryTextModal.modal('show');
        });
    },
    showSubmissions: function(e) {
        s.displayArea.load('/api/submissions');
    },
    showThermostat: function(e) {
        s.displayArea.load(App.getAddEntryURI(App.getActiveDeviceId()));
    },
    showEntries: function(e) {
        App.loadNoCache(s.displayArea, App.getEntryURI(App.getActiveDeviceId()), function() {
            $('tr[data-entry-id]').click(App.showEntryText);
        });
    },

};


(function() {
    App.init();
})();