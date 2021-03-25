window.onload = () => {
    function disableAllSection(sections) {
        sections.forEach(function(item, index) {
            item.classList.add("Hide");
        });
    }

    function disableAllSectionExcept(sections, number) {
        sections.forEach(function(item, index) {
            if (index != number) {
                item.classList.add("Hide");
            }
        });
    }

    var sectionHeadings = document.querySelectorAll(".Section-Heading");      
    var sections = document.querySelectorAll(".Section");

    disableAllSection(sections);

    sectionHeadings.forEach(function (item, index) {
        item.addEventListener("click", () => {
            disableAllSectionExcept(sections, index);
            sections[index].classList.toggle("Hide");
        });
    });
};