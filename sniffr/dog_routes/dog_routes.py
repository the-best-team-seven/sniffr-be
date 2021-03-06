from concurrent.futures import process
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from sniffr.models import Dog, process_records, db, User, process_record, Breed

# Blueprint Configuration
dog_bp = Blueprint("dog_bp", __name__)


@dog_bp.route("/dog/<dog_id>", methods=["GET"])
@cross_origin()
def get_dog(dog_id):
    """Get dog info"""
    dog_id = int(dog_id)

    queried_dog = db.session.query(Dog).join(User).filter(Dog.dog_id==dog_id).first()
    if queried_dog:
        response = process_record(queried_dog)
        response['owner'] = queried_dog.owner.username
        response['breed'] = queried_dog.breed.breed_name
        return response

    else:
        response = {"message": "Dog Not Found"}
        return response, 400


@dog_bp.route("/dog", methods=["POST"])
@cross_origin()
def post_dog():
    """Create or edit dog info"""
    content = request.json

    # If dog_id not in body then they are trying to create
    # If dog_id in body then updating content
    if "dog_id" in content.keys():
        queried_dog = db.session.query(Dog).filter(Dog.dog_id==content["dog_id"]).first()
        if queried_dog:
            # Update properties
            queried_dog.dog_name = content['dog_name']
            queried_dog.owner_id = content['owner_id']
            queried_dog.breed_id = content['breed_id']
            queried_dog.is_vaccinated = content['is_vaccinated']
            queried_dog.is_fixed = content['is_fixed']
            queried_dog.age = content['age']
            queried_dog.sex = content['sex']
            queried_dog.sex = content['sex']
            queried_dog.sex = content['sex']
            queried_dog.last_updated = datetime.now()

            db.session.commit()

            response = process_record(queried_dog)
            response['breed'] = queried_dog.breed.breed_name

            return response

        else:
            response = {"message": "Dog Not Found"}
            return response

    else:
        # create dog
        dog_name = content["dog_name"]
        owner_id = content["owner_id"]
        breed_id = content["breed_id"]
        is_vaccinated = content["is_vaccinated"]
        is_fixed = content["is_fixed"]
        age = content["age"]
        sex = content["sex"]

        new_dog = Dog(
            dog_name=dog_name,
            owner_id=owner_id,
            breed_id=breed_id,
            age=age,
            sex=sex,
            is_vaccinated=is_vaccinated,
            is_fixed=is_fixed
        )
        db.session.add(new_dog)
        db.session.commit()

        queried_dog = (
            db.session.query(Dog).join(Breed).join(User).filter(Dog.dog_id==new_dog.dog_id).first()
        )
        response = process_record(queried_dog)
        response['breed'] = queried_dog.breed.breed_name

        return response
