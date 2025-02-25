document.querySelectorAll(".box").forEach(x => {
    x.setAttribute("value", "0");
    // console.log("x")
    x.addEventListener('click', () => {
        if (x.classList.contains("active")) {
            x.classList.remove("active")
            x.classList.add("notsure")
            x.setAttribute("value", "-1");

        } else if (x.classList.contains("notsure")) {
            x.classList.remove("notsure")
            x.setAttribute("value", "0");

        } else {
            x.classList.add("active")
            x.setAttribute("value", "1");

        }
    })
})
