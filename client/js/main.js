window.onload = function () {

    var uploadButton = document.querySelector('.upload-song-button');
    var uploadedSong = document.querySelector('.upload-song');
    var imageContainer = document.querySelector('.image-container');
    var numbersContainer = document.querySelector('.numbers-container');

    var intervalStart = document.querySelector('.interval-start');
    var intervalEnd = document.querySelector('.interval-end');

    function sendRequest(url, method = 'GET', data) {
        return fetch(url, { method, body: data }).then(response => response.json());
    }

    function showShouldRenderNumbersButton() {
        var button = document.createElement('button');
        button.innerHTML = 'Показать числовые данные';
        button.addEventListener('click', function () {
            sendRequest('/get-numbers-values').then(value => {
                if (value.data) {
                    var numbers = value.data;
                    var numbersBlock = document.createElement('div');
                    numbersBlock.classList.add('numbers');
                    Object.entries(numbers).forEach(([interval, values]) => {
                        var valuesStr = '';
                        values.forEach(value => {
                            valuesStr += value + ', '
                        });
                        valuesStr.length -= 2;
                        numbersBlock.innerHTML += `Диапазон: ${interval}; значения: ${valuesStr}\n`;
                    });
                    numbersContainer.appendChild(numbersBlock);
                }
            })
        });
        numbersContainer.innerHTML = '';
        numbersContainer.appendChild(button);
    }

    function renderImageToContainer(imageCode) {
        var image = document.createElement('img');
        image.src = `data:image/png;base64,${imageCode}`;
        image.classList.add('image');
        imageContainer.innerHTML = '';
        imageContainer.appendChild(image);
        showShouldRenderNumbersButton();
    }

    uploadButton.addEventListener('click', function () {
        var file = uploadedSong.files[0];
        var data = new FormData();
        var startInterval = Number(intervalStart.value) || '';
        var endInterval = Number(intervalEnd.value) || '';
        var url = `/upload-song?start=${startInterval}&end=${endInterval}`;
        data.append('file', file);
        sendRequest(url, 'POST', data)
            .then(value => {
                renderImageToContainer(value.img);
            })
    });

};