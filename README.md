# Django Mini Project Challenge

## 1. Project's Title

Django Celery Integration: Producer-Consumer Communication

## 2. Project Description

This project demonstrates the integration of two Django projects to establish communication between a producer and a consumer via API calls. The producer generates data based on user input, sends it to the consumer asynchronously using Celery, and receives the processed results through a webhook. Key features include the use of RabbitMQ as the message broker, Django REST framework for API endpoints, and django-celery-results for storing Celery task results.

## 3. Table of Contents
* [Requirements](#requirements)
* [Setup](#setup)
* [Usage](#usage)
* [Testing](#testing)
* [Achievements](#Achievements)

## 4. Requirements

- Python 3.8 or higher
- Django 3.2 or higher
- RabbitMQ (as the message broker)
- Django REST framework
- Celery
- django-celery-results
- Requests library

## 5. Setup

To set up this project, you will need to install only Docker and Docker Compose on your machine. Follow these steps:

1. Clone the repository 
    ```bash
    git clone https://github.com/Farkito-dev/farkito-hotel-api.git
    ```
2. Change settings Domain name for Producer and Consumer to you local ip address in both projects

3. Build Docker Image and Make Migrations
    ```bash
    docker-compose build --no-cache
    docker-compose run app sh -c "python manage.py makemigrations"
    docker-compose run app sh -c "python manage.py migrate"
    ```
4. generate API key for both application using django shell 

    ```bash
    docker-compose run app sh -c "python manage.py sh"
    from rest_framework_api_key.models import APIKey
    api_key, key = APIKey.objects.create_key(name="my-remote-service")
    print(api_key, key)

    ```

## 6. Usage

### 6.1 Consumer App

##### TaskResult Model

- Represents the result of a Celery task.


##### TaskAPIKey Model

- Extends AbstractAPIKey for API key functionality.
- Fields:
    - `task`: ForeignKey to the TaskResult model.

#### 6.1.2 API Endpoints

1. **Endpoint to List, Create, Update, and Delete Tasks:**
   - Method: GET, POST, PUT, PATCH, DELETE
   - URL: `/api/v1/consumer/tasks/`
   - View: `TaskResultViewSet`

2. **Endpoint to Send Message:**
   - Method: POST
   - URL: `/api/v1/consumer/send-message/`
   - View: `SendMessageView`

3. **Endpoint to Process Message:**
   - Method: POST
   - URL: `/api/v1/consumer/process-message/`
   - View: `ProcessMessageView`

##### Example 2: Create user

``` json 
{
  "webhook_url": "http://127.0.0.1:7000/api/v1/data/orders/c151efba-f415-4d2a-8b8f-161f30456aff/status/update",
  "address": "123 Main St",
  "phone_number": "555-1234",
  "order_key": "ABC123",
  "status": "pending",
  "currency": "USD"
}
```


### 6.2 Producer App

#### 6.2.1 Models Used

##### Order Model

- Represents an order created by a customer and consulted by a restaurant.
- Fields:
    - `uuid`: UUIDField for unique identification.
    - `user`: ForeignKey to the CustomUser model.
    - `address`: CharField for the delivery address.
    - `phone_number`: PhoneNumberField for the customer's phone number.
    - `created_at`: DateTimeField for the order creation timestamp.
    - `updated_at`: DateTimeField for the last update timestamp.
    - `total_paid`: DecimalField for the total amount paid.
    - `currency`: CharField for the currency used.
    - `order_key`: CharField for a unique order key.
    - `status`: CharField for order status (choices: pending, confirmed, cancelled).

##### OrderItem Model

- Represents an item within an order.
- Fields:
    - `order`: ForeignKey to the Order model.
    - `item_name`: CharField for the item name.
    - `price`: DecimalField for the item price.
    - `quantity`: PositiveIntegerField for the quantity ordered.

##### OrderAPIKey Model

- Extends AbstractAPIKey for API key functionality.
- Fields:
    - `order`: ForeignKey to the Order model.

##### TaskResult Model

- Represents the result of a Celery task.
- Fields:
    - `task_id`: CharField for the task ID.
    - `result`: CharField for the task result.


##### User Model

- Represents the result of a Celery task.
- Fields:
    - `username`: CharField for the user.
    - `password`: CharField for the user.
    - `email`: EmailField for the user.
    - `phone_number`: CharField for the user.


#### 6.2.2 API Endpoints



1. **Endpoint to List and Create Orders:**
   - Method: GET, POST
   - URL: `/api/v1/data/orders/`
   - View: `OrderViewSet`

2. **Endpoint to Retrieve, Update, and Delete a Specific Order:**
   - Method: GET, PUT, PATCH, DELETE
   - URL: `/api/v1/data/orders/<uuid:uuid>/`
   - View: `OrderViewSet`

3. **Endpoint to Update Order Status:**
   - Method: POST
   - URL: `/api/v1/data/orders/<uuid:uuid>/status/update`
   - View: `ChangeOrderStatusView`

4. **Endpoint to List Task Results:**
   - Method: GET
   - URL: `/api/v1/data/task-results/`
   - View: `TaskResultViewSet`

5. **Endpoint to Retrieve a Specific Task Result:**
   - Method: GET
   - URL: `/api/v1/data/task-results/<str:pk>/`
   - View: `TaskResultViewSet`

6. **Endpoint to Create Task Result:**
   - Method: POST
   - URL: `/api/v1/data/task-results/`
   - View: `TaskResultViewSet`

7. **Endpoint to Update and Delete a Specific Task Result:**
   - Method: PUT, PATCH, DELETE
   - URL: `/api/v1/data/task-results/<str:pk>/`
   - View: `TaskResultViewSet`


7. **Endpoint to Create User:**
   - Method: PUT, PATCH, DELETE
   - URL: `/api/v1/users/create`
   - View: `TaskResultViewSet`


7. **Endpoint to Create Token:**
   - Method: PUT, PATCH, DELETE
   - URL: `/api/v1/users/token`
   - View: `TaskResultViewSet`

#### 6.1.3 Examples of Payloads

##### Example 1: Create Order

```json
{
    "address": "Ariana Nkhilet",
    "phone_number": "+21658741196",
    "total_paid": 50,
    "currency": "TND",
    "items": [
        {
            "item_name": "item1",
            "price": 20,
            "quantity": 1
        },
        {
            "item_name": "item2",
            "price": 30,
            "quantity": 1
        }
    ]
}
```
##### Example 2: Create user

``` json 
{
    "username": "yahya",
    "email": "mlaouhi.yahya@gmail.com",
    "password": "1234567yahya@",
    "phone_number": "+21658741196"
}
```

## 7. Testing

Run unit tests for both projects:

```bash
# In the producer project
docker-compose run producer sh -c "python manage.py test"

# In the consumer project
docker-compose run consumer sh -c "python manage.py test"
```

## 8.  Achievements 

1. **Creating Virtual Environments and Installing Packages:**
   - I set up separate virtual environments for each application using Dockerfile.producer and Dockerfile.consumer. Additionally, I created a docker-compose file that manages both services for easier manipulation, addressing some configuration difficulties.

2. **Creating Django Projects and Apps:**
   - I established Django projects and apps for both the producer and consumer. Naming them was flexible, allowing customization.

3. **Creating Models in the Producer Project:**
   - For the producer project, I designed models to represent the data intended for the consumer. Specifically, I created an 'Order' model along with an 'Order Item' model to accurately track order states like 'pending' and 'confirmed.'

4. **Creating API Endpoints in the Producer Project:**
   - I developed API endpoints in the producer project using the Django REST framework. Utilizing model viewsets, I customized serializers and viewsets for creating orders and order items. Authentication and permission classes were implemented to secure access to these endpoints.

5. **Implementing Webhook Receiver in the Producer Project:**
   - I introduced a feature called 'ChangeOrderStatusView' within the producer project, serving as a webhook receiver. Authentication used API keys via 'rest_framework_api_key' for added security.

6. **Creating Celery Tasks in the Consumer Project:**
   - In the consumer project, I crafted Celery tasks designed to process message data and webhook URLs received from the producer. These tasks execute operations such as string concatenation (e.g., currency, order key, and status). The results were stored using 'django-celery-results.'

7. **Creating a View to Trigger Celery Task in the Consumer Project:**
   - A view named 'SendMessageView' was established within the consumer project. It accepts POST requests from the producer, initiating Celery tasks with the provided data. A response, including the task ID, is sent back to the producer.

8. **Exposing Celery Task Results via API in the Consumer Project:**
   - An API endpoint was devised in the consumer project to expose Celery task results. Using Django REST framework, a serializer and viewset were created for the 'TaskResult' model. Authentication and permission classes were implemented to control access to this endpoint.

9. **Creating a Signal Handler in the Consumer Project:**
   - A signal handler was implemented in the consumer project, triggered upon saving a Celery task result in the database. This handler sends the result to the producer's webhook URL using the 'requests' library.

10. **Writing Unit Tests:**
    - Unit tests were developed for both the consumer and producer projects using Django’s built-in testing framework.

11. **Running Tests and Manual Endpoint Testing:**
    - Tests were executed to ensure proper functionality in both projects. Additionally, local runs allowed manual testing of API endpoints using tools like Postman or curl.