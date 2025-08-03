## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Ermachok/test_gist_app.git

2. В корень проекта скопируйте приложенные в сообщении с ссылкой на гит .env и google_credits.json
3. В терминале 
    ```bash
   sudo docker compose up --build 
4. Приложение поднимется на http://127.0.0.1:8000, Swagger на http://127.0.0.1:8000/docs#,
5. таблица Google https://docs.google.com/spreadsheets/d/1VCp6JbDFZFW9s83Moct8xN8JaYzxCUrf5Ei88rvfP9E/edit?usp=sharing
6. Должно работать асинхронно. Например на запрос 
   ```bash
   curl -X POST http://localhost:8000/coverage -H "Content-Type: application/json" -d '{"latitude":55.75,"longitude":37.62,"radius_m":1000}' & 
   curl -X POST http://localhost:8000/coverage -H "Content-Type: application/json" -d '{"latitude":59.93,"longitude":30.31,"radius_m":1500}' & 
   curl -X POST http://localhost:8000/coverage -H "Content-Type: application/json" -d '{"latitude":48.85,"longitude":2.35,"radius_m":500}' & 
   curl -X POST http://localhost:8000/coverage -H "Content-Type: application/json" -d '{"latitude":40.71,"longitude":-74.01,"radius_m":1200}' & 
   curl -X POST http://localhost:8000/coverage -H "Content-Type: application/json" -d '{"latitude":34.05,"longitude":-118.24,"radius_m":800}' &
   wait
Ожидается ответ, где запросы обрабатываются асинхронно и стоит искусственная задержка в 5 секунд
![example_1](https://github.com/Ermachok/test_gist_app/blob/main/screens/img.png)
