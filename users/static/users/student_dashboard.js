


let inprogress_btn = document.querySelector('.inprogress_btn')
let past_btn = document.querySelector('.past_btn')
let future_btn = document.querySelector('.future_btn')
let inprogress = document.querySelector('.inprogress')
let past = document.querySelector('.past')
let future = document.querySelector('.future')

inprogress_btn.addEventListener('click' , () =>{
    inprogress.style.display = 'block';
    inprogress.style.textAlign = 'left' ;
    past.style.display = 'none';
    future.style.display = 'none' ;
})

past_btn.addEventListener('click' , () =>{
    inprogress.style.display = 'none';
    past.style.display = 'block';
    past.style.textAlign = 'left' ;
    future.style.display = 'none' ;
})

future_btn.addEventListener('click' , () =>{
    inprogress.style.display = 'none';
    past.style.display = 'none';
    future.style.display = 'block' ;
    future.style.textAlign = 'left' ;
})