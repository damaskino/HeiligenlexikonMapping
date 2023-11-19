$(document).ready(function() {
  $.ajax({
    url: 'test.json',
    dataType: 'json',
    success: function(data) {
      const dataArray = Object.entries(data).map(([key, value]) => ({ key, ...value }));

      $('#dataTable').DataTable({
        data: dataArray,
        columns: [
          { data: 'key', title: 'Key' },
          { data: 'SaintName' },
          { data: 'Gender' },
          { data: 'EntryLength' },
          { data: 'CanonizationStatus' },
          { data: 'NumberInHlex' },
          { data: 'RawFeastDay' },
          { data: 'OriginalText'}
          // Add more columns as needed
        ]
      });
    },
    error: function(xhr, status, error) {
      console.error('Error loading JSON file:', error);
    }
  });
});