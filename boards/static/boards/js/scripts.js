document.addEventListener('DOMContentLoaded', function () {
    const boardsContainer = document.getElementById('boards-container'); // контейнер для досок

    // Инициализация задач после загрузки страницы
    function initTasks() {
        const tasks = document.querySelectorAll('.task');
        tasks.forEach(task => {
            task.setAttribute('draggable', true);

            task.addEventListener('dragstart', function (event) {
                event.dataTransfer.setData('taskId', task.dataset.taskId);
                event.dataTransfer.setData('sourceBoardId', task.closest('.board').dataset.boardId);
                setTimeout(() => task.classList.add('dragging'), 0); // Плавное выделение задачи
            });

            task.addEventListener('dragend', function () {
                task.classList.remove('dragging'); // Удаление выделения
            });
        });
    }

    // Проверка и обновление состояния пустой доски
    function updateEmptyBoardMessage(board) {
        const taskList = board.querySelector('.task-list');
        const emptyBoardMessage = taskList.querySelector('.empty-board');

        // Проверяем, есть ли хотя бы одна задача на доске
        if (taskList.children.length === 0) {
            // Если задач нет, показываем сообщение
            if (emptyBoardMessage) {
                emptyBoardMessage.style.display = 'block'; // Показать сообщение о пустой доске
            }
        } else {
            // Если на доске есть задачи, скрываем сообщение
            if (emptyBoardMessage) {
                emptyBoardMessage.style.display = 'none'; // Скрыть сообщение о пустой доске
            }
        }
    }

    // Обработчик события перетаскивания задачи на доску
    boardsContainer.addEventListener('dragover', function (event) {
        const board = event.target.closest('.task-list');
        if (board) {
            event.preventDefault(); // Разрешаем перетаскивание
            board.classList.add('drag-over'); // Подсветка при наведении
        }
    });

    boardsContainer.addEventListener('dragleave', function (event) {
        const board = event.target.closest('.task-list');
        if (board) {
            board.classList.remove('drag-over'); // Убираем подсветку при выходе
        }
    });

    boardsContainer.addEventListener('drop', function (event) {
        const board = event.target.closest('.task-list');
        if (!board) return;

        event.preventDefault();
        board.classList.remove('drag-over');

        const taskId = event.dataTransfer.getData('taskId');
        const sourceBoardId = event.dataTransfer.getData('sourceBoardId');
        const targetBoardId = board.closest('.board').dataset.boardId;

        // Проверяем, перемещается ли задача в другую доску
        if (sourceBoardId !== targetBoardId) {
            const task = document.querySelector(`[data-task-id='${taskId}']`);
            task.classList.add('loading');

            // Отправляем запрос на сервер для перемещения задачи
            fetch('/move_task/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({
                    task_id: taskId,
                    board_id: targetBoardId,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        board.appendChild(task);
                        // Обновляем состояние доски сразу после переноса задачи
                        updateEmptyBoardMessage(board); // Проверяем доску после добавления задачи
                        const sourceBoard = document.querySelector(`[data-board-id='${sourceBoardId}']`);
                        if (sourceBoard) {
                            updateEmptyBoardMessage(sourceBoard); // Обновляем состояние доски-источника
                        }
                    } else {
                        alert('Не удалось переместить задачу: ' + data.error);
                    }
                })
                .catch(error => {
                    alert('Произошла ошибка при перемещении задачи.');
                    console.error(error);
                })
                .finally(() => {
                    task.classList.remove('loading');
                });
        }
    });

    // Добавление новой задачи
    document.querySelectorAll('.add-task').forEach(button => {
        button.addEventListener('click', function () {
            const boardId = button.closest('.board').dataset.boardId;
            const taskTitle = prompt('Введите название задачи:');
            if (taskTitle) {
                // Показываем индикатор создания
                button.disabled = true;

                // Отправляем запрос на сервер
                fetch('/add_task/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: JSON.stringify({
                        board_id: boardId,
                        title: taskTitle,
                    }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Создаём новую задачу в DOM
                            const newTask = document.createElement('div');
                            newTask.className = 'task';
                            newTask.dataset.taskId = data.task_id;
                            newTask.innerHTML = `<h4>${taskTitle}</h4><p>Описание задачи</p>`;
                            initTasks();
                            button.closest('.board').querySelector('.task-list').appendChild(newTask);
                            // Обновляем состояние доски после добавления новой задачи
                            updateEmptyBoardMessage(button.closest('.board'));
                        } else {
                            alert('Ошибка при добавлении задачи.');
                        }
                    })
                    .catch(error => {
                        alert('Произошла ошибка при добавлении задачи.');
                        console.error(error);
                    })
                    .finally(() => {
                        button.disabled = false;
                    });
            }
        });
    });

    // Функция для получения CSRF-токена из куки
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split('; ');
        for (let cookie of cookies) {
            if (cookie.startsWith(name + '=')) {
                return cookie.split('=')[1];
            }
        }
        return '';
    }

    // Инициализация задач после загрузки страницы
    initTasks();

    // Для всех досок на начальной загрузке проверим их состояние (пустые или нет)
    document.querySelectorAll('.board').forEach(board => {
        updateEmptyBoardMessage(board); // Проверка для каждой доски
    });
});
