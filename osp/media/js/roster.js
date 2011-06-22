if (learning_styles.auditory > 0 || learning_styles.kinesthetic > 0 || learning_styles.visual > 0) {
    google.load('visualization', '1', {packages: ['corechart']});
    google.setOnLoadCallback(drawChart);
}

function drawChart() {
    var learning_styles_data = new google.visualization.DataTable();

    learning_styles_data.addColumn('string', 'Style');
    learning_styles_data.addColumn('number', 'Students');
    
    learning_styles_data.addRows(3);
    learning_styles_data.setValue(0, 0, 'Auditory');
    learning_styles_data.setValue(1, 0, 'Kinesthetic');
    learning_styles_data.setValue(2, 0, 'Visual');
    
    learning_styles_data.setValue(0, 1, learning_styles.auditory);
    learning_styles_data.setValue(1, 1, learning_styles.kinesthetic);
    learning_styles_data.setValue(2, 1, learning_styles.visual);
    
    var learning_styles_chart = new google.visualization.BarChart(document.getElementById('class-chart'));
    learning_styles_chart.draw(learning_styles_data, {width: 480, height: 200, legend: 'none', backgroundColor: '#fff'});
}
