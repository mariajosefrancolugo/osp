function refreshVisits(page) {
    $.get(base_url + 'profile/' + student_id + '/all/' + page + '/',
          function(data) {
        $('#visits').fadeOut('fast', function() {
            $(this).html(data);
            $(this).fadeIn('fast');
        });
    });
}

function styleTable(){
    if($('#custom-assessments-body tr:even').hasClass("odd")){
    }else{
        $('#custom-assessments-body tr:even').addClass("odd");
    }
    if($('#custom-assessments-body tr:odd').hasClass("even")){
    }else{
        $('#custom-assessments-body tr:odd').addClass("even");
    }
}

$(function() {

    $('a').click(function(){
        if($(this).attr('href') == '#assessment-results') {
            styleTable();
        }

    });

    $("#profile_menu").tabs({ fx: { opacity: 'toggle', duration: 'fast' } });

    $('#visit-paging a').live('click', function() {
        refreshVisits($(this).data('page'));
    });

    $('#view-note-window').dialog(default_window_options);
    $('#view-visit-window').dialog(default_window_options);

    $('#log-visit-window').dialog(default_window_options);
    $('#log-visit-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#visit-form').serializeArray();
                $.post(base_url + 'visit/' + student_id + '/log/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        refreshVisits(1);
                        $('#log-visit-window').dialog('close');
                        location.reload();
                    } else if(data.status == 'fail') {
                        $('#log-visit-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
            }
        }
    ]);

   $('#note-window').dialog(default_window_options);
   $('#note-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#note-form').serializeArray();
                $.post(base_url + 'note/add/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        refreshVisits(1);
                        $('#note-window').dialog('close');
                        window.location.reload();
                    } else if(data.status == 'fail') {
                        $('#note-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
            }
        }
    ]);

    $('#intervention-window').dialog(default_window_options);
    $('#intervention-window').dialog('option', 'buttons', [
        {
            text: 'Submit',
            click: function() {
                var data = $('#intervention-form').serializeArray();
                $.post(base_url + 'notification/intervene/',
                       data,
                       function(data) {
                    if(data.status == 'success') {
                        $('#intervention-window').dialog('close');
                        location.reload();
                    } else if(data.status == 'fail') {
                        $('#intervention-window').html(data.template);
                        applyNotificationStyles();
                    }
                }, 'json');
            }
        }
    ]);

    $('#log-visit').click(function() {
        $.get(base_url + 'visit/' + student_id + '/log/', function(data) {
            $('#log-visit-window').html(data);
            $('#log-visit-window').dialog('open');
        });
    });

    $('#id-note').click(function() {
        var data = $('#visit_note-form').serializeArray();
        $.get(base_url + 'note/add', data, function(data) {
            $('#note-window').html(data);
            $('#note-window').dialog('open');
        });
    });

    $('#id-intervene').click(function() {
        var data = $('#profile_intervention-form').serializeArray();
        $.get(base_url + 'notification/intervene/', data, function(data) {
            $('#intervention-window').html(data);
            $('#intervention-window').dialog('open');
        });
    });

    $('.view-visit').live('click', function() {
        $.get(base_url + 'visit/' + student_id + '/view/' +
              $(this).data('visit') + '/',
              function(data) {
            $('#view-visit-window').html(data);
            applyNotificationStyles();
            $('#view-visit-window').dialog('open');
        });
    });

    $('.view-note').live('click', function() {
        $.get(base_url + 'note/' + student_id + '/view/' +
              $(this).data('note') + '/',
              function(data) {
            $('#view-note-window').html(data);
            applyNotificationStyles();
            $('#view-note-window').dialog('open');
        });
    });

    $('a.modal').click(function() {
        if($(this).attr('ref') == 'survey-window') {
            $('#survey-window').dialog(default_window_options).load(base_url + 'survey/results/' + $(this).data('result-id') + '/');
            $('#survey-window').dialog('open');
        }
    });

});

function showPersonalityCharts(){$('#personality-type-charts').show();};
function showLearningCharts(){$('#Learning-style-container').show();};

