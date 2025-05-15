from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import joblib
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
import time

my_list = [
    {
        "type": "t2",
        "id": "Weight",
        "en": "Weight (kg)",
        "title": "الوزن (كجم)",
        "placeholder": " ",
        "max": 200,
        "min": 30,
        "hint": "اكتب وزنك بالكيلو، مثلاً: 75",
        "hint_en": "Enter your weight in kilograms, e.g., 75",
    },
    {
        "type": "t2",
        "id": "Height",
        "en": "Height (cm)",
        "title": "الطول (سم)",
        "placeholder": " ",
        "max": 250,
        "min": 120,
        "hint": "اكتب طولك بالسنتيمتر، مثلاً: 170",
        "hint_en": "Enter your height in centimeters, e.g., 170",
    },
    {
        "type": "t2",
        "id": "Age",
        "en": "Age",
        "title": "العمر",
        "placeholder": " ",
        "max": 99,
        "min": 18,
        "hint": "اكتب عمرك الحالي، لازم يكون فوق 18",
        "hint_en": "Enter your current age, must be 18 or older",
    },
    {
        "type": "t3",
        "id": "Sex",
        "en": "Gender",
        "title": "الجنس",
        "list": [
            {"value": 1, "title": "ذكر"},
            {"value": 2, "title": "أنثى"},
        ],
        "hint": "اختر إذا كنت ذكر أو أنثى",
        "hint_en": "Select your gender: male or female",
    },
    {
        "type": "t1",
        "id": "HighChol",
        "en": "Do you suffer from high cholesterol?",
        "title": "هل تعاني من ارتفاع الكوليسترول ؟",
        "icon": "",
        "hint": "هل سبق قالك الطبيب إن نسبة الكوليسترول عندك مرتفعة؟",
        "hint_en": "Has a doctor ever told you that you have high cholesterol?",
    },
    {
        "type": "t1",
        "id": "CholCheck",
        "en": "Have you had a cholesterol test in the past five years?",
        "title": "هل أجريت فحص كوليسترول خلال الخمس سنين الماضية ؟",
        "icon": "",
        "hint": "هل سويت تحليل دم للكوليسترول آخر 5 سنوات؟",
        "hint_en": "Have you had a blood test for cholesterol in the last 5 years?",
    },
    {
        "type": "t1",
        "id": "Smoker",
        "en": "Are you a smoker?",
        "title": "هل أنت مدخن ؟",
        "icon": "",
        "hint": "سواء تدخن بشكل يومي أو أحياناً",
        "hint_en": "Do you smoke regularly or occasionally?",
    },
    {
        "type": "t1",
        "id": "HeartDiseaseorAttack",
        "en": "Do you suffer from heart diseases?",
        "title": "هل تعاني من أمراض القلب ؟",
        "icon": "",
        "hint": "هل عندك أي مشاكل صحية بالقلب زي الذبحة أو ضعف العضلة؟",
        "hint_en": "Do you have any heart conditions like angina or heart failure?",
    },
    {
        "type": "t1",
        "id": "Fruits",
        "en": "Do you eat fruits daily?",
        "title": "هل تتناول الفواكه يوميا ؟",
        "icon": "",
        "hint": "هل عادتك اليومية تشمل فواكه زي تفاحة أو موزة؟",
        "hint_en": "Do you usually eat fruits every day like apples or bananas?",
    },
    {
        "type": "t1",
        "id": "PhysActivity",
        "en": "Have you done any physical activity in the past month?",
        "title": "هل عملت نشاط حركي خلال الشهر الاخير ؟",
        "icon": "",
        "hint": "هل مارست رياضة أو أي مجهود بدني مؤخراً؟",
        "hint_en": "Have you done any physical exercise or activity in the past 30 days?",
    },
    {
        "type": "t1",
        "id": "Veggies",
        "en": "Do you eat vegetables at least once a day?",
        "title": "هل تتناول الخضار مرة واحدة باليوم على الأقل ؟",
        "icon": "",
        "hint": "هل تاكل خضار زي السلطة أو خيار أو جزر يومياً؟",
        "hint_en": "Do you eat vegetables like salad or cucumbers daily?",
    },
    {
        "type": "t1",
        "id": "DiffWalk",
        "en": "Do you have difficulty walking?",
        "title": "هل تواجه مشاكل في المشي ؟",
        "icon": "",
        "hint": "هل تحس بألم أو تعب لما تمشي؟",
        "hint_en": "Do you feel pain or difficulty when walking?",
    },
    {
        "type": "t1",
        "id": "Stroke",
        "en": "Have you ever had a stroke?",
        "title": "هل سبق وتعرضت لجلطة ؟",
        "icon": "",
        "hint": "هل أصبت بجلطة في الدماغ أو القلب من قبل؟",
        "hint_en": "Have you ever had a stroke or mini-stroke?",
    },
    {
        "type": "t1",
        "id": "HighBP",
        "en": "Do you have high blood pressure?",
        "title": "هل لديك ارتفاع في ضغط الدم ؟",
        "icon": "",
        "hint": "هل قالك الطبيب إن ضغطك أعلى من الطبيعي؟",
        "hint_en": "Have you been diagnosed with high blood pressure?",
    },
    {
        "type": "t2",
        "id": "PhysHlth",
        "en": "How many times have you had a physical injury in the past 30 days?",
        "title": "كم مرة تعرضت لاصابة جسدية خلال الثلاثين يوم الماضية",
        "placeholder": "1..",
        "max": 30,
        "min": 0,
        "hint": "اكتب عدد المرات اللي تأذيت فيها جسدياً آخر شهر",
        "hint_en": "Enter how many times you’ve had a physical injury in the last 30 days",
    },
    {
        "type": "t2",
        "id": "MentHlth",
        "en": "How many days have you had poor mental health in the past 30 days?",
        "title": "كم مر بك يوم سيء لصحتك النفسية خلال الثلاثين يوم الماضية",
        "placeholder": "20..",
        "max": 30,
        "min": 0,
        "hint": "كم يوم حسيت فيه بتعب نفسي أو توتر خلال الشهر الماضي؟",
        "hint_en": "How many days did you feel mentally unwell in the past 30 days?",
    },
    {
        "type": "t3",
        "id": "GenHlth",
        "en": "Rate your overall health from 1 to 5 (1 = Excellent, 5 = Very Poor)",
        "title": "قيم صحتك العامة من ١ الى ٥ (١ ممتازة جداً ٥ سيئة جداً)",
        "list": [
            {"value": 1, "title": "1"},
            {"value": 2, "title": "2"},
            {"value": 3, "title": "3"},
            {"value": 4, "title": "4"},
            {"value": 5, "title": "5"},
        ],
        "hint": "قيّم صحتك بشكل عام من ممتازة إلى سيئة جداً",
        "hint_en": "Rate your general health from excellent to very poor",
    },
]

