
$(document).ready(function(){

    SetKineticChart('');

    $( ".ArrayRange .ArrayRange-slider" ).slider({
        range: true,
        min: -100,
        max: 100,
        values: [-100, 100 ],
        slide: function( event, ui ) {
            $( ".ArrayRange-display" ).text( ui.values[ 0 ] + " to " + ui.values[ 1 ] );
        }});

    $(".ArrayRange .ArrayRange-display").text($( ".ArrayRange .ArrayRange-slider" ).slider("values")[0]+" to "+$( ".ArrayRange .ArrayRange-slider" ).slider("values")[1]);
    //
    $( ".ArrayExRange .ArrayExRange-slider" ).slider({
        range: true,
        min: -1,
        max: 30,
        values: [-1, 10 ],
        slide: function( event, ui ) {
            $( ".ArrayExRange-display" ).text( ui.values[ 0 ] + " to " + ui.values[ 1 ] );
        }});

    $(".ArrayExRange .ArrayExRange-display").text($( ".ArrayExRange .ArrayExRange-slider" ).slider("values")[0]+" to "+$( ".ArrayExRange .ArrayExRange-slider" ).slider("values")[1]);
    //
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
    });

    $('.mass_div input[name=A0]').val(20);
    $('.mass_div input[name=Z0]').val(10);
    $('.mass_div input[name=A1]').val(2);
    $('.mass_div input[name=Z1]').val(1);

    $('.mass_div input[name=A2]').val(21);
    $('.mass_div input[name=Z2]').val(10);
    $('.mass_div input[name=A3]').val(1);
    $('.mass_div input[name=Z3]').val(1);

    $('.mass_div .A').each(function(){
        SetNameAndMass($(this));
        var z_tmp = $(this).parent().children(".Z").val();
        $(this).parent().children(".C").val(z_tmp);
    });

    ////////////////////////////////////////////////
    /////////////////form button function///////////
    ////////////////////////////////////////////////

    $("#kinetic_btn").bind('click',function(){

        var formdata_tmp = [];

        var ArrayRangeValues = $(".ArrayRange .ArrayRange-slider" ).slider("values");
        var ArrayExRangeValues = $(".ArrayExRange .ArrayExRange-slider" ).slider("values");
        formdata_tmp.push({'name':'ArrayRangeValues','value':ArrayRangeValues});
        formdata_tmp.push({'name':'ArrayExRangeValues','value':ArrayExRangeValues});

        $('.mass_div input').each(function(){
            formdata_tmp.push({'name':$(this).prop('name'),'value':$(this).prop('value')});
        });

        $('.input_para input').each(function(){
            formdata_tmp.push({'name':$(this).prop('name'),'value':$(this).prop('value')});
        });

        $(".scrollContent tr td").each(function(){
            formdata_tmp.push({'name':'Ex','value':$(this).text()});
        });

        console.log(formdata_tmp);

        $.ajax({type:"POST",
            url:"CalculateCurve",
            contentType:"application/json",
            data:JSON.stringify(formdata_tmp),
            success:function(data)
        {
            var obj = $.parseJSON(data);

            var len = obj[0].length;

            var chart1 = $('#chart_container1').highcharts();
            while(chart1.series.length>0)
            chart1.series[0].remove(true);

        var chart2 = $('#chart_container2').highcharts();
        while(chart2.series.length>0)
            chart2.series[0].remove(true);

        for(i=0;i<len;i++)
        {

            chart1.addSeries({
                name: obj[1][i].toString(),
                data:obj[0][i][0],
                marker: { radius: 2 },
                lineWidth:0
            });

            chart2.addSeries({
                name: obj[1][i].toString(),
                data:obj[0][i][1],
                lineWidth:0,
                marker: { radius: 2 },

            });
        }

        $('#chart_container2').highcharts().xAxis[0].setExtremes($( ".ArrayRange .ArrayRange-slider" ).slider("values")[0],$( ".ArrayRange .ArrayRange-slider" ).slider("values")[1]);

        $('#chart_container2').highcharts().yAxis[0].setExtremes($( ".ArrayExRange .ArrayExRange-slider" ).slider("values")[0],$( ".ArrayExRange .ArrayExRange-slider" ).slider("values")[1]);
        }

        });

    });

    ////////////////////////////////////////////////
    /////////////////input keyup function///////////
    ////////////////////////////////////////////////

    $(".mass_div input").bind('keyup',function(){
        SetNameAndMass($(this));
        if($(this).prop('name')[0]=='C') return;
        var z_tmp = $(this).parent().children(".Z").val();
        $(this).parent().children(".C").val(z_tmp);
    });

    ////////////////////////////////////////////////
    /////////////////ex form  selected//////////////
    ////////////////////////////////////////////////

    $(".ExContainer tr").click(function(){

        SetSelectedItemBKColor($(this));
    });

    ////////////////////////////////////////////////
    /////////////////ex form  function//////////////
    ////////////////////////////////////////////////

    $("#AddEx").click(function(){
        var NewEx = prompt("Please enter an excitation energy",'0');
        var NewElement = "<tr><td>"+NewEx+"</td></tr>";
        $(NewElement).appendTo(".scrollContent").click(function(){SetSelectedItemBKColor($(this));});
        //   $(".scrollContent").append("<tr><td>0</td></tr>" );

    });

    $("#DeleteEx").click(function(){
        $(".scrollContent .RowSelected").remove();
    });

});

function SetNameAndMass(it)
{
    var A_name = it.parent().children(".A").prop('name');
    var A_input = it.parent().children(".A").val();
    var Z_input = it.parent().children(".Z").val();
    formdata=[ {'name':"Z",'value':Z_input},{'name':"A",'value':A_input} ];
    var parentform = it.parent().parent();
    $.ajax({type:"POST",
        url:"ElementFinder",
        contentType:"application/json",
        data:JSON.stringify(formdata),
        success:function(data)
    {

        var obj = $.parseJSON(data);
        var tmpname = obj.Name;
        var tmpA = obj.A;
        var tmpZ = obj.Z;
        return_str = tmpA + tmpname + tmpZ;
        //alert(parentform.prop('class')+parentform.prop('tagName'));

        parentform.children(".left").children(".element").text(return_str);
        var tmpMass = obj.Mass;
        Mass_str = tmpMass+'u';
        parentform.children(".right").children(".result").text(Mass_str);
    }

    });

}

function SetSelectedItemBKColor(it)
{ it.toggleClass("RowSelected");
}
function SetKineticChart(data)
{

    $('#chart_container1').highcharts({

        title: {
            text: 'Lab theta 3 vs Kinetic energy'
        },

        subtitle: {
            text: 'Data input from CSV'
        },

        tooltip: {
            shared: true,
        crosshairs: true
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true
                }
            }
        },

        series: []
    });

    $('#chart_container2').highcharts({

        title: {
            text: 'Position vs Kinetic Energy for Particle 3'
        },

        subtitle: {
            text: 'Data input from CSV'
        },

        tooltip: {
            shared: true,
        crosshairs: true
        },

        yAxis: {min:-1,max:10},

        plotOptions: {
            series: {
                marker: {
                    enabled: true
                }
            }
        },

        series: []
    });
};
