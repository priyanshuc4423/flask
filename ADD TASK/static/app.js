
let open = document.querySelectorAll(".open")
let content = document.querySelectorAll('.container');
let close = document.querySelectorAll(".close");
let value = document.getElementById('text')



open.addEventListener('click',function(){
    content.classList.add('visible');
    Text.innerText = 'CONTENT';
})

close.addEventListener('click',function(){
    content.classList.remove("visible");

})

