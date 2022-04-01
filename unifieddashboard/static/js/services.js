$('#service_categories').on('change', function() {
    var url = new URL(window.location);
    var category = this.value;
    if (category === 'All') {
        url.searchParams.delete('category');
    } else {
        url.searchParams.set('category', category);
    }
    window.location.replace(url);
});

$('#service_statuses').on('change', function() {
    var url = new URL(window.location);
    var status = this.value;
    if (status === 'All') {
        url.searchParams.delete('status');
    } else {
        url.searchParams.set('status', status);
    }
    window.location.replace(url);
});

$('#service_priorities').on('change', function() {
    var url = new URL(window.location);
    var priority = this.value;
    if (priority === 'All') {
        url.searchParams.delete('priority');
    } else {
        url.searchParams.set('priority', priority);
    }
    window.location.replace(url);
});
