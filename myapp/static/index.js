// هذا الكود حق الاسئلة اللي جوابه 0و1

document.querySelector(".lang").addEventListener('click', () => {
    window.open('lang', '_self');

})

// document.querySelectorAll(".box").forEach(x => {
//     x.setAttribute("value", "0");
//     x.addEventListener('click', () => {
//         if (x.classList.contains("active")) {
//             x.classList.remove("active")
//             x.setAttribute("value", "-1");

//         }else {
//             x.classList.add("active")
//             x.setAttribute("value", "1");

//         }
//     })
// })

// اراي لتحديد العمر
let ageIndex = [[18, 24, "1"], [25, 29, "2"], [30, 34, "3"], [35, 39, "4"], [40, 44, "5"], [45, 49, "6"], [50, 54, "7"], [55, 59, "8"], [60, 64, "9"], [65, 69, "10"], [70, 74, "11"], [75, 79, "12"], [80, 120, "13"]];

//  اراي فيها جميع الأعمدة بالترتيب كما هو موجود بالمودل 
let col = ['Age', 'Sex', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Stroke', 'HighBP']

// برمجة زر الارسال
document.querySelector(".send").addEventListener('click', (e) => {
    // هذي الاكواد للتحقق من الاخطاء
    let flag = false;
    document.querySelectorAll(".valid").forEach(q => {
        q.classList.remove("error")
        if (["", NaN, "-1", Infinity].includes(q.value) || !q.validity.valid) {
            q.classList.add("error")
            flag = true
        }
    })
    if (flag) {
        popupError()
        return;
    }

    // يجيب بيانات الاسئلة اللي على شكل 0و1 (checkBox)
    let yn = [...document.querySelectorAll(".box")].map(yn => {
        return {
            id: yn.getAttribute("id"),
            value: yn.checked ? 1 : 0,
            col: col.findIndex(x => x == yn.getAttribute("id"))
        }
    })

    // يجيب بيانات الاسئلة اللي على شكل حقل ادخال (input)
    let val = [...document.querySelectorAll(".val")].map(val => {
        return {
            id: val.getAttribute("id"),
            value: val.querySelector("input").value,
            col: col.findIndex(x => x == val.getAttribute("id"))
        }
    })
    // هذا الكود يطلع البي ام اي
    let bmi = [val.splice(val.findIndex(x => x.id == "Weight"), 1)[0], val.splice(val.findIndex(x => x.id == "Height"), 1)[0]];
    bmi[1].value /= 100
    bmi = bmi[0].value / (bmi[1].value * bmi[1].value)
    val.push({ id: "BMI", value: bmi, col: 4 })
    // هذا الكود يحول العمر
    let age = val[val.findIndex(x => x.id == "Age")].value
    age = ageIndex.find(x => {
        return (x[0] <= age && x[1] >= age)
    })[2]
    val[val.findIndex(x => x.id == "Age")].value = age


    // يجيب بيانات الاسئلة اللي على شكل قائمة (select)
    let select = [...document.querySelectorAll(".select")].map(val => {
        return {
            id: val.getAttribute("id"),
            value: val.querySelector("select").value,
            col: col.findIndex(x => x == val.getAttribute("id"))
        }
    })

    // يجمع المتغيرات السابقة بمتغير واحد (data)
    let data = yn.concat(val, select)
    // يسوي ترتيب للمعلومات حسب الاراي الموجودة بداية الكود
    data = data.sort(function (a, b) { return a['col'] - b['col'] });

    // console.log(data)
    // ينسق البيانات عشان نرسلهن للسيرفر (صفحة الفيو views.py)
    data = {
        features_name: JSON.stringify({ array: data.map(x => x.id) }),
        values: JSON.stringify({ array: data.map(x => x.value) }),
        csrfmiddlewaretoken: csrf,

    }




    let formData = new FormData();
    formData.append('features_name', data.features_name);
    formData.append('values', data.values);
    formData.append('csrfmiddlewaretoken', data.csrfmiddlewaretoken);

    fetch("/setp", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(response => {
            popup(response);
        })
        .catch(err => {
            popupError()
        });

})
