bash
pip install fastapi uvicorn
uvicorn main:app --reload


Примеры CURL запросов

curl -X POST "http://localhost:8000/reviews" \
-H "Content-Type: application/json" \
-d '{"text": "Мне нравится этот сервис, он отличный!"}'
{"id":2,"text":"Мне нравится этот сервис, он отличный!","sentiment":"positive","created_at":"2025-07-09T14:31:41.176565"}% 


curl "http://localhost:8000/reviews?sentiment=positive"
[{"id":2,"text":"Мне нравится этот сервис, он отличный!","sentiment":"positive","created_at":"2025-07-09T14:31:41.176565"}]%   


curl "http://localhost:8000/reviews"
[{"id":1,"text":"string","sentiment":"neutral","created_at":"2025-07-09T13:27:35.208688"},{"id":2,"text":"Мне нравится этот сервис, он отличный!","sentiment":"positive","created_at":"2025-07-09T14:31:41.176565"}]%  
