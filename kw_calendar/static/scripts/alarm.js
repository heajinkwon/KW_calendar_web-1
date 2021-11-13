//indexedDB 관련 상태를 알려주는 변수
const stateNote = document.getElementById('notifications')

let db;

let newItem = [
    { taskTitle: "", hours: 0, minutes: 0, day: 0, month: "", notified: "no" }
];

//html 요소들을 자바스크립트로 가져오는 변수
const taskList = document.getElementById('task-list');
const taskForm = document.getElementById('task-form');
const title = document.getElementById('title');

const hours = document.getElementById('deadline-hours');
const minutes = document.getElementById('deadline-minutes');
const day = document.getElementById('deadline-days');
const month = document.getElementById('deadline-months');

const submit = document.getElementById('submit');

//웹페이지가 온전히 로드된 상태에서 작동
window.onload = function () {
    //브라우저가 기능을 지원하는지 물어보고 권한을 설정했는지 물어보는 if문
    if (!("Notification" in window)) {
        alert("현재 브라우저는 알림 기능을 지원하지 않습니다");
    }
    else if (Notification.permission === "granted") {
        var notification = new Notification("KW Calendar Web", {body:'작동 준비 완료'});

        setTimeout(function (){
            notification.close();
        },3000);
    }
    else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(function (permission) {
            if (permission === "granted") {
                var notification = new Notification("KW Calendar Web", {body:'권한 설정 완료'});

                setTimeout(function (){
                    notification.close();
                },3000);
            }
            else {
                alert("알림 권한 요청이 거부되었습니다.")
            }
        });
    }

    stateNote.innerHTML += '<li>App initialised.</li>';
    window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
    window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.msIDBTransaction;
    window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.msIDBKeyRange;

    //데이터베이스 오픈
    const DBOpenRequest = window.indexedDB.open("KW-Calendar-Web");

    //에러 처리
    DBOpenRequest.onerror = function (event) {
        stateNote.innerHTML += '<li>Error loading database.</li>';
    };

    //성공 처리
    DBOpenRequest.onsuccess = function (event) {
        stateNote.innerHTML += '<li>Database initialised.</li>';

        db = DBOpenRequest.result;

        displayData();
    };

    //데이터베이스 저장소 생성
    DBOpenRequest.onupgradeneeded = function (event) {
        let db = event.target.result;

        //에러 처리
        db.onerror = function (event) {
            stateNote.innerHTML += '<li>Error loading database.</li>';
        };

        let objectStore = db.createObjectStore("KW-Calendar-Web", {keyPath: "taskTitle"});

        objectStore.createIndex("hours", "hours", {unique: false});
        objectStore.createIndex("minutes", "minutes", {unique: false});
        objectStore.createIndex("day", "day", {unique: false});
        objectStore.createIndex("month", "month", {unique: false});

        objectStore.createIndex("notified", "notified", { unique: false });

        stateNote.innerHTML += '<li>Object store created.</li>';
    }

    function displayData() {
        taskList.innerHTML = "";

        let objectStore = db.transaction('KW-Calendar-Web').objectStore('KW-Calendar-Web');
        objectStore.openCursor().onsuccess = function(event) {
            let cursor = event.target.result;

            if(cursor) {
                const listItem = document.createElement('li');

                daySuffix = "일";

                listItem.innerHTML = cursor.value.taskTitle + ' — ' + cursor.value.hours + ':' + cursor.value.minutes + ', ' + cursor.value.month + ' ' + cursor.value.day + daySuffix + ' ';

                if(cursor.value.notified == "yes") {
                    listItem.style.textDecoration = "line-through";
                    listItem.style.color = "rgba(255,0,0,0.5)";
                }

                taskList.appendChild(listItem);

                const deleteButton = document.createElement('button');
                listItem.appendChild(deleteButton);
                deleteButton.innerHTML = 'X';
                deleteButton.setAttribute('data-task', cursor.value.taskTitle);
                deleteButton.onclick = function(event) {
                    deleteItem(event);
                }

                cursor.continue();

            } else {
                stateNote.innerHTML += '<li>Entries all displayed.</li>';
            }
        }
    }

    taskForm.addEventListener('submit',addData,false);

    function addData(e) {
        e.preventDefault();

        if(title.value == '' || hours.value == null || minutes.value == null || day.value == '' || month.value == '') {
            stateNote.innerHTML += '<li>Data not submitted — form incomplete.</li>';

        } else {

            let newItem = [
                { taskTitle: title.value, hours: hours.value, minutes: minutes.value, day: day.value, month: month.value, notified: "no" }
            ];

            let transaction = db.transaction(["KW-Calendar-Web"], "readwrite");

            transaction.oncomplete = function() {
                stateNote.innerHTML += '<li>Transaction completed: database modification finished.</li>';

                displayData();
            };

            transaction.onerror = function() {
                stateNote.innerHTML += '<li>Transaction not opened due to error: ' + transaction.error + '</li>';
            };

            let objectStore = transaction.objectStore("KW-Calendar-Web");
            console.log(objectStore.indexNames);
            console.log(objectStore.keyPath);
            console.log(objectStore.name);
            console.log(objectStore.transaction);
            console.log(objectStore.autoIncrement);

            let objectStoreRequest = objectStore.add(newItem[0]);
            objectStoreRequest.onsuccess = function(event) {

                stateNote.innerHTML += '<li>Request successful.</li>';

                title.value = '';
                hours.value = null;
                minutes.value = null;
                day.value = 01;
                month.value = '1월';
            };
        }
    }

    function deleteItem(event) {
        let dataTask = event.target.getAttribute('data-task');

        let transaction = db.transaction(["KW-Calendar-Web"], "readwrite");
        let request = transaction.objectStore("KW-Calendar-Web").delete(dataTask);

        transaction.oncomplete = function() {
            event.target.parentNode.parentNode.removeChild(event.target.parentNode);
            stateNote.innerHTML += '<li>Task \"' + dataTask + '\" deleted.</li>';
        };
    }

    function checkLectureTime() {

        const now = new Date();

        const minuteCheck = now.getMinutes();
        const hourCheck = now.getHours();
        const dayCheck = now.getDate();
        const monthCheck = now.getMonth();


        let objectStore = db.transaction(['KW-Calendar-Web'], "readwrite").objectStore('KW-Calendar-Web');
        objectStore.openCursor().onsuccess = function(event) {
            let cursor = event.target.result;
            if(cursor) {
                switch(cursor.value.month) {
                    case "1월":
                        var monthNumber = 0;
                        break;
                    case "2월":
                        var monthNumber = 1;
                        break;
                    case "3월":
                        var monthNumber = 2;
                        break;
                    case "4월":
                        var monthNumber = 3;
                        break;
                    case "5월":
                        var monthNumber = 4;
                        break;
                    case "6월":
                        var monthNumber = 5;
                        break;
                    case "7월":
                        var monthNumber = 6;
                        break;
                    case "8월":
                        var monthNumber = 7;
                        break;
                    case "9월":
                        var monthNumber = 8;
                        break;
                    case "10월":
                        var monthNumber = 9;
                        break;
                    case "11월":
                        var monthNumber = 10;
                        break;
                    case "12월":
                        var monthNumber = 11;
                        break;
                    default:
                        alert('날짜가 맞지 않습니다.');
                }

                if(+(cursor.value.hours) == hourCheck && +(cursor.value.minutes) == minuteCheck && +(cursor.value.day) == dayCheck && monthNumber == monthCheck && cursor.value.notified == "no") {

                    if(Notification.permission === 'granted') {
                        createNotification(cursor.value.taskTitle);
                    }
                }

                cursor.continue();
            }

        }

    }

    function createNotification(title) {

        let text = '"' + title + '" 강의가 곧 시작됩니다.';
        let notification = new Notification('KW-Calendar-Web', { body: text });

        let objectStore = db.transaction(['KW-Calendar-Web'], "readwrite").objectStore('KW-Calendar-Web');

        let objectStoreTitleRequest = objectStore.get(title);

        objectStoreTitleRequest.onsuccess = function() {

            let data = objectStoreTitleRequest.result;

            data.notified = "yes";

            let updateTitleRequest = objectStore.put(data);

            updateTitleRequest.onsuccess = function() {
                displayData();
            }
        }
    }

    setInterval(checkLectureTime, 1000);
}

