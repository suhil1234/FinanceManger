const renderChart = (categoryNames, totalAmounts) => {
    const ctx = document.getElementById('myChart');
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categoryNames,
        datasets: [{
          label: '',
          data: totalAmounts,
          borderWidth: 1
        }]
      },
      options: {
        title: {
            display: true,
            text: "Expenses per category",
          },
      }
    });
    };

const getChartData = () => {
fetch("/expenses/expenses_summary")
  .then(response => response.json())
  .then(data => {

    const categoryNames = [];
    const totalAmounts = [];

    // Extract the category names and total amounts
    for (const [categoryName, totalAmount] of Object.entries(data)) {
      categoryNames.push(categoryName);
      totalAmounts.push(totalAmount);
    }
renderChart(categoryNames,totalAmounts)
  })
  .catch(error => {
    console.error('Error:', error);
  });

};

document.onload = getChartData();