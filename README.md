# Social Network DRF-simpleJWT + Bot

Simple social network created by using Django REST Framework and Simple JWT Authentication.
+ Bot which registers "n" amount of users, creates "n" amount of posts and likes other's posts.

## Overview

Social network project which allows to sign-up and authenticate users, create posts and interact with them by "Like / Unlike system". For more information please read "Features"

## Features

- User sign-up
- User login
- User authentification using token
- Creating post
- View Other's posts
- Like / Unlike Other's posts
- Post's like analytics calculated per day
- User's activity information (last login, last request)

- Bot:
- Sign-up users (number as per config file)
- Each created User creates random number of posts with any content (number as per config file)
- Each created User likes posts randomly, posts can be liked multiple times

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/carrion626/social_network.git
    ```

2. Install dependencies:

    ```bash
    pip install django djangorestframework
    ```
Simple JWT can be installed with pip:

pip install djangorestframework_simplejwt
Then, your django project must be configured to use the library. In settings.py, add rest_framework_simplejwt.authentication.JWTAuthentication to the list of authentication classes:

REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}

## Usage

By signing-up you can proceed to Login User and once you enter "username" and "password" of registered user it will return 'access' and 'refresh' token.
With 'access' token you can go to Postman and interact with other endpoints which are listed below.

## Endpoints

    'api/register/' - Register User
    'api/' - User Login
    'api/users/' - List of All Users
    'api/token/' - Get Registered User Access Token
    'api/token/refresh/' - Refresh Existing Token
    'api/posts/' - ViewSet of Posts
    'api/create/' - Create new post
    'api/posts/<int:post_id>/like/' - Like / Unlike Post
    'api/user_activity/' - User Activity endpoint
    'api/analytics/' - Post activity analytics endpoint


### Register User

- **Endpoint:** `/api/register/`
- **Method:** `POST`
- **Description:** Register a new user.

### User Login

- **Endpoint:** `/api/`
- **Method:** `POST`
- **Description:** Authenticate an existing user and obtain JWT tokens.

### All Users

- **Endpoint:** `/api/users/`
- **Method:** `GET`
- **Authentication:** JWT (JSON Web Token)
- **Description:** Retrieve a list of all registered users.

### Posts

- **Endpoint:** `/api/posts/`
- **Method:** `GET`
- **Authentication:** JWT (JSON Web Token)
- **Description:** Retrieve a list of all posts.

### Create Post

- **Endpoint:** `/api/create/`
- **Method:** `POST`
- **Authentication:** JWT (JSON Web Token)
- **Description:** Create post.

### Like / Unlike Post

- **Endpoint:** `api/posts/<int:post_id>/like/`
- **Method:** `POST`
- **Authentication:** JWT (JSON Web Token)
- **Description:** Like post (or if post was already liked - Unlike).

### User Activity

- **Endpoint:** `api/user_activity/`
- **Method:** `GET`
- **Authentication:** JWT (JSON Web Token)
- **Description:** View user activity (last login, last request).

### Post Analytics

- **Endpoint:** `api/analytics/?date_from=2020-02-25&date_to=2020-02-26`
- **Method:** `GET`
- **Authentication:** JWT (JSON Web Token)
- **Description:** View post activity (like / unlike) per day.

## Licence

This project borrows code from the Django REST Framework as well as concepts from the implementation of another JSON web token library for the Django REST Framework, django-rest-framework-jwt. The licenses from both of those projects have been included in this repository in the "licenses" directory.
