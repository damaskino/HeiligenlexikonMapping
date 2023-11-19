$(document).ready(function() {
  $('#dataTable').DataTable({
    ajax: {
      url: 'test.json', // Replace 'data.json' with your JSON file path
      dataSrc: ''
    },
    columns: [
      { data: 'SaintName' },
      { data: 'CanonizationStatus' }
      { data: 'EntryLength' }
      // Define more columns as needed
    ]
  });
});