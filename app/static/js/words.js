fetch('words/10')
    .then(response => response.json())
    .then(json => {
        const div = document.querySelector(".from-script");
        const list = document.createElement('ul');
        list.className = "list-group";
        for (const word in json) {
            if (json.hasOwnProperty(word)) {
                const li = document.createElement('li');
                li.innerText = `${word} - ${json[word]}`;
                li.className = "list-group-item border-0";
                list.append(li);
            }
        }
        div.append(list)
    })