from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
import joblib
import pandas as pd
import json
from mysite.settings import BASE_DIR


# Create your views here.
def home(request):
    my_list = [
        {
            "type": "t2",
            "id": "Weight",
            "title": "الوزن",
            "placeholder": " ",
            "max": 200,
            "min": 30,
        },
        {
            "type": "t2",
            "id": "Height",
            "title": "الطول",
            "placeholder": " ",
            "max": 250,
            "min": 120,
        },
        {
            "type": "t2",
            "id": "Age",
            "title": "العمر",
            "placeholder": " ",
            "max": 99,
            "min": 15,
        },
        {
            "type": "t3",
            "id": "Sex",
            "title": "الجنس",
            "list": [
                {"value": 1, "title": "ذكر"},
                {"value": 2, "title": "أنثى"},
            ],
        },
        {
            "type": "t1",
            "id": "HighChol",
            "title": "هل تعاني من ارتفاع الكوليسترول ؟",
            "icon": "",
        },
        {
            "type": "t1",
            "id": "CholCheck",
            "title": "هل أجريت فحص كوليسترول خلال الخمس سنين الماضية ؟",
            "icon": "",
        },
        {"type": "t1", "id": "Smoker", "title": "هل أنت مدخن ؟", "icon": ""},
        {
            "type": "t1",
            "id": "HeartDiseaseorAttack",
            "title": "هل تعاني من أمراض القلب ؟",
            "icon": "",
        },
        {"type": "t1", "id": "Fruits", "title": "هل تتناول الفواكه يوميا ؟", "icon": ""},
        {
            "type": "t1",
            "id": "PhysActivity",
            "title": "هل عملت نشاط حركي خلال الشهر الاخير ؟",
            "icon": "",
        },
        {
            "type": "t1",
            "id": "Veggies",
            "title": "هل تتناول الخضار مرة واحدة باليوم على الأقل ؟",
            "icon": "",
        },
        {"type": "t1", "id": "DiffWalk", "title": "هل تواجه مشاكل في المشي ؟", "icon": ""},
        {"type": "t1", "id": "Stroke", "title": "هل سبق وتعرضت لجلطة ؟", "icon": ""},
        {"type": "t1", "id": "HighBP", "title": "هل لديك ارتفاع في ضغط الدم ؟", "icon": ""},
        {
            "type": "t2",
            "id": "PhysHlth",
            "title": "كم مرة تعرضت لاصابة جسدية خلال الثلاثين يوم الماضية",
            "placeholder": "1..",
            "max": 30,
            "min": 0,
        },
        {
            "type": "t2",
            "id": "MentHlth",
            "title": "كم مر بك يوم سيء لصحتك النفسية خلال الثلاثين يوم الماضية",
            "placeholder": "20..",
            "max": 30,
            "min": 0,
        },
        {
            "type": "t3",
            "id": "GenHlth",
            "title": "قيم صحتك العامة من ١ الى ٥ (١ ممتازة جداً ٥ سيئة جداً)",
            "list": [
                {"value": 1, "title": "1"},
                {"value": 2, "title": "2"},
                {"value": 3, "title": "3"},
                {"value": 4, "title": "4"},
                {"value": 5, "title": "5"},
            ],
        },
    ]
    return render(request, "index.html", {"questions": my_list})


def setp(request):
    if request.method == "POST":
        # قراءة البيانات المرسلة عبر POST
        features_name = request.POST.get("features_name", None)
        values = request.POST.get("values", None)
        response = HttpResponse("success")
        response.set_cookie("features_name", features_name, max_age=25)
        response.set_cookie("values", values, max_age=25)
        return response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


class result(TemplateView):
    def get(self, request):
        # print(BASE_DIR)
        model = joblib.load("myapp/model_1.pkl")
        features_name = request.COOKIES.get("features_name", None)
        values = request.COOKIES.get("values", None)
        if features_name == None or values == None:
            return redirect("home")
        x1 = features_name
        x2 = values
        y1 = json.loads(x1)
        y2 = json.loads(x2)
        input_data = pd.DataFrame([y2["array"]], columns=y1["array"])
        prediction = model.predict(input_data)
        return render(request, "result.html", {"result": int(prediction[0])})

    def post(self, request):
        return HttpResponse("boodone")
