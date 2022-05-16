const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;


if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
        switchThemeDark();
    }
}


function switchThemeDark() {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
}


function switchThemeLight() {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light'); 
}