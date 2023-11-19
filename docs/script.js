document.addEventListener('DOMContentLoaded', function () {
  fetch('test.csv') // Replace 'data.csv' with your CSV file path
    .then(response => response.text())
    .then(data => {
      const table = document.getElementById('dataTable');
      const rows = data.trim().split('\n');

      rows.forEach(row => {
        const cells = row.split(',');
        const newRow = table.insertRow();

        cells.forEach(cellData => {
          const newCell = newRow.insertCell();
          newCell.textContent = cellData;
        });
      });
    })
    .catch(error => console.error('Error fetching the data:', error));
});