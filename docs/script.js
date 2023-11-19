$(document).ready(function() {
  $.ajax({
    url: 'test.json',
    dataType: 'json',
    success: function(data) {
      const dataArray = Object.values(data);

      $('#dataTable').DataTable({
        data: dataArray,
        columns: [
          { data: 'SaintName' },
          { data: 'CanonizationStatus' },
          { data: 'NumberInHlex' },
          { data: 'RawFeastDay' },
          // Add more columns as needed
        ]
      });
    },
    error: function(xhr, status, error) {
      console.error('Error loading JSON file:', error);
    }
  });
});