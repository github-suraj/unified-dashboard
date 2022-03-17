$('#category').on('change', function() {
    var category = this.value;
    var url = '/blogs/category/' + category + '/view';
    window.location.replace(url);
});

$('#user_category').on('change', function() {
    var username = $('#username').val();
    var category = this.value;
    var url = '/blogs/' + username + '/' + category;
    window.location.replace(url);
});