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

function blogCommentUpdateShow(commentId) {
    // Show edit buttons if hide (was open for editing)
    $('.edit-comment').css('display', 'block');
    // Hide all forms if already open for editing
    $('.update-div').hide();
    // Show all paras if hide (was open for editing)
    $('.update-para').show();
    // Hide edit button for the comment on which edit button is clicked
    $('#edit_' + commentId).css('display', 'none');
    // Hide para for the comment on which edit button is clicked
    $('#view_' + commentId).hide();
    // Add value to the textarea form field on which edit button is clicked
    document.getElementById('id_comment_' + commentId).value = $('#view_' + commentId).html();
    // Show form for the comment on which edit button is clicked
    $('#update_' + commentId).show();
}

function blogCommentUpdateHide(commentId) {
    // Show edit button on which comment editing canceled
    $('#edit_' + commentId).css('display', 'block');
    // Show para on which comment editing canceled
    $('#view_' + commentId).show();
    // Hide form on which comment editing canceled
    $('#update_' + commentId).hide();
}