function drawRCharts(){
    var r1 = Raphael("personality-type-chart-1"),
    r2 = Raphael("personality-type-chart-2"),
    r3 = Raphael("personality-type-chart-3"),
    r4 = Raphael("personality-type-chart-4"),
    fin = function (num) {
        var bar_value = num*100;
        bar_value = bar_value.toFixed(0);
        var text_value = bar_value + "%";
        this.flag = this.label(0,50,  text_value || "0").insertBefore(this);
    },
    fout = function () {
        this.flag.animate({opacity: 0}, 300, function () {this.remove();});
    };


    var r1Rect1 = r1.rect(25, 5, 400*personality_type_scores[0][1], 28, 3);
    var r1Rect2 = r1.rect(25+400*personality_type_scores[0][1], 5, (400 - 400*personality_type_scores[0][1]), 28, 3);
    r1Rect1.attr({fill: "#6D95F3", stroke: "#777"});
    r1Rect2.attr({fill: "#CCDAFB", stroke: "#777"});
    var value1 = personality_type_scores[0][1]
    value1 = value1*100;
    value1 = value1.toFixed(0);
    value1 = value1+"%";
    var value2 = personality_type_scores[0][2]
    value2 = value2*100;
    value2 = value2.toFixed(0);
    value2 = value2+"%";

    var r1Text = r1.text(50,25,value1).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
     r1Text = r1.text(400,25,value2).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
     // r1.path("M25, 40L425, 40");
    // r1.text(225,38, "|")

    var r2Rect1 = r2.rect(25, 5, 400*personality_type_scores[1][1], 28, 3);
    var r2Rect2 = r2.rect(25+400*personality_type_scores[1][1], 5, (400 - 400*personality_type_scores[1][1]), 28, 3);
    r2Rect1.attr({fill: "#6D95F3", stroke: "#777"});
    r2Rect2.attr({fill: "#CCDAFB", stroke: "#777"});
    value1 = personality_type_scores[1][1]
    value1 = value1*100;
    value1 = value1.toFixed(0);
    value1 = value1+"%";
    value2 = personality_type_scores[1][2]
    value2 = value2*100;
    value2 = value2.toFixed(0);
    value2 = value2+"%";
    var r2Text = r2.text(50,25,value1).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
    r2Text = r2.text(400,25,value2).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
    //r2.path("M25, 40L425, 40");
    //r2.text(225,38, "|")

    var r3Rect1 = r3.rect(25, 5, 400*personality_type_scores[2][1], 28, 3);
    var r3Rect2 = r3.rect(25+400*personality_type_scores[2][1], 5, (400 - 400*personality_type_scores[2][1]), 28, 3);
    r3Rect1.attr({fill: "#6D95F3", stroke: "#777"});
    r3Rect2.attr({fill: "#CCDAFB", stroke: "#777"});
    value1 = personality_type_scores[2][1]
    value1 = value1*100;
    value1 = value1.toFixed(0);
    value1 = value1+"%";
    value2 = personality_type_scores[2][2]
    value2 = value2*100;
    value2 = value2.toFixed(0);
    value2 = value2+"%";
    var r3Text = r3.text(50,25,value1).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
    r3Text = r3.text(400,25,value2).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
    //r3.path("M25, 40L425, 40");
    //r3.text(225,38, "|")

    var r4Rect1 = r4.rect(25, 5, 400*personality_type_scores[3][1], 28, 3);
    var r4Rect2 = r4.rect(25+400*personality_type_scores[3][1], 5, (400 - 400*personality_type_scores[3][1]), 28, 3);
    r4Rect1.attr({fill: "#6D95F3", stroke: "#777"});
    r4Rect2.attr({fill: "#CCDAFB", stroke: "#777"});
    value1 = personality_type_scores[3][1]
    value1 = value1*100;
    value1 = value1.toFixed(0);
    value1 = value1+"%";
    value2 = personality_type_scores[3][2]
    value2 = value2*100;
    value2 = value2.toFixed(0);
    value2 = value2+"%";
    var r4Text = r4.text(50,25,value1).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
    r4Text = r4.text(400,25,value2).attr({ "font-size": 20, "font-family": "Arial, Helvetica, sans-serif" });;
    //r4.path("M25, 40L425, 40");
    //r4.text(225,38, "|")

    if (personality_type_scores[0][0] == 'E') {
            $('#personality-type-chart-label1 span.left').addClass('highlight');
        } else {
            $('#personality-type-chart-label1 span.right').addClass('highlight');
        }
    if (personality_type_scores[1][0] == 'S') {
            $('#personality-type-chart-label2 span.right').addClass('highlight');
        } else {
            $('#personality-type-chart-label2 span.left').addClass('highlight');
        }
    if (personality_type_scores[2][0] == 'T') {
            $('#personality-type-chart-label3 span.right').addClass('highlight');
        } else {
            $('#personality-type-chart-label3 span.left').addClass('highlight');
        }
    if (personality_type_scores[3][0] == 'J') {
            $('#personality-type-chart-label4 span.left').addClass('highlight');
        } else {
            $('#personality-type-chart-label4 span.right').addClass('highlight');
        }
        showPersonalityCharts();
};

function drawLearningChart(){
    var l1 = Raphael("learningStyleChart"),
    fin = function () {
        var bar_value = this.bar.value*100;
        if (bar_value < 10){
            bar_value = bar_value.toFixed(0);
            var text_value = "Score: "+bar_value;
            this.flag = l1.label(50 , this.bar.y,  text_value || "0").insertBefore(this);
        }
    },
    fout = function () {
        if (this.bar.value*100 < 10){
        this.flag.animate({opacity: 0}, 300, function () {this.remove();});
        }
    };
    //Drawing the x and y axis.
    var x = l1.path("M0 175L270 175");
    var y = l1.path("M0 40L0 175");
    var i = 1;
    while(i<11){

        l1.text(0+(i*27),190,i+"");
        var m = "M"+(i*27)+" 175";
        var l = "L"+(i*27)+" 165"
        l1.path("M"+(i*27)+" 180L"+(i*27)+" 175");
        i++;
    }
    l1.path("M0 180L0 170");
    l1.text(3,190,"0");

    l1.hbarchart(0, 30, 275, 200, [[latest_learning_style_result.auditory_score]/100,[latest_learning_style_result.kinesthetic_score]/100,[latest_learning_style_result.visual_score]/100,[.1]], {type: "soft", "gutter":"40%", colors:['#6D95F3','#6D95F3','#6D95F3']}).hover(fin,fout);

    showLearningCharts();
};