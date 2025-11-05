let Bar=document.getElementById("bar");
let emoji=document.getElementById("basis_r")
let Catagories=document.getElementById("ct");
let closBar=document.getElementById("close_bar");

let Man=document.getElementById("man")
let UnorderList=document.getElementById("uol")
let Dopedowm1=document.getElementById("dopdowm1")

let woMan=document.getElementById("women")
let Dopedowm2=document.getElementById("dopdowm2")

let Jualary=document.getElementById("juwelry")
let Dopedowm3=document.getElementById("dopdowm3")

let LI=document.querySelectorAll('.l1');
let catagoriz_text=document.querySelector('section div div ul');
let carousel=document.querySelector('#default-carousel');

if (window.innerWidth<768){
    UnorderList.classList.add('hidden')
}
Bar.addEventListener('click',function(){
    UnorderList.classList.remove('hidden')
    UnorderList.classList.add('flex-col')
    UnorderList.style.paddingLeft="10px"
    Bar.classList.add('hidden')
    closBar.classList.remove('hidden')
})
closBar.addEventListener('click',function(){
    UnorderList.classList.add('hidden')
    closBar.classList.add('hidden')
    Bar.classList.remove('hidden')
    
})
Man.addEventListener('mouseover',()=>{
    Dopedowm1.classList.remove('hidden') 
})
Man.addEventListener('mouseout',()=>{
    Dopedowm1.classList.add('hidden')
})
woMan.addEventListener('mouseover',()=>{
    Dopedowm2.classList.remove("hidden");
})
woMan.addEventListener('mouseout',()=>{
    Dopedowm2.classList.add("hidden")
})
Jualary.addEventListener('mouseover',()=>{
    Dopedowm3.classList.remove("hidden")
})
Jualary.addEventListener('mouseout',()=>{
    Dopedowm3.classList.add("hidden")
})

let Search=document.getElementById("search")
let products=document.querySelectorAll(".prodt")

Search.addEventListener('keyup',function(){
    let searh_item=this.value.toLowerCase()
    products.forEach((product)=>{
       let prodt=product.textContent.toLowerCase()

        if (prodt.includes(searh_item)){
            product.style.display="inline-block";

        }
        else{
            product.style.display="none"
        }
    })
})