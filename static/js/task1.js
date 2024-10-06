window.onload = function() {
    fetch('/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => response.json())
    .then(data => {
            document.getElementById('branch').value = data[0];
            document.getElementById('customNo').value = data[1];
            document.getElementById('arabicName').value = data[2];
            document.getElementById('arabicDescription').value = data[3];
            document.getElementById('englishName').value = data[4];
            document.getElementById('englishDescription').value = data[5];
            document.getElementById('note').value = data[6];
            document.getElementById('address').value = data[7];
    })
    .catch(error => console.error('Error fetching data:', error));
};

$('#addBtn').on('click', function(e) {
    e.preventDefault();
    var customNo = $('#customNo').val();
    var arabicName = $('#arabicName').val();
    var arabicDescription = $('#arabicDescription').val();
    var englishName = $('#englishName').val();
    var englishDescription = $('#englishDescription').val();
    var note = $('#note').val();
    var address = $('#address').val();

    $.ajax({
        url: '/add',
        method: 'POST',
        data: {
            custom_num: customNo,
            ar_name: arabicName,
            ar_desc: arabicDescription,
            en_name: englishName,
            en_desc: englishDescription,
            note: note,
            address: address
        },
        success: function(response) {
            alert('New branch is added with empty fields!');
            window.location.href = '/' + new_branch;


        },
        error: function(err) {
            alert('Error adding data');
        }
    });
});

$('#saveBtn').on('click', function(e) {
    e.preventDefault();
    var id = $('#branch').val();
    var customNo = $('#customNo').val();
    var arabicName = $('#arabicName').val();
    var arabicDescription = $('#arabicDescription').val();
    var englishName = $('#englishName').val();
    var englishDescription = $('#englishDescription').val();
    var note = $('#note').val();
    var address = $('#address').val();

    $.ajax({
        url: '/edit',
        method: 'POST',
        data: {
            id: id,
            custom_num: customNo,
            ar_name: arabicName,
            ar_desc: arabicDescription,
            en_name: englishName,
            en_desc: englishDescription,
            note: note,
            address: address
        },
        success: function(response) {
            alert('Data edit successfully!');


        },
        error: function(err) {
            alert('Error adding data');
        }
    });
});