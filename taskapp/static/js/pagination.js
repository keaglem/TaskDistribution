function clickFunction( page_num) {
    var deviceId = $('#device-select').val();
    $('#display-area').load('/api/entries/'+ deviceId +'/' +page_num);
}
