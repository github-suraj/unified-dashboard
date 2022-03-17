$('#category').on('change', function() {
    var category = this.value;
    var url = '/blogs/category/' + category;
    window.location.replace(url);
});
