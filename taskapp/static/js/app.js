var s, socket,
App = {
    settings: {
        displayArea: $('#display-area'),
        viewButton: $('#view-btn'),
        simButton: $('#sim-btn'),
        allSimButton: $('#all-sim-btn'),
        submitButton: $('#submit-btn'),
        lastClicked: $('#view-btn'),
    },

    init: function() {
        s = this.settings;
        socket = io.connect('http://' + document.domain + ':' + location.port + '/live_connect');
        socket.on('connect', function() {
            s.submitButton.append('<div class="connected">Connected to server</div>');
            socket.emit('my event', {data: 'I\'m connected!'});
        });
        socket.on('disconnect', function() {
            s.submitButton.removeClass("connected");
        });
        socket.on('active jobs', function(inputData) {
            s.submitButton.find(".connected").text(inputData.num_jobs + ' remaining jobs');
        });

        this.bindUIActions();
        this.updateDisplay();
    },


    bindUIActions: function() {
        s.viewButton.click(App.handleButtonClick(App.showSubmissions));
        s.submitButton.click(App.handleButtonClick(App.showSubmit));
        s.simButton.click(App.handleButtonClick(App.showSimulations));
        s.allSimButton.click(App.handleButtonClick(App.showAllSimulations));
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
    showSubmit: function(e) {
        s.displayArea.load('/api/upload')
    },
    showSimulations: function(e) {
        s.displayArea.load('/api/simulations')
    },
    showAllSimulations: function(e) {
        s.displayArea.load('/api/all_simulations')
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