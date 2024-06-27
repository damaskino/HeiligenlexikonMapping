
function openDataset(evt, datasetName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(datasetName).style.display = "block";
  evt.currentTarget.className += " active";
}



$(document).ready(function() {
  $.ajax({
    url: 'gold_standard.json',
    dataType: 'json',
    success: function(data) {
      const dataArray = Object.entries(data).map(([key, value]) => ({ key, ...value }));

      $('#goldStandardTable').DataTable({
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

    $.ajax({
    url: 'parsed_heiligenlexikon.json',
    dataType: 'json',
    success: function(data) {
      const dataArray = Object.entries(data).map(([key, value]) => ({ key, ...value }));

      var table = $('#hlexDataTable').DataTable({
        data: dataArray,
        columns: [
          { data: 'key', title: 'Key' },
          { data: 'SaintName', title: 'Saint Name' },
          { data: 'NumberInHlex', title: 'Number in Lexicon' },
          { data: 'FeastDay0', title: 'FeastDay0', defaultContent:'' },
          { data: 'FeastDay1', title: 'FeastDay1', defaultContent:''  },
          { data: 'FeastDay2', title: 'FeastDay2', defaultContent:''  },
          { data: 'RawFeastDay', title: 'Raw Feast Day', defaultContent:'' },
          { data: 'OriginalText',  title: 'Raw Text from Saints Lexicon'},
          { data: 'Gender',  title: 'Gender' },
          { data: 'EntryLength', title: 'Character Length of Entry' },
          { data: 'CanonizationStatus', title: 'Canonization' }
          //{ data: 'Occupation', title: 'Occupation' },
          //{ data: 'RawOccupation', title: 'Raw Occupation' },
          // Add more columns as needed
        ]
      });
        let searchParams = new URLSearchParams(window.location.search)
        console.log(searchParams)
        if (searchParams.has('id')) {
            var idParam = searchParams.get('id')
            table.search(idParam).draw();
        }
    },
    error: function(xhr, status, error) {
      console.error('Error loading JSON file:', error);
    }
  });
});