from django.shortcuts import render,HttpResponse
from django.views.generic import TemplateView
import joblib
import pandas as pd

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

def result(request):
    value = request.COOKIES.get('data')
    print(value)
    model = joblib.load('myapp\model_1.pkl')

    features_name = ['Age', 'Sex', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'HeartDiseaseorAttack', 'PhysActivity',
                    'Fruits', 'Veggies','GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Stroke',
                    'HighBP']

    input_data = pd.DataFrame([[4, 1, 0,1,26, 0, 0, 1, 0, 1, 3,5, 30, 0, 0, 1]], columns=features_name)
    prediction = model.predict(input_data)

    return render(request,"result.html",{"result":int(prediction[0])})

def setp(request):
    # request.session.setdefault('how_many_visits', 0)
    # request.session['how_many_visits'] += 1
    # print(request.session['how_many_visits'])
    data = request.GET.getlist('features_name',default=None)
    print(data)
    
    return render(request,"result.html")







# class result(TemplateView):
#     def get(self ,request):
#         model = joblib.load('myapp\model_1.pkl')

#         features_name = ['Age', 'Sex', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'HeartDiseaseorAttack', 'PhysActivity',
#                         'Fruits', 'Veggies','GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Stroke',
#                         'HighBP']

#         input_data = pd.DataFrame([[4, 1, 0,1,26, 0, 0, 1, 0, 1, 3,5, 30, 0, 0, 1]], columns=features_name)
#         prediction = model.predict(input_data)

#         print("Prediction:\n", int(prediction[0]))
#         return render(request,"result.html",{"result":int(prediction[0])})