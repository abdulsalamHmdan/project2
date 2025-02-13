document.querySelectorAll(".box").forEach(x => {
    x.setAttribute("value", "0");
    // console.log("x")
    x.addEventListener('click', () => {
        x.classList.toggle("active")
        x.setAttribute("value", "1");
    })
})
