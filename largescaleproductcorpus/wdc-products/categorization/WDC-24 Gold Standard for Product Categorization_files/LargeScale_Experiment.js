const data_experiment = [
  { category: 'Health and Beauty', accuracy: 100 },
  { category: 'Automotive', accuracy: 90 },
  { category: 'Grocery and Gourmet Food', accuracy: 90 },
  { category: 'Musical Instruments', accuracy: 90 },
  { category: 'Shoes', accuracy: 90 },
  { category: 'Toys and Games', accuracy: 90 },
  { category: 'CDs and Vinyl', accuracy: 80 },
  { category: 'Cell Phones and Accessories', accuracy: 80 },
  { category: 'Clothing', accuracy: 80 },
  { category: 'Jewelry', accuracy: 80 },
  { category: 'Movies and TV', accuracy: 80 },
  { category: 'Others', accuracy: 80 },
  { category: 'Video Games', accuracy: 80 },
  { category: 'Books', accuracy: 70 },
  { category: 'Camera and Photo', accuracy: 70 },
  { category: 'Other Electronics', accuracy: 70 },
  { category: 'Pet Supplies', accuracy: 70 },
  { category: 'Home and Garden', accuracy: 60 },
  { category: 'Office Products', accuracy: 60 },
  { category: 'Computers and Accessories', accuracy: 50 },
  { category: 'Luggage and Travel Gear', accuracy: 50 },
  { category: 'Tools and Home Improvement', accuracy: 50 },
  { category: 'Baby', accuracy: 40 },
  { category: 'Sports and Outdoors', accuracy: 30 }
];

const svg_experiment = d3.select('#largescale_experiment')
  .attr('width', 970)
  .attr('height', data_experiment.length * 30 + 120);

const margin_experiment = { top: 60, right: 100, bottom: 80, left: 250 };
const width_experiment = +svg_experiment.attr('width') - margin_experiment.left - margin_experiment.right;
const height_experiment = +svg_experiment.attr('height') - margin_experiment.top - margin_experiment.bottom;

const xScale_experiment = d3.scaleLinear()
  .range([0, width_experiment])
  .domain([0, d3.max(data_experiment, d => d.accuracy)]);

const yScale_experiment = d3.scaleBand()
  .range([0, height_experiment])
  .padding(0.1)
  .domain(data_experiment.map(d => d.category));

const g_experiment = svg_experiment.append('g')
  .attr('transform', `translate(${margin_experiment.left},${margin_experiment.top})`);

const bars_experiment = g_experiment.selectAll('.bar-accuracy')
  .data(data_experiment)
  .enter()
  .append('rect')
  .attr('class', 'bar-accuracy')
  .attr('x', 0)
  .attr('y', d => yScale_experiment(d.category))
  .attr('width', d => xScale_experiment(d.accuracy))
  .attr('height', yScale_experiment.bandwidth())
  .style('fill', (d, i) => {
    const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([data_experiment.length + 4.5 , 1]);
    return colorScale(i);
  });

const labels_accuracy = g_experiment.selectAll('.bar-label-accuracy')
  .data(data_experiment)
  .enter()
  .append('text')
  .attr('class', 'bar-label-accuracy')
  .attr('x', d => xScale_experiment(d.accuracy) + 5)
  .attr('y', d => yScale_experiment(d.category) + yScale_experiment.bandwidth() / 2)
  .attr('text-anchor', 'start')
  .attr('alignment-baseline', 'middle')
  .text(d => `${d.accuracy}%`)
  .style('fill', 'black');

const xAxis_experiment = d3.axisBottom(xScale_experiment)
  .ticks(5)
  .tickFormat(d => d + '%');

g_experiment.append('g')
  .attr('class', 'x-axis')
  .attr('transform', `translate(0, ${height_experiment})`)
  .call(xAxis_experiment)
   .style("font-size", "13px")
  .attr("y", 10);

const yAxis_experiment = d3.axisLeft(yScale_experiment)
  .tickSize(0)
  .tickPadding(10);

g_experiment.append('g')
  .attr('class', 'y-axis-label')
  .call(yAxis_experiment)
  .style("font-size", "13px")
  .attr("y", 10);

// Add x-axis label
svg_experiment.append('text')
  .attr('class', 'x-axis-label')
  .attr('x', width_experiment / 2 + margin_experiment.left)
  .attr('y', height_experiment + margin_experiment.top + 40)
  .attr('text-anchor', 'middle')
  .text('Accuracy (%)')
  .style('font-size', '14px')
  .style('font-weight', 'bold');

// Add y-axis label
svg_experiment.append('text')
  .attr('class', 'y-axis-label')
  .attr('transform', `translate(${margin_experiment.left - 210}, ${margin_experiment.top + height_experiment / 2}) rotate(-90)`)
  .attr('text-anchor', 'middle')
  .text('Category')
  .style('font-size', '14px')
  .style('font-weight', 'bold');

// Add chart title
svg_experiment.append('text')
  .attr('class', 'chart-title')
  .attr('x', width_experiment / 2 + margin_experiment.left)
  .attr('y', margin_experiment.top - 20)
  .attr('text-anchor', 'middle')
  .text('Figure 2: Accuracy per Category Using a Sample Set from WDC Products Corpus Predictions')
  .style('font-size', '16px')
  .style('font-weight', 'bold');

function handleMouseOver() {
  d3.select(this)
    .transition()
    .duration(200)
    .style('fill', 'steelblue');
}

function handleMouseOut() {
  d3.select(this)
    .transition()
    .duration(200)
    .style('fill', (d, i) => {
      const sortedData = data_experiment.slice().sort((a, b) => b.accuracy - a.accuracy);
      const index = sortedData.findIndex(item => item.category === d.category);
      const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([data_experiment.length + 4.5, 1]);
      return colorScale(index);
    });
}

bars_experiment.on('mouseover', handleMouseOver).on('mouseout', handleMouseOut);

// Sort the data in descending order based on accuracy
data_experiment.sort((a, b) => b.accuracy - a.accuracy);

// Update the yScale domain with the sorted data
yScale_experiment.domain(data_experiment.map(d => d.category));

// Update the bars and labels with the sorted data
bars_experiment.data(data_experiment)
  .transition()
  .duration(750)
  .attr('y', d => yScale_experiment(d.category))
  .attr('height', yScale_experiment.bandwidth());

labels_accuracy.data(data_experiment)
  .transition()
  .duration(750)
  .attr('y', d => yScale_experiment(d.category) + yScale_experiment.bandwidth() / 2)
  .text(d => `${d.accuracy}%`);

// Update the y-axis
g_experiment.select('.y-axis')
  .transition()
  .duration(750)
  .call(yAxis_experiment);
