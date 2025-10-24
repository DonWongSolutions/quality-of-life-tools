$(document).ready(function() {
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Using 'change' event specifically for select and checkbox
    $('#configForm input, #configForm select').on('input change', function() {
        $.ajax({
            url: '/preview_rproxy',
            method: 'POST',
            data: $('#configForm').serialize(),
            success: function(response) {
                $('#livePreview').html('<pre>' + escapeHtml(response) + '</pre>');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error:', textStatus, errorThrown);
            }
        });
    });
});