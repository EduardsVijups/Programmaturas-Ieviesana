const xValues = [100,200,300,400,500,600,700,800,900,1000];

const ctx = document.getElementById('chart');

new Chart(ctx, {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{ 
      data: [870,1140,1060,1060,1070,1110,1330,2210,7830,2478],
      borderColor: "green",
      pointRadius: 2,
<<<<<<< HEAD
      tension: 0.1,
=======
      tension: 0.6,
>>>>>>> feature
    }, { 
      data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000],
      borderColor: "blue",
      pointRadius: 2,
<<<<<<< HEAD
      tension: 0.1,
=======
      tension: 0.6,
>>>>>>> feature
    }, { 
      data: [300,700,2000,5000,6000,4000,2000,1000,200,100],
      borderColor: "green",
      pointRadius: 2,
<<<<<<< HEAD
      tension: 0.1,
=======
      tension: 0.6,
>>>>>>> feature
    }]
  },
  options: {
    plugins: {
      legend: { display: false }
    }
  }
});