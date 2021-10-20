//ejecutar fuincion en el evento click //
document.getElementById("btn_open").addEventListener("click", open_close_menu)
//declaramos variables//

var side_menu= document.getElementById("menu-side");
var btn_open= document.getElementById("btn_open");
var body= document.getElementById("body");

//Evento para mostrar y ocultar menu//

function open_close_menu(){
    body.classList.toggle("body_move")
    side_menu.classList.toggle("menu_side_move")
}