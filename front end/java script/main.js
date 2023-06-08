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


// function addToCart(productName){
//     fetch('add-to-cart',{
//         method:'POST',
//         body: JSON.stringify({ productName: productName})
//     }).then((_res) => {
//         window.location.href = "/" ;
//     })
// }

// function inPro(productName){
//     fetch('increase-product',{
//         method:'POST',
//         body: JSON.stringify({ productName: productName})
//     }).then((_res) => {
//         window.location.href = "/" ;
//     })
// }

// function dePro(productName){
//     fetch('decrease-product',{
//         method:'POST',
//         body: JSON.stringify({ productName: productName})
//     }).then((_res) => {
//         window.location.href = "/" ;
//     })
// }

// function removeProduct(productName){
//     fetch('admin',{
//         method:'DELETE',
//         body: JSON.stringify({ productName: productName})
//     }).then((_res) => {
//         window.location.href = "/" ;
//     })
// }

var button = document.getElementById("remove-product");

button.addEventListener("click", function() {
  var productName = button.getAttribute("data-product-id");

  fetch("/remove-product", {
    method: "POST",
    body: JSON.stringify({ productName: productName })
  }).then((_res) => {
    window.location.reload();
  });
});