from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from models import Question, Choice, Kinetic
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from Kinetic import AtomicMassTable
from Kinetic.KINEMATICS import KINEMATICS
import json
from django.core.context_processors import csrf
import math
import chartit
from Kinetic import HELIOS
import numpy as np
# Create your views here.

def IndexView(request):
    template_name = 'polls/index.html'
    template = loader.get_template(template_name)

    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    kinetic_data = chartit.DataPool(
        series=[{'options':{'source':Kinetic.objects.all()},
            'terms':['angle','energy',]}]
            )

    kinetic_chart = chartit.Chart(datasource = kinetic_data,
            series_options=
            [{'options':{
                'type':'line',
                'stacking':False},
              'terms':{'angle':['energy']}

                  }],
            chart_options=
                {'title':{'text':'bobo'},
                    'xAxis':{
                        'title':{'text':'angle'}
                }})

    context = RequestContext(request,  {
            'latest_question_list': latest_question_list,
            'error_message': "You didn't select a choice.",
            'kinetic_chart':kinetic_chart,
        })
    context.update(csrf(request))

    template_content = template.render(context)
    return HttpResponse(template_content)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):

    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def ElementFinder(request):
    #print "another bobo"
    json_str = request.body.decode(encoding='UTF-8')
    json_obj = json.loads(json_str)
    #print json_str
    tmpA=-10
    tmpZ=-10;
    for ele in json_obj:

        if ele['name'][0] == 'A':
            try:
                tmpA = int(ele['value'])
            except:
                pass

        if ele['name'][0] == 'Z':
            try:
                tmpZ = int(ele['value'])
            except:
                pass

    #print "another bobo", tmpA," ",tmpZ
    #print AtomicMass.objects.all();
    return_ele = 0
    try:
        return_ele = AtomicMassTable.GetElement(tbjcZ=tmpZ,tbjcA=tmpA)
    except:
        pass
    print return_ele
    return_obj = {}
    if return_ele != None:
        #print return_ele.Name
        return_obj =  {"A":return_ele[1],"Z":return_ele[2],"Mass":return_ele[3],"Name":return_ele[4]}
    #print "I am here?",return_ele
    return_str = json.dumps(return_obj)
    print return_str
    #return_str = "1234"
    return HttpResponse(return_str)

def CalculateCurve(request):

    json_str = request.body.decode(encoding='UTF-8')
    json_obj = json.loads(json_str)

    AList = [0 for i in range(4)]
    ZList = [0 for i in range(4)]
    CList = [0 for i in range(4)]
    massList = [0 for i in range(4)]

    ExList = []
    HELIOS_B= None
    K0 = None

    ArrayRange = None
    ArrayExRange = None

    print json_obj
    for ele in json_obj:
        index = 0
        try:
            index = int(ele['name'][1:])
        except:
            pass

        if ele['name'][0] == 'A' and len(ele['name']) == 2:
            AList[index] = int(ele['value'])

        if ele['name'][0] == 'Z' and len(ele['name']) == 2:
            ZList[index] = int(ele['value'])

        if ele['name'][0] == 'C' and len(ele['name']) == 2:
            CList[index] = int(ele['value'])

        if ele['name'] == "Ex":
            ExList.append(float(ele['value']))

        if ele['name'] == "HELIOS_B":
            HELIOS_B = float(ele['value'])

        if ele['name'] == "K0":
            K0 = float(ele['value'])

        if ele['name'] == "ArrayRangeValues":
            ArrayRange = ele['value']

        if ele['name'] == "ArrayExRangeValues":
            ArrayExRange = ele['value']

    print ArrayRange, ArrayExRange

    for idx in range(4):
        element = AtomicMassTable.GetElement(tbjcZ=ZList[idx],tbjcA=AList[idx])
        try:
            massList[idx] = element[3]
        except:
            pass

    unique_Ex =[]
    [unique_Ex.append(item) for item in ExList if item not in unique_Ex]
    return_list = []
    #print "unique", unique_Ex
    for ex3 in unique_Ex:
        kin = KINEMATICS(m=massList, K0=K0,Eex2 = 0, Eex3 = ex3)
        KList = []
        thetaList = []
        ZPosList = []
        KPlotList = []
        thetaCMSList = []
        for i in np.linspace(1,180,1800*5):
            theta = i*math.pi/180
            kin.calculate(theta,0)

            if 1:#i % 4 == 0:
                #thetaList.append(kin.thetalab3)
                #thetaList.append(math.pi-theta)
                thetaList.append(i)
                KList.append(kin.K3)
            zpostmp = None
            #print kin.V3,kin.thetalab3,ZList[3]

            if kin.K3 > ArrayExRange[0] and kin.K3 <ArrayExRange[1]:
                try:
                    zpostmp=HELIOS.ZPos(kin.V3,kin.thetalab3/180.0*math.pi,CList[3],massList[3],HELIOS_B,arrayradius=0.01)
                   # if zpostmp is None:
                   #     zpostmp = ''
                   # print "zpos:",zpostmp
                except:
                    pass
                if zpostmp is not None and zpostmp >ArrayRange[0] and zpostmp <ArrayRange[1]:
                    KPlotList.append(kin.K3)
                    ZPosList.append(zpostmp)
        total_list = [thetaList,KList]
        totalHELIOS_list = [ZPosList,KPlotList]

        return_list.append([ map(list,zip(*total_list)),map(list,zip(*totalHELIOS_list)) ])

    return_str = json.dumps([return_list,unique_Ex])

    #print "allala", return_str
    return HttpResponse(return_str)