model = joblib.load("myapp/model_old.pkl")


# Create your views here.
def home(request):
    lan = request.COOKIES.get("lan", 0)
    if lan == "en":
        return render(request, "index_en.html", {"questions": my_list})
    elif lan == "ar":
        return render(request, "index.html", {"questions": my_list})
    else:
        return render(request, "lang.html", {"questions": my_list})


# @csrf_exempt
# def app(request):
#     if request.method == "POST":
#         data = request.POST.get("data", None)
#         print(data)
#         return JsonResponse("good response", status=200, safe=False)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def app(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)
        data = body_data.get("arr", None)
        features_name = [
            "Age",
            "Sex",
            "HighChol",
            "CholCheck",
            "BMI",
            "Smoker",
            "HeartDiseaseorAttack",
            "PhysActivity",
            "Fruits",
            "Veggies",
            "GenHlth",
            "MentHlth",
            "PhysHlth",
            "DiffWalk",
            "Stroke",
            "HighBP",
        ]
        input_data = pd.DataFrame([data], columns=features_name)
        # print(input_data)
        prediction = model.predict_proba(input_data)
        # print(prediction[0])
        return JsonResponse(
            {"data": round(prediction[0][1] * 100, 2)}, status=200, safe=False
        )
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def setp(request):
    if request.method == "POST":
        # قراءة البيانات المرسلة عبر POST
        features_name = request.POST.get("features_name", None)
        values = request.POST.get("values", None)
        model = joblib.load("myapp/model_old.pkl")
        x1 = features_name
        x2 = values
        y1 = json.loads(x1)
        y2 = json.loads(x2)
        input_data = pd.DataFrame([y2["array"]], columns=y1["array"])
        prediction = model.predict_proba(input_data)

        response = HttpResponse(round(prediction[0][1] * 100, 2))
        response.set_cookie(
            "features_name",
            features_name,
        )  # max_age=25)
        response.set_cookie(
            "values",
            values,
        )  # max_age=25)
        return response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def setlan(request):
    if request.method == "POST":
        # قراءة البيانات المرسلة عبر POST
        values = request.POST.get("values", None)
        response = HttpResponse("lan")
        response.set_cookie("lan", values)
        return response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def result(request):
    # model = joblib.load("myapp/model_1.pkl")
    model = joblib.load("myapp/model_old.pkl")
    features_name = request.COOKIES.get("features_name", None)
    values = request.COOKIES.get("values", None)
    if features_name == None or values == None:
        return redirect("home")
    x1 = features_name
    x2 = values
    y1 = json.loads(x1)
    y2 = json.loads(x2)
    input_data = pd.DataFrame([y2["array"]], columns=y1["array"])
    prediction = model.predict_proba(input_data)
    print(prediction[0])
    lan = request.COOKIES.get("lan", 0)
    if lan == "en":
        return render(
            request, "result_en.html", {"result": round(prediction[0][1] * 100, 2)}
        )
    else:
        return render(
            request, "result.html", {"result": round(prediction[0][1] * 100, 2)}
        )


def lang(request):
    return render(request, "lang.html")


# class result(TemplateView):
#     def get(self, request):
#         model = joblib.load("myapp/model_1.pkl")
#         features_name = request.COOKIES.get("features_name", None)
#         values = request.COOKIES.get("values", None)
#         if features_name == None or values == None:
#             return redirect("home")
#         x1 = features_name
#         x2 = values
#         y1 = json.loads(x1)
#         y2 = json.loads(x2)
#         input_data = pd.DataFrame([y2["array"]], columns=y1["array"])
#         prediction = model.predict(input_data)
#         return render(request, "result.html", {"result": int(prediction[0])})
