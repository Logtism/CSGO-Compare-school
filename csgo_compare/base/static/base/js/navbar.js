const navbar = document.getElementsByTagName("nav");
const nav_content_links = document.getElementsByClassName("nav-content-links");


function toggle_navbar() {
    const nav_links_content = document.getElementById("nav-content");
    nav_links_content.classList.toggle("nav-toggled");
}


open_drop_downs = []


function toggle_dropdown(id) {
    let dropdown_content = document.getElementById(id);

    open_drop_downs.forEach(dropdown => {
        if (dropdown != dropdown_content) {
            dropdown.classList.remove("nav-dropdown-toggle");
        }
    });
    dropdown_content.classList.toggle("nav-dropdown-toggle");
    open_drop_downs.push(dropdown_content);
}