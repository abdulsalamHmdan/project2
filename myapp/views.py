from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView
import joblib
import pandas as pd
import json
# Create your views here.

def home(request):
    my_list = [
            {"id":"HighChol","title":"تعاني من ارتفاع بالكلسترول","icon":""},
              {"id":"CholCheck","title":"عملت فحص كلتسرول بالخمس سنين الماضية","icon":""},
              {"id":"Smoker","title":"مدخن","icon":""},
              {"id":"HeartDiseaseorAttack","title":"لديك امراض قلب","icon":""},
              {"id":"Fruits","title":"تتناول الفواكه يوميا","icon":""},
              {"id":"PhysActivity","title":"هل عملت نشاط حركي خلال الشهر الاخير","icon":""},
              {"id":"Veggies","title":"تتناول الخضار مرة واحدة باليوم على الأقل","icon":""},
              {"id":"DiffWalk","title":"تواجه مشاكل في المشي","icon":""},
              {"id":"Stroke","title":"سبق وتعرضت لجلطة","icon":""},
              {"id":"HighBP","title":"لديك ارتفاع في ضغط الدم","icon":""},
              ]
    
    my_list2 = [
              {"id":"PhysHlth","title":"كم مرة تعرضت لاصابة في جسمك خلال الثلاثين يوم الماضية","placeholder":"1..","max":30,"min":0},
              {"id":"Age","title":"العمر","placeholder":" ","max":110,"min":18},
              {"id":"Weight","title":"الوزن","placeholder":" ","max":200,"min":0},
              {"id":"Height","title":"الطول","placeholder":" ","max":250,"min":0},
              {"id":"MentHlth","title":"كم مر بك يوم سيء لصحتك النفسية خلال الثلاثين يوم الماضية","placeholder":"20..","max":30,"min":0},
              ]
    
    my_list3 = [
              {"id":"GenHlth","title":"قيم صحتك العامة من ١ الى خمسة (١ ممتازة جداً ٥ سيئة جداً)","list":[
                  {"value":1,"title":"1"},
                  {"value":2,"title":"2"},
                  {"value":3,"title":"3"},
                  {"value":4,"title":"4"},
                  {"value":5,"title":"5"},
                  
                  ]},
              {"id":"Sex","title":"الجنس","list":[
                  {"value":1,"title":"ذكر"},
                  {"value":2,"title":"أنثى"},
                  ]},
              ]
    return render(request,"index.html",{'Yn': my_list,'mqaly': my_list2,'select': my_list3})

def setp(request):
    if request.method == "POST":
        # قراءة البيانات المرسلة عبر POST
        features_name = request.POST.get('features_name', None)
        values = request.POST.get('values', None)
        # x = '{"aa":["HighChol","CholCheck","Smoker","HeartDiseahysHlth","Age","MentHlth","bmi","GenHlth","Sex"]}'
        # x1 = features_name
        # y1 = json.loads(x1)
        # print(y1['aa'])
        # x2 = values
        # y2 = json.loads(x2)
        # print(y2['aa'])
        response = HttpResponse('blah')
        response.set_cookie('features_name', features_name)
        response.set_cookie('values', values)
        return response

        # return JsonResponse({"message": "Data received successfully"})        
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

# def setp(request):
#     print(request.POST['features_name'])
#     response = HttpResponse('blah')
#     response.set_cookie('cookie_name', ['aaaaa',"lalla"])
#     return response

class result(TemplateView):
    def get(self,request):
        model = joblib.load('myapp\model_1.pkl')
        features_name = request.COOKIES.get('features_name')
        values = request.COOKIES.get('values')
        col = ['Age', 'Sex', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'HeartDiseaseorAttack', 'PhysActivity','Fruits', 'Veggies','GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Stroke','HighBP']

        x1 = features_name
        y1 = json.loads(x1)
        print(y1)

        x2 = values
        y2 = json.loads(x2)
        # print(y2['aa'][0])

        input_data = pd.DataFrame([y2['aa']], columns=y1['aa'])
        # input_data = pd.DataFrame([y2['aa']], columns=y2['aa'])
        prediction = model.predict(input_data)

        return render(request,"result.html",{"result":int(prediction[0])})
    def post(self,request):
        request.session.setdefault('keys', 0)
        # request.session.setdefault('values', 0)
        # request.session['keys'] = request.POST["features_name"]
        # request.session['values'] = request.POST["values"]
        return HttpResponse("boodone")

