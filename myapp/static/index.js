document.querySelectorAll(".box").forEach(x => {
    x.setAttribute("value", "0");
    console.log("x")
    x.addEventListener('click', () => {
        x.classList.toggle("active")
        x.setAttribute("value", "1");
    })
})

document.querySelector(".send").addEventListener('click', (e) => {
    let yn = [...document.querySelectorAll(".box")].map(yn => {
        return {
            id: yn.getAttribute("id"),
            value: yn.getAttribute("value"),
        }
    })
    console.log(yn)

    let val = [...document.querySelectorAll(".val")].map(val => {
        return {
            id: val.getAttribute("id"),
            value: val.querySelector("input").value,
        }
    })
    let bmi = val.splice(2, 2);
    bmi[1].value /= 100
    bmi = bmi[0].value / (bmi[1].value * bmi[1].value)
    val.push({ id: "bmi", value: bmi })
    console.log(val)


    let select = [...document.querySelectorAll(".select")].map(val => {
        return {
            id: val.getAttribute("id"),
            value: val.querySelector("select").value,
        }
    })
    console.log(select)

    let data = yn.concat(val, select)
    data = {
        features_name: data.map(x => x.id),
        values: data.map(x => x.value)
    }
    console.log(data)
    $.ajax({
        url: "/setp",
        type: "get",
        data,
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log("error")
        }
    });



})