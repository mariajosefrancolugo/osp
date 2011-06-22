if (learning_style_counts.auditory > 0 || learning_style_counts.kinesthetic > 0 || learning_style_counts.visual > 0) {
    google.load('visualization', '1', {packages: ['corechart']});
    google.setOnLoadCallback(drawChart);
}

function drawChart() {
    var learning_style_counts_data = new google.visualization.DataTable();

    learning_style_counts_data.addColumn('string', 'Style');
    learning_style_counts_data.addColumn('number', 'Students');
    
    learning_style_counts_data.addRows(3);
    learning_style_counts_data.setValue(0, 0, 'Auditory');
    learning_style_counts_data.setValue(1, 0, 'Kinesthetic');
    learning_style_counts_data.setValue(2, 0, 'Visual');
    
    learning_style_counts_data.setValue(0, 1, learning_style_counts.auditory);
    learning_style_counts_data.setValue(1, 1, learning_style_counts.kinesthetic);
    learning_style_counts_data.setValue(2, 1, learning_style_counts.visual);
    
    var learning_style_counts_chart = new google.visualization.BarChart(document.getElementById('class-chart'));
    learning_style_counts_chart.draw(learning_style_counts_data, {width: 480, height: 200, legend: 'none', backgroundColor: '#fff'});
}
