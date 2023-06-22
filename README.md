Here is groceries assistant with recipe database FOODGRAM. Here you can find a community of people sharing various reipces. 
You can add your own recipes or check other users ideas, if you find anything you like add it to favorites or to shopping cart.
Shopping cart allows you to receive a list of all the necessary ingredients with given amounts.


![Workflow status](https://github.com/cosmofactory/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### How to start a project:

Clone the repository:

```
git clone git@github.com:cosmofactory/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Activate virtual environment:

```
python -m venv env
```

* Linux/MacOS

    ```
    source env/bin/activate
    ```

* Windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Install necessary requirements.txt:

```
pip install -r requirements.txt
```

Migrate the database tables:

```
python manage.py migrate
```

Load your database with preset ingredients:

```
python manage.py import_csv
```

Run project:

```
python manage.py runserver
```

Api documentation is located here:

```
http://127.0.0.1:8000/redoc/
```

Some API examples:

```
    {
        "id": 3,
            "tags": [
                {
                    "id": 3,
                    "name": "Ужин",
                    "color": "#C6FF22",
                    "slug": "dinner"
                },
                {
                    "id": 1,
                    "name": "Завтрак",
                    "color": "#FF0000",
                    "slug": "breakfast"
                }
            ],
            "author": {
                "email": "shopper@g.com",
                "id": 2,
                "username": "the_best_chef1977",
                "first_name": "Joe",
                "last_name": "Dow",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 4,
                    "name": "черника замороженная",
                    "measurement_unit": "г",
                    "amount": 69.0
                },
                {
                    "id": 5,
                    "name": "чечевица",
                    "measurement_unit": "г",
                    "amount": 13.0
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Boiled potatoes",
            "image": "http://127.0.0.1:8000/media/images/temp_ehqltZk.png",
            "text": "Just boild them in water",
            "cooking_time": 90
    },
```

Author:
Nikita Assorov, email - nikssor@yandex.ru

```
https://github.com/cosmofactory
```
Stack used: DRF, Djoser, REST API, Redoc, React, Docker, PostgreSQL
