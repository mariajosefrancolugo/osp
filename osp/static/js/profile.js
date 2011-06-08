function visit_paging(page) {
    $.ajax({
        url: base_url + 'visit/' + student + '/page/' + page + '/',
        success: function(data) {
            $("div#visits-animate").fadeOut('fast', function() {
                    $("div#visits-animate").html(data);
                });
            $("div#visits-animate").fadeIn('fast', function() {
                $("div#visit-paging a").each(function(index) {
                    $(this).click(function() {
                        visit_paging($(this).attr("page"));
                    });
                });
            });
        }
    });
}

$(function() {
    $("div#visit-paging a").each(function(index) {
        $(this).click(function() {
            visit_paging($(this).attr("page"));
        });
    });

    var window_options = {
      autoOpen: false,
      height: 500,
      width: 750,
      modal: true,
      resizable: false
    }

    $('a.modal').each(function() {
      if($(this).attr('ref') == 'ls-window') {
        $('#ls-window').dialog(window_options).load(base_url + 'assessment/learning-style/results/' + latest_lsa_result.id + '/');
      } else if($(this).attr('ref') == 'pt-window') {
        $('#pt-window').dialog(window_options).load(base_url + 'assessment/personality-type/results/' + latest_pta_result_id + '/');
      } else if($(this).attr('ref') == 'survey-window') {
        $('#survey-window').dialog(window_options).load(base_url + 'survey/results/' + $(this).data('result-id') + '/');
      }
    });

    $('a.modal').click(function() {
        $('#' + $(this).attr('ref')).dialog('open');
    });
});

if (latest_pta_result_id !== '' && latest_lsa_result.id !== '') {
    google.load('visualization', '1', {packages: ['corechart']});
    google.setOnLoadCallback(drawCharts);

    function drawCharts() {
        if (latest_pta_result_id !== '') {
            // Extraverted/Introverted Chart
            var pt_data_1 = new google.visualization.DataTable();

            pt_data_1.addColumn('string', 'Category');
            pt_data_1.addColumn('number', 'Score');

            pt_data_1.addRows(2);
            pt_data_1.setValue(0, 0, 'Extraverted');
            pt_data_1.setValue(1, 0, 'Introverted');

            if (pt_scores[0][0] == 'E') {
                pt_data_1.setValue(0, 1, pt_scores[0][1]);
                pt_data_1.setValue(1, 1, pt_scores[0][2]);
            } else {
                pt_data_1.setValue(0, 1, pt_scores[0][2]);
                pt_data_1.setValue(1, 1, pt_scores[0][1]);
            }

            var pt_chart_1 = new google.visualization.PieChart(document.getElementById('personality-type-chart-1'));
            pt_chart_1.draw(pt_data_1, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});

            // Sensing/Intuitive Chart
            var pt_data_2 = new google.visualization.DataTable();

            pt_data_2.addColumn('string', 'Category');
            pt_data_2.addColumn('number', 'Score');

            pt_data_2.addRows(2);
            pt_data_2.setValue(0, 0, 'Sensing');
            pt_data_2.setValue(1, 0, 'Intuitive');

            if (pt_scores[1][0] == 'S') {
                pt_data_2.setValue(0, 1, pt_scores[1][1]);
                pt_data_2.setValue(1, 1, pt_scores[1][2]);
            } else {
                pt_data_2.setValue(0, 1, pt_scores[1][2]);
                pt_data_2.setValue(1, 1, pt_scores[1][1]);
            }

            var pt_chart_2 = new google.visualization.PieChart(document.getElementById('personality-type-chart-2'));
            pt_chart_2.draw(pt_data_2, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});

            // Thinking/Feeling Chart
            var pt_data_3 = new google.visualization.DataTable();

            pt_data_3.addColumn('string', 'Category');
            pt_data_3.addColumn('number', 'Score');

            pt_data_3.addRows(2);
            pt_data_3.setValue(0, 0, 'Thinking');
            pt_data_3.setValue(1, 0, 'Feeling');

            if (pt_scores[2][0] == 'T') {
                pt_data_3.setValue(0, 1, pt_scores[2][1]);
                pt_data_3.setValue(1, 1, pt_scores[2][2]);
            } else {
                pt_data_3.setValue(0, 1, pt_scores[2][2]);
                pt_data_3.setValue(1, 1, pt_scores[2][1]);
            }

            var pt_chart_3 = new google.visualization.PieChart(document.getElementById('personality-type-chart-3'));
            pt_chart_3.draw(pt_data_3, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});

            // Judging/Perceiving Chart
            var pt_data_4 = new google.visualization.DataTable();

            pt_data_4.addColumn('string', 'Category');
            pt_data_4.addColumn('number', 'Score');

            pt_data_4.addRows(2);
            pt_data_4.setValue(0, 0, 'Judging');
            pt_data_4.setValue(1, 0, 'Perceiving');

            if (pt_scores[3][0] == 'J') {
                pt_data_4.setValue(0, 1, pt_scores[3][1]);
                pt_data_4.setValue(1, 1, pt_scores[3][2]);
            } else {
                pt_data_4.setValue(0, 1, pt_scores[3][2]);
                pt_data_4.setValue(1, 1, pt_scores[3][1]);
            }

            var pt_chart_4 = new google.visualization.PieChart(document.getElementById('personality-type-chart-4'));
            pt_chart_4.draw(pt_data_4, {width: 175, height: 175, legend: 'bottom', backgroundColor: '#ededee'});
        }

        if (latest_lsa_result.id !== '') {
            // Learning Styles Chart
            var ls_data = new google.visualization.DataTable();

            // Data table columns
            ls_data.addColumn('string', 'Style');
            ls_data.addColumn('number', 'Score');

            // Data table rows
            ls_data.addRows(3);
            ls_data.setValue(0, 0, 'Auditory');
            ls_data.setValue(1, 0, 'Kinesthetic');
            ls_data.setValue(2, 0, 'Visual');

            // Add learning style scores to data table
            ls_data.setValue(0, 1, latest_lsa_result.auditory_score);
            ls_data.setValue(1, 1, latest_lsa_result.kinesthetic_score);
            ls_data.setValue(2, 1, latest_lsa_result.visual_score);

            // Draw bar chart for learning style
            var ls_chart = new google.visualization.BarChart(document.getElementById('learning-style-chart'));
            ls_chart.draw(ls_data, {width: 400, height: 200, legend: 'none', backgroundColor: '#ededee'});
        }
    }
}
