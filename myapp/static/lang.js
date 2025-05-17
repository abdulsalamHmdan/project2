document.querySelectorAll(".box").forEach(box => {
    box.addEventListener('click', () => {
        data = {
            values: box.id,
            csrfmiddlewaretoken: csrf,

        }
        // console.log(data)
        // يرسل البيانات الى السيرفر

        $.ajax({
            url: "/setlan",
            type: "POST",
            data: data,
            success: function (response) { // ينفذ الفنكشن هذي في حال تم ارسال البيانات بنجاح
                window.open('/', '_self');
            },
            error: function (err) {// ينفذ الفنكشن هذي في حال واجه مشكلة في ارسال البيانات
                // console.log(err)
                alert("يوجد مشكلة يرجى المحاولة لاحقا")
            }
        });

    })
})