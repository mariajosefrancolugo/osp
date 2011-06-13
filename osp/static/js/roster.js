if (ls_count.auditory > 0 || ls_count.kinesthetic > 0 || ls_count.visual > 0) {
    google.load('visualization', '1', {packages: ['corechart']});
    google.setOnLoadCallback(drawChart);
}

function drawChart() {
    var ls_data = new google.visualization.DataTable();

    ls_data.addColumn('string', 'Style');
    ls_data.addColumn('number', 'Students');
    
    ls_data.addRows(3);
    ls_data.setValue(0, 0, 'Auditory');
    ls_data.setValue(1, 0, 'Kinesthetic');
    ls_data.setValue(2, 0, 'Visual');
    
    ls_data.setValue(0, 1, ls_count.auditory);
    ls_data.setValue(1, 1, ls_count.kinesthetic);
    ls_data.setValue(2, 1, ls_count.visual);
    
    var ls_chart = new google.visualization.BarChart(document.getElementById('class-chart'));
    ls_chart.draw(ls_data, {width: 480, height: 200, legend: 'none', backgroundColor: '#fff'});
}
