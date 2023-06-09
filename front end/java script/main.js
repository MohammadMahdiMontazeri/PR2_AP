let slideIndex = 1
function setSlide(input,index){
    slideIndex = index;
    let item = document.querySelector(`#${input}`)
    let slides = [...document .querySelector('.slides').children];
    slides.forEach((element)=>{
        element.classList.remove ('active');
    })
    item.classList.add('active');
}


setInterval (()=>{
    slideIndex += 1;
    if(slideIndex == 4){
        slideIndex = 1
    }
    setSlide(`slide${slideIndex}` , slideIndex)
} , 4500)


function addToCart(productName) {
  fetch("/add-to-cart", {
    method: "POST",
    body: JSON.stringify({ productName: productName })
  }).then((_res) => {
    window.location.reload();
  });
};

