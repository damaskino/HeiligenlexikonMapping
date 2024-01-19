$(document).ready(function() {
  $.ajax({
    url: 'gold_standard.json',
    dataType: 'json',
    success: function(data) {
      const dataArray = Object.entries(data).map(([key, value]) => ({ key, ...value }));

      $('#dataTable').DataTable({
        data: dataArray,
        columns: [
          { data: 'key', title: 'Key' },
          { data: 'SaintName', title: 'Saint Name' },
          { data: 'Gender',  title: 'Gender' },
          { data: 'Occupation', title: 'Occupation' },
          { data: 'RawOccupation', title: 'Raw Occupation' },
          { data: 'EntryLength', title: 'Character Length of Entry' },
          { data: 'CanonizationStatus', title: 'Canonization' },
          { data: 'NumberInHlex', title: 'Number in Lexicon' },
          { data: 'FeastDay0', title: 'FeastDay0' },
          { data: 'FeastDay1', title: 'FeastDay1' },
          { data: 'FeastDay2', title: 'FeastDay2' },
          { data: 'RawFeastDay', title: 'Raw Feast Day' },
          { data: 'OriginalText',  title: 'Raw Text from Saints Lexicon'}
          // Add more columns as needed
        ]
      });
    },
    error: function(xhr, status, error) {
      console.error('Error loading JSON file:', error);
    }
  });
});