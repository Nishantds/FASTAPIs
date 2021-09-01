
# User Base Blog APIs

A user base crud API created with FastAPI and SQLAlchemy for mysql.

# Available APIs For User

It is recommended to test the available APIs from [GET] /docs

*     [GET] / -root - ( check API status )
*     [POST] / users / me - ( create user )
*     [POST] / token - ( login for access token )
*     [GET] / user / me - ( read current user details )

## When login with the created user then user is able to make it's own Blog

### Blog APIs for user 

*     [POST] / api / todos - ( create own blog details )
*     [GET] / api / mytodos - ( get current user  all blog )
*     [GET] / api / mytodos / { todo_id } - ( get blog detail by blog id )
*     [PUT] / api / todos / { todo_id } - ( update blog details by id  )
*     [DELETE] / api / todos / { todo_id } - ( delete blog details by id )


# Usage

set up a virtual environment :
    
    pip install virtualenv

using virtualenv :

    virtualenv my_name   

activate env using this command :
    
    source my_name/Scripts/activate

run application :

    uvicorn main:app --reload     
