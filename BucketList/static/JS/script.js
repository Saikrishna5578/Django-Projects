// console.log("started");

// let inp = document.querySelector("input");
// let ul = document.querySelector("ul");
// let uldv = document.getElementById("listitems")

// let form = document.querySelector("form");
// form.addEventListener("submit", (e) => {
//     if (inp.value === "") {
//         e.preventDefault(); // prevent only if no input
//         enter.innerText = "Enter list item before clicking on 'ADD TO LIST'";
//         enter.style.backgroundColor = "white";
//     }
//     else{
//         console.log(inp.value);
//         e.preventDefault()
//         uldv.innerHTML += `
//     <li>
//     <p>${inp.value}</p>
//     <div>
//     <button id = "edit">Edit</button>
//     <button id = "del">Delete</button>
//     </div>
//     </li>`
//     inp.value = ""
//     enter.innerText = ""
//     enter.style.backgroundColor = "";

//     }
// });

// // btn.addEventListener("click", ()=>{

// //     if(inp.value === ""){
// //         enter.innerText = "Enter list item before clicking on 'ADD TO LIST ' "
// //         enter.style.backgroundColor = "white";
// //     }
    
// // })


// // console.log(inp.value);
// ul.addEventListener("click",(e)=>{
//     console.log(e.target);
//     if(e.target.innerText === "Delete"){
//         e.target.parentElement.parentElement.remove();
//         inp.value = "";
//     }
//     else if(e.target.innerText === "Edit"){
//         inp.value = e.target.parentElement.previousElementSibling.innerText;
//         e.target.innerText = "Update";
//         btn.style.display = "none";
//         e.target.parentElement.lastElementChild.style.display ="none"

//     }
//     else if(e.target.innerText === "Update"){
//         e.target.parentElement.previousElementSibling.innerText = inp.value;
//         e.target.innerText = "Edit";
//         btn.style.display = "inline";
//         e.target.parentElement.lastElementChild.style.display ="inline"

//         inp.value = "";
//     }
//     else{
//         btn.style.display = "inline";
//     }
// })



