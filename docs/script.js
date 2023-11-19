document.addEventListener('DOMContentLoaded', function () {
  fetch('test.json') // Replace 'data.json' with your JSON file path
    .then(response => response.json())
    .then(data => {
      const table = document.getElementById('dataTable');

      // Create table headers from the keys in the first object
      const headers = Object.keys(data[0]);
      const headerRow = table.insertRow();
      headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
      });

      // Populate table with data
      data.forEach(obj => {
        const row = table.insertRow();
        headers.forEach(header => {
          const cell = row.insertCell();
          cell.textContent = obj[header];
        });
      });
    })
    .catch(error => console.error('Error fetching the data:', error));
});