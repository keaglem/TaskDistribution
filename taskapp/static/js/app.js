var s,
App = {
    settings: {
        displayArea: $('#display-area'),
        deviceSelect: $('#device-select'),
        thermostatButton: $('#thermostat-btn'),
        entriesButton: $('#entries-btn'),
        entryTextModal: $('#entry-text-modal'),
        entryTextModalBody: $('#entry-text-modal .modal-body'),
        nestTextModal: $('#nest-text-modal'),
        nestTextModalBody: $('#nest-text-modal .modal-body'),
        lastClicked: $('#entries-btn'),
    },

    init: function() {
        s = this.settings;
        this.bindUIActions();
        this.updateDisplay();
    },

    bindUIActions: function() {
        s.thermostatButton.click(App.handleButtonClick(App.showThermostat));
        s.entriesButton.click(App.handleButtonClick(App.showEntries));
        s.deviceSelect.change(App.updateDisplay);
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