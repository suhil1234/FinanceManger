const renderChart = (categoryNames, totalAmounts) => {
    const ctx = document.getElementById('myChart');
    const colors = [ '#43ff64d9', '#e91c33cc'];
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categoryNames,
        datasets: [{
          label: '',
          data: totalAmounts,
          borderWidth: 1,
          backgroundColor: colors.slice(0, categoryNames.length)
        }]
      },
      options: {
        title: {
            display: true,
            text: "full summary",
          },
      }
    });
    };

    
 const renderChart2 = (categoryNames, totalAmounts) => {
      const ctx2 = document.getElementById('myChart2');
      const colors = [ '#43ff64d9', '#e91c33cc'];
      new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: categoryNames,
          datasets: [{
            label: '',
            data: totalAmounts,
            borderWidth: 1,
            backgroundColor: colors.slice(0, categoryNames.length)
          }]
        },
        options: {
          title: {
              display: true,
              text: "full summary",
            },
        }
      });
      };   

const getChartData = () => {
fetch("/dashboard_summary")
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
renderChart2(categoryNames,totalAmounts)
  })
  .catch(error => {
    console.error('Error:', error);
  });

};

document.onload = getChartData();