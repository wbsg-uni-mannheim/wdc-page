const data = [
  { category: "Clothing", offers: 16.95, clusters: 17.57 },
  { category: "Home and Garden", offers: 13.47, clusters: 13.55 },
  { category: "Sports and Outdoors", offers: 8.59, clusters: 8.64 },
  { category: "Office Products", offers: 6.10, clusters: 6.15 },
  { category: "Jewelry", offers: 5.97, clusters: 6.06 },
  { category: "Tools and Home_Improvement", offers: 5.43, clusters: 5.57 },
  { category: "Health and Beauty", offers: 4.78, clusters: 4.39 },
  { category: "Automotive", offers: 4.28, clusters: 4.31 },
  { category: "Toys and Games", offers: 4.22, clusters: 4.11 },
  { category: "Books", offers: 3.95, clusters: 3.90 },
  { category: "Shoes", offers: 3.73, clusters: 3.78 },
  { category: "Grocery and Gourmet_Food", offers: 3.64, clusters: 3.52 },
  { category: "Other Electronics", offers: 2.76, clusters: 2.71 },
  { category: "Computers and Accessories", offers: 2.78, clusters: 2.59 },
  { category: "Pet Supplies", offers: 2.18, clusters: 2.13 },
  { category: "Luggage and Travel_Gear", offers: 1.98, clusters: 2.03 },
  { category: "Musical Instruments", offers: 1.93, clusters: 1.91 },
  { category: "Baby", offers: 1.61, clusters: 1.61 },
  { category: "Cell Phones and Accessories", offers: 1.52, clusters: 1.51 },
  { category: "CDs and Vinyl", offers: 1.44, clusters: 1.40 },
  { category: "Camera and Photo", offers: 1.19, clusters: 1.13 },
  { category: "Others", offers: 0.84, clusters: 0.76 },
  { category: "Video Games", offers: 0.40, clusters: 0.41 },
  { category: "Movies and TV", offers: 0.26, clusters: 0.25 }
];

const svg = d3.select("#dynamic_barchart")
  .attr("width", 970)
  .attr("height", 990);

const margin = { top: 40, right: 100, bottom: 80, left: 250 }; // Adjusted left margin
const width = +svg.attr("width") - margin.left - margin.right;
const height = +svg.attr("height") - margin.top - margin.bottom;

const x = d3.scaleLinear()
  .range([0, width])
  .domain([0, d3.max(data, d => d.offers)]);

const y = d3.scaleBand()
  .range([0, height])
  .padding(0.1)
  .domain(data.map(d => d.category));

const g = svg.append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);

let bars = g.selectAll(".bar")
  .data(data)
  .enter()
  .append("g")
  .attr("class", "bar")
  .attr("transform", d => `translate(0, ${y(d.category)})`);

bars.append("rect")
  .attr("class", "bar-rect")
  .attr("x", 0)
  .attr("y", 0)
  .attr("width", d => x(d.offers))
  .attr("height", y.bandwidth())
  .style("fill", (d, i) => {
    const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([data.length + 4.5, 1]);
    return colorScale(i);
  })
  .on("mouseover", handleMouseOver)
  .on("mouseout", handleMouseOut);

bars.append("text")
  .attr("class", "bar-label")
  .attr("x", d => x(d.offers) + 5)
  .attr("y", y.bandwidth() / 2)
  .attr("alignment-baseline", "middle")
  .text(d => `${d.offers}%`);

g.append("g")
  .attr("class", "axis x-axis")
  .attr("transform", `translate(0, ${height})`)
  .call(d3.axisBottom(x).tickFormat(d => `${d}%`).ticks(5))
  .selectAll("text")
  .style("font-size", "13px")
  .attr("y", 10);
  
  
  // Adjust the y position of the x-axis labels
g.append("g")
  .attr("class", "axis y-axis")
  .call(d3.axisLeft(y))
  .selectAll("text")
  .style("font-size", "13px") // Adjusted font size of y-axis labels
  .attr("x", -50); // Adjust the x position of the y-axis labels

// Add x-axis label
svg.append("text")
  .attr("class", "x-axis-label")
  .attr("x", width / 2 + margin.left)
  .attr("y", height + margin.top + 50) // Adjust the y position of the x-axis label
  .attr("text-anchor", "middle")
  .text("Distribution %")
  .style("font-size", "15px")
  .style('font-weight', 'bold');

// Add y-axis label
const yAxisTitle = svg.append("text")
  .attr("class", "y-axis-label")
  .attr("transform", `translate(${margin.left - 210}, ${margin.top + height / 2}) rotate(-90)`) // Adjusted position and rotation
  .attr("text-anchor", "middle")
  .text("Category")
  .style("font-size", "15px")
  .style('font-weight', 'bold');

// Add chart title
const chartTitle = svg.append("text")
  .attr("class", "chart-title")
  .attr("x", width / 2 + margin.left)
  .attr("y", margin.top - 10) // Adjust the y position of the chart title
  .attr("text-anchor", "middle")
  .style("font-size", "16px")
  .style("font-weight", "bold");

// Update the chart title based on the selected KPI
function updateChartTitle(selectedKPI) {
  const kpiLabel = selectedKPI === "offers" ? "Offers" : "Clusters";
  chartTitle.text(`Figure 1: Distribution % of ${kpiLabel} per Category`);
}

// Update the color order based on the selected KPI
function updateColorOrder(selectedKPI) {
  bars.selectAll(".bar-rect")
    .style("fill", (d, i) => {
      const sortedData = data.slice().sort((a, b) => b[selectedKPI] - a[selectedKPI]);
      const index = sortedData.findIndex(item => item.category === d.category);
      const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([data.length + 4.5 ,1]);
      return colorScale(index).darker(1.4);
    });

  // Update the y-axis title dynamically
  const kpiLabel = selectedKPI === "offers" ? "Offers" : "Clusters";
  yAxisTitle.text(`Category`);
}

// Handle KPI select change event
const kpiSelect = document.getElementById("kpi-select");
kpiSelect.addEventListener("change", handleKPISelectChange);

function handleKPISelectChange() {
  const selectedKPI = kpiSelect.value;

  const sortedData = data.slice().sort((a, b) => b[selectedKPI] - a[selectedKPI]);

  y.domain(sortedData.map(d => d.category));

  bars = g.selectAll(".bar")
    .data(sortedData, d => d.category)
    .order();

  bars.transition()
    .duration(750)
    .attr("transform", d => `translate(0, ${y(d.category)})`);

  bars.select(".bar-rect")
    .transition()
    .duration(750)
    .attr("width", d => x(d[selectedKPI]));

  bars.select(".bar-label")
    .transition()
    .duration(750)
    .attr("x", d => x(d[selectedKPI]) + 5)
    .text(d => `${d[selectedKPI]}%`);

  g.select(".axis.y-axis")
    .transition()
    .duration(750)
    .call(d3.axisLeft(y));

  updateChartTitle(selectedKPI);
  updateColorOrder(selectedKPI);
}

function handleMouseOver() {
  d3.select(this)
    .transition()
    .duration(200)
    .style("fill", "steelblue");
}

function handleMouseOut() {
  d3.select(this)
    .transition()
    .duration(200)
    .style("fill", (d, i) => {
      const sortedData = data.slice().sort((a, b) => b.offers - a.offers);
      const index = sortedData.findIndex(item => item.category === d.category);
      const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([data.length + 4.5, 1]);
      return colorScale(index);
    });
}

// Initial setup
handleKPISelectChange();
