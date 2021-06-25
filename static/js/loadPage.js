class ConstructPage {

    constructor() {
        this.lyricSong = this.createNode("div", "",
            "col-8 song h-75 overflow-auto");
        this.translateSong = this.createNode("div", "",
            "col-4 px-5 h-75 border-start border-secondary");
        this.translateSong.append(this.makeCopyIcon());
        document.querySelector("#main-content").append(this.lyricSong);
        document.querySelector("#main-content").append(this.translateSong);
        this.name = `${location.pathname}/lyric`;
        this.currentWordNum = 0;
        (async () => {
            let lyric = await this.loadLyric();
            this.lyricSong.textContent = lyric.lyric;
            this.lyricSong.classList.add("song", "h-75", "overflow-auto");
            this.wordsPosition = this.getWordsPosition(this.lyricSong.textContent);
            this.createTranslateDiv();
            this.selectWord(0);
            this.translateForm = this.makeSmallForm();
            this.translateSong.append(this.translateForm);
        })();
    }

    async loadLyric() {
        try {
            let response = await fetch(this.name);
            return await response.json();
        } catch (err) {
            this.lyricSong.innerHTML = "<h3>Истина где-то рядом</h3>";
        }
    }

    makeCopyIcon() {
        let span = this.createNode("span");
        let h5 = this.createNode("h5", "", "my-2");
        let img = this.createNode("img", "", "inline mx-1");
        img.src = "/static/copy.svg";
        img.style = "height: 0.9em;";
        h5.append(span, img);
        return h5;
    }

    makeSmallForm() {
        let div = this.createNode("div", "", "mt-3 pt-3");
        let input = this.createNode("input", "", "form-control");
        input.value = null;
        input.placeholder = "Введите перевод";
        let btn = this.createNode("button", "Отправить", "btn btn-primary m-2");
        btn.setAttribute("data-action-translate", "translate");
        let btn2 = this.createNode("button", "Забыть", "btn btn-warning m-2");
        btn2.setAttribute("data-action-translate", "forget");
        div.append(input, btn, btn2);
        div.hidden = true;
        div.addEventListener('click', this.eventHandler.bind(this))
        return div;
    }

    eventHandler(event) {
        let action = event.target.dataset.actionTranslate;
        let inputField = event.target.parentElement.querySelector("input");
        if (action !== undefined) {
            let toTranslate = {};
            toTranslate[this.currentWord.word] = (action === "translate") ? inputField.value : this.currentWord.word;
            this.wordsMethodPOST(toTranslate).then(() => {
                inputField.value = null;
                setTimeout(() => this.nextWord(), 1000);
            })
        }
    }


    makeObj(iterable) {
        let array = Array.from(iterable);
        let result = new Map();
        array.forEach(elem => result[elem] = "");
        return result;
    }

    async sendWords(words) {
        return this.wordsMethodGET(words)
    }

    async wordsMethodPOST(words) {
        let url = `${location.origin}/words/json`;
        const data = {words: words};
        let content;
        const rawResponse = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        content = await rawResponse.json();
        return content;
    }

    async wordsMethodGET(words) {
        let url = new URL(`${location.origin}/words/json`),
            params = this.makeObj(words)
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        let rawResponse = await fetch(url);
        return await rawResponse.json();
    }

    createNode(tag, textContent, className) {
        const node = document.createElement(tag);
        textContent ? node.textContent = textContent : null;
        className ? node.className = className : null;
        return node;
    }

    nextWord() {
        (this.currentWordNum < this.wordsPosition.length - 1) ? this.currentWordNum++ : this.currentWordNum = 0;
        this.selectWord(this.currentWordNum);
    }

    selectWord(num) {
        let selection = this.wordsPosition[num];
        this.makeSelection(this.lyricSong, selection.start, selection.end);
        let word = this.wordsPosition[this.currentWordNum].word
        this.sendWordToTranslateDiv(word);
        this.translateSong.querySelector("h5").firstChild.textContent = word;
        this.currentWord = this.wordsPosition[num];
        this.changeTranslateList(this.currentWord.word);
        navigator.clipboard.writeText(this.currentWord.word)
    }

    makeSelection(node, start, end) {
        node.textContent = node.innerText;
        let range = new Range();
        range.setStart(node.firstChild, start);
        range.setEnd(node.firstChild, end);
        let newNode = document.createElement('span');
        newNode.className = "btn btn-primary";
        range.surroundContents(newNode);
        newNode.scrollIntoView({block: "center", behavior: "smooth"});
    }

    createTranslateDiv() {
        const list = document.createElement('ul');
        list.className = "list-group";
        const btn = this.createNode("button", "Дальше", "btn btn-secondary mt-5")
        btn.addEventListener('click', event => this.nextWord());
        this.translateSong.append(list, btn)
    }

    makeTranslateList(word) {
        const li = this.createNode("li", "_",
            "list-group-item border-0 btn btn-outline-secondary");
        li.addEventListener('click', event => {
            if (li.textContent === this.response[this.currentWord.word]) {
                li.classList.remove("btn-outline-secondary");
                li.classList.add("btn-outline-success");
                setTimeout(() => this.nextWord(), 1000);
            } else {
                li.classList.remove("btn-outline-secondary");
                li.classList.add("btn-outline-danger");
            }
        });
        return li;
    }

    sendWordToTranslateDiv(word) {
        let list = this.translateSong.querySelector("ul")
        list.innerHTML = "";
        for (let i = 0; i < 5; i++) {
            list.append(this.makeTranslateList());
        }
    }

    changeTranslateList(word) {
        let list = this.makeFakeList(word);
        let i = 0;
        this.sendWords(list).then(content => {
                this.response = content.words;
                let response = Object.entries(content.words);
                for (let li of this.translateSong.children[1].children) {
                    li.textContent = response[i][1] ? response[i][1] : response[i][0];
                    i++;
                }
                this.translateForm.hidden = !!content.words[this.currentWord.word];
            }
        )
    }

    makeFakeList(word) {
        let fakeList = new Set();
        fakeList.add(word);
        while (fakeList.size < 5) {
            let randomWord = this.wordsPosition[Math.floor(Math.random() * this.wordsPosition.length)].word;
            fakeList.add(randomWord);
        }
        let result = Array.from(fakeList);
        return result.sort(() => Math.random() - 0.5);
    }


    getWordsPosition(text) {
        const re = /\b([A-Z]|[a-z])+[']*[’]*[a-z]*('|\b)/g;
        const reMatch = text.matchAll(re);
        let result = [];
        for (let element of reMatch) {
            if (element[0]) {
                result.push({
                    word: element[0].toLowerCase(),
                    start: element.index,
                    end: element.index + element[0].length,
                })
            }
        }
        return result
    }
}


class LoadContent
    extends ConstructPage {

    constructor() {
        super()
    }
}

new LoadContent();
