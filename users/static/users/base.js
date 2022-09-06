let btn = document.querySelector('.dropdown_btn');

btn.addEventListener('click' , () => {
    if (btn.className == 'dropdown_btn'){
        let dropdown = document.querySelector('.dropdown');
        dropdown.style.display = 'block';
        btn.className = 'dropdown_btn2';
        btn.style.border = 'none' ;
        btn.style.backgroundColor =  'rgb(12, 8, 36)';
        btn.style.color = 'white' ;
    }
    else if (btn.className == 'dropdown_btn2'){
        let dropdown = document.querySelector('.dropdown')
        dropdown.style.display = 'none'
        btn.className = 'dropdown_btn';
        btn.style.border = 'none' ;
        btn.style.backgroundColor =  'rgb(12, 8, 36)';
        btn.style.color = 'white' ;
    }
})