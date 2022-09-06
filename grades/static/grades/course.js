let courses = document.querySelector('.course')
let button = document.querySelector('.navbtn')
courses.style.display = 'block'
button.addEventListener('click' , () =>{
    
    if (courses.style.display == 'none'){
        courses.style.display = 'block';
        return ;
    }
    if (courses.style.display == 'block'){
        courses.style.display = 'none' ;
        return ;
    }
    // let display = courses.style.display ;
    // console.log(display)
    // if (display == 'block'){
    //     console.log(display)
    //     display = 'none'
    // }
    // if (display == 'none'){
    //     console.log(display)
    //     display = 'block'
    // }
})



