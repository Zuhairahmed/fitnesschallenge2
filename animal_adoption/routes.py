import datetime
import uuid
import json
from pathlib import Path
from flask.helpers import send_from_directory
from animal_adoption import (
    app, Shelter, User, UserDetail, ShelterWorker,
    Adopter, UserType, Animal, AnimalClass,
    AnimalNews, ALLOWED_EXTENSIONS, Administrator
)
from flask import jsonify, make_response, redirect, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies, unset_access_cookies
)
from werkzeug.utils import secure_filename


app.config['JWT_SECRET_KEY'] = 'JofJtRHKzQmFRXGI4v60'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=86400)
app.config['JWT_COOKIE_NAME'] = "ACCESS-COOKIE"
jwt = JWTManager(app)


def allowed_file(filename):
    print(filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', endpoint='', methods=['GET'])
def index():
    """
    Index
    :return:
    """
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/login', endpoint='login', methods=['POST'])
def login():
    """
    Authenticate existing user
    :return:
    """
    if not request.is_json:
        print('uri=/login error="Missing JSON in request"')
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        print('uri=/login error="Missing password parameter"')
        return jsonify({"msg": "Missing password parameter"}), 400

    result = User.authenticate_user(username=username, password=password)
    if result:
        access_token = create_access_token(identity=User.get_id_by_username(username))
        response = jsonify(message='Login Succeeded!')
        set_access_cookies(response, access_token, 86400)
        return response
    else:
        return jsonify(message='Bad username or password'), 401


@app.route('/logout', endpoint='logout', methods=['GET'])
@jwt_required(locations='cookies')
def logout():
    """
    Logout
    :return:
    """
    response = jsonify(message='Logout Succeeded')
    unset_access_cookies(response)
    return response


@app.route('/create-user-with-all-details', endpoint='create_user_with_all_details', methods=['POST'])
def create_user_with_all_details():
    """
    Create a new user with the provided credentials and details
    :return:
    """
    if not request.is_json:
        print('uri=/login error="Missing JSON in request"')
        return jsonify({"msg": "Missing JSON in request"}), 400

    print('JSON received: {}'.format(request.json))
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        first_name = request.json.get('firstName', None)
        last_name = request.json.get('lastName', None)
        user_type = request.json.get('userType', None)
        shelter_name = request.json.get('shelterName', None)
        dispositions = request.json.get('dispositions', None)
        good_with_animals = request.json.get('goodWithAnimals', None)
        good_with_children = request.json.get('goodWithChildren', None)
        animal_leashed = request.json.get('animalLeashed', None)
        animal_preference = request.json.get('animalPreference', None)
    except Exception as e:
        return jsonify({"msg": '{}'.format(e)}), 499

    if not username:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        print('uri=/login error="Missing password parameter"')
        return jsonify({"msg": "Missing password parameter"}), 400
    if not first_name:
        print('uri=/login error="Missing first name parameter"')
        return jsonify({"msg": "Missing first name parameter"}), 400
    if not last_name:
        print('uri=/login error="Missing last name parameter"')
        return jsonify({"msg": "Missing last name parameter"}), 400
    if not user_type:
        print('uri=/login error="Missing user type parameter"')
        return jsonify({"msg": "Missing user type parameter"}), 400
    if user_type == 'shelter worker':
        if not shelter_name:
            print('uri=/login error="Missing shelter name parameter for shelter worker"')
            return jsonify({"msg": "Missing shelter name parameter for shelter worker"}), 400

    response = {
        'create_user_result': False,
        'create_user_detail_result': False,
        'assign user as adopter': False,
        'assign_user_to_shelter': False,
        'assign_dispositions': False,
        'animal_preference': False
    }

    new_user = User()
    create_user_result = new_user.create_user(username=username, password=password)

    response['create_user_result'] = create_user_result

    existing_user_detail = UserDetail.get_user_detail(username)

    if not existing_user_detail:
        new_user_detail = UserDetail()
        create_user_detail_result = new_user_detail.create_user_detail(
            username=username,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )
        response['create_user_detail_result'] = create_user_detail_result

    if user_type == 'adopter':
        try:
            assign_adopter_result = Adopter.assign_user_by_username(username)
            response['assign user as adopter'] = assign_adopter_result
        except Exception as e:
            return jsonify(message=e), 500

        print('Animal preference parsed: {}'.format(animal_preference))
        if animal_preference:
            try:
                adopter = Adopter.get_adopter_by_name(username)
                assign_animal_preference_result = adopter.assign_animal_preference_by_name(animal_preference)
                response['animal_preference'] = assign_animal_preference_result
            except Exception as e:
                return jsonify(message=e), 501
        else:
            return jsonify(message='Animal preference required for adopter'), 502
    elif user_type == 'shelter worker':
        if shelter_name:
            assign_shelter_worker_result = ShelterWorker.assign_user_by_username(username, shelter_name)
            response['assign_user_to_shelter'] = assign_shelter_worker_result
            if assign_shelter_worker_result:
                print('User {} assigned to shelter {}'.format(username, shelter_name))
    else:
        return jsonify(message='User type {} not found'.format(user_type)), 503

    if not dispositions:
        dispositions = []
        if good_with_animals:
            dispositions.append('Good with other animals')
        if good_with_children:
            dispositions.append('Good with children')
        if animal_leashed:
            dispositions.append('Animal must be leashed at all times')

    if UserDetail.get_user_detail(username):
        try:
            dispo_result = UserDetail.update_user_dispositions(
                username=username,
                dispositions=dispositions
            )
            response['assign_dispositions'] = dispo_result
        except Exception as e:
            return jsonify(message=e), 504
    else:
        response['assign_dispositions'] = False

    if response['create_user_result'] and response['create_user_detail_result']:
        return jsonify(message=response), 200
    else:
        return jsonify(message=response), 505


@app.route('/get-user-details', endpoint='get-user-details', methods=['GET'])
@jwt_required(locations='cookies')
def get_user_details():
    """
    Get details for a specified user
    :return:
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400

    try:
        username = User.get_username_by_id(current_user)
        result = UserDetail.get_printable_user_detail(username)

        if result['userType'] == 'adopter':
            animal_preference = Adopter.get_animal_preference(username)
            result['animalPreference'] = animal_preference

            dispositions = UserDetail.get_user_dispositions(User.get_username_by_id(current_user))
            result['dispositions'] = dispositions['dispositions']
        elif result['userType'] == 'shelter worker':
            result['shelter'] = ShelterWorker.get_shelter_by_username(username)

    except Exception as e:
        return jsonify(message='{}'.format(e)), 510

    if result:
        return jsonify(message=result), 200
    else:
        return jsonify(message='User {} not found'.format(username)), 511


@app.route('/update-user-details', endpoint='update-user-details', methods=['POST'])
@jwt_required(locations='cookies')
def update_user_details():
    """
    Update details for user that does exist
    :return:
    """
    current_user = get_jwt_identity()
    if not current_user:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400

    if not request.is_json:
        print('uri=/login error="Missing JSON in request"')
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    first_name = request.json.get('firstName', None)
    last_name = request.json.get('lastName', None)
    dispositions = request.json.get('dispositions', None)
    good_with_animals = request.json.get('goodWithAnimals', None)
    good_with_children = request.json.get('goodWithChildren', None)
    animal_leashed = request.json.get('animalLeashed', None)
    animal_preference = request.json.get('animalPreference', None)

    if not username:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400
    if not first_name:
        print('uri=/login error="Missing first name parameter"')
        return jsonify({"msg": "Missing first name parameter"}), 400
    if not last_name:
        print('uri=/login error="Missing last name parameter"')
        return jsonify({"msg": "Missing last name parameter"}), 400

    response = {
        'update_user_detail_result': False,
        'update_dispositions': False,
        'update_preference': False
    }

    if UserDetail.get_user_detail(User.get_username_by_id(current_user)):
        result = UserDetail.update_user_detail(
            current_user,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        if result:
            response['update_user_detail_result'] = result

    if animal_preference:
        adopter = Adopter.get_adopter_by_name(username)
        assign_animal_preference_result = adopter.assign_animal_preference_by_name(animal_preference)
        response['animal_preference'] = assign_animal_preference_result

    if not dispositions:
        dispositions = []
        if good_with_animals:
            dispositions.append('Good with other animals')
        if good_with_children:
            dispositions.append('Good with children')
        if animal_leashed:
            dispositions.append('Animal must be leashed at all times')

    if UserDetail.get_user_detail(username):
        dispo_result = UserDetail.update_user_dispositions(
            username=username,
            dispositions=dispositions
        )
        response['assign_dispositions'] = dispo_result
    else:
        response['assign_dispositions'] = False

    if response['update_user_detail_result'] or response['update_dispositions'] or response['update_preference']:
        return jsonify(message=response), 200
    else:
        return jsonify(message=response), 500


@app.route('/update-user-dispositions', endpoint='update-user-dispositions', methods=['POST'])
@jwt_required(locations='cookies')
def update_user_dispositions():
    """
    Update dispositions for a specific user
    :return:
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400

    if not request.is_json:
        print('uri=/login error="Missing JSON in request"')
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = User.get_username_by_id(current_user)
    dispositions = request.json.get('dispositions', None)

    if not dispositions:
        print('uri=/login error="Missing dispositions parameter"')
        return jsonify({"msg": "Missing dispositions parameter"}), 400

    if UserDetail.get_user_detail(username):
        result = UserDetail.update_user_dispositions(
            username=username,
            dispositions=dispositions
        )
    else:
        return jsonify(message='User {} does not exist'.format(username)), 500

    if result:
        return jsonify(message='Dispositions for user {} updated successfully'.format(username)), 200
    else:
        return jsonify(message='User {} detail update failed'.format(username)), 500


@app.route('/get-shelters', endpoint='get_shelter', methods=['GET'])
def get_shelters():
    """
    Return a list of shelters with details
    :return:
    """
    shelters = Shelter.get_shelters()

    if shelters:
        return jsonify(message=shelters), 200
    else:
        return jsonify(message='Failed to get shelters'), 500


@app.route('/assign-user-to-shelter', endpoint='assign_user_to_shelter', methods=['POST'])
@jwt_required(locations='cookies')
def assign_user_to_shelter():
    """
    Route to assign a logged in user to a shelter
    :return:
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing username parameter"')
        return jsonify({"msg": "Missing username parameter"}), 400

    if not request.is_json:
        print('uri=/login error="Missing JSON in request"')
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = User.get_username_by_id(current_user)
    shelter_name = request.json.get('shelter_name', None)

    if not shelter_name:
        print('uri=/assign-user-to-shelter error="Missing shelter parameter"')
        return jsonify({"msg": "Missing shelter parameter"}), 400

    result = ShelterWorker.assign_user_by_username(username, shelter_name)

    if result:
        return jsonify(message='User {} assigned to shelter {} successfully'.format(username, shelter_name)), 200
    else:
        return jsonify(message='User {} assignment to shelter {} failed'.format(username, shelter_name)), 500


@app.route('/create-animal', endpoint='create_animal', methods=['POST'])
@jwt_required(locations='cookies')
def create_animal():
    """
    Route for an authenticated shelter worker to add a new animal to their shelter
    :return:
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    required_args = [
        'name',
        'age',
        'description',
        'animalClass',
        'animalBreed',
        'dispositions',
        'adoptionStatus'
    ]

    try:
        username = User.get_username_by_id(current_user)
        data = json.loads(request.form.get('data'))

        for required_arg in required_args:
            if required_arg not in data.keys():
                return jsonify(message='Missing arg {}'.format(required_arg)), 400

        animal_name = data['name']
        animal_age = data['age']
        description = data['description']
        image = ''
        if 'images' in request.files:
            image = request.files['image']
        animal_class = data['animalClass']
        animal_breed = data['animalBreed']
        dispositions = data['dispositions']
        adoption_status = data['adoptionStatus']
    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 500

    try:
        user_detail = UserDetail.get_printable_user_detail(username)
        print(user_detail, flush=True)
    except Exception as e:
        print(e, flush=True)
        return jsonify(message="{}".format(e)), 501

    if user_detail['userType'] != 'shelter worker':
        return jsonify(message="User is not a shelter worker"), 401
    else:
        try:
            shelter_name = ShelterWorker.get_shelter_by_username(username)
        except Exception as e:
            print(e, flush=True)
            return jsonify(message='{}'.format(e)), 502

    if image and allowed_file(image.filename):
        filename = str(uuid.uuid4()) + secure_filename(image.filename)
        image_path = Path.joinpath(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
    else:
        image_path = ''
        print("Image not found", flush=True)

    try:
        new_animal = Animal()
        result = new_animal.create_animal(
            animal_name,
            animal_age,
            description,
            '{}'.format(image_path),
            animal_class,
            animal_breed,
            adoption_status,
            shelter_name,
            dispositions
        )
    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 504

    return jsonify(message='{}'.format(result)), 200


@app.route('/get-animal-by-details', endpoint='get_animal_by_details', methods=['GET'])
def get_animal_by_details():
    """
    Route to search for and return an animal based on the provided parameters
    """
    animal_name = request.args.get('animalName', None)
    shelter_name = request.args.get('shelterName', None)
    animal_age = request.args.get('animalAge', None)

    try:
        animal = Animal.get_animal_by_name_shelter_age(animal_name, shelter_name, animal_age)
        if animal:
            printable_animal = Animal.object_as_dict(animal)
            print(printable_animal)
            return jsonify(message='{}'.format(printable_animal)), 200
        else:
            message = 'Animal {} not found'.format(animal_name)
            print(message)
        return jsonify(message='{}'.format(message)), 500
    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/get-animals-of-shelter', endpoint='get_animals_of_shelter', methods=['GET'])
@jwt_required(locations='cookies')
def get_animals_of_shelter():
    """
    Route to return a list of all animals of the shelter
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    try:
        shelter_id = ShelterWorker.get_shelter_id_by_user_id(current_user)
        animals = Animal.get_animals_by_shelter_id(shelter_id)
        return jsonify(message='{}'.format(json.dumps(animals))), 200
    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/get-animals', endpoint='get_animals', methods=['GET'])
@jwt_required(locations='cookies')
def get_animals():
    """
    Route to return a list of all animals
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    try:
        animals = Animal.get_animals()
        return jsonify(message='{}'.format(json.dumps(animals))), 200
    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 501


@app.route('/get-matching-animals', endpoint='get_matching_animals', methods=['GET'])
@jwt_required(locations='cookies')
def get_matching_animals():
    """
    Route to return a list of animals available for adoption that match the criteria of
    the logged in user
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    try:
        username = User.get_username_by_id(current_user)
        user_detail = UserDetail.get_printable_user_detail(username)
        dispositions = UserDetail.get_user_dispositions(username)
        animal_preference = AnimalClass.get_animal_class_by_name(Adopter.get_animal_preference(username))
        print('User detail {}'.format(user_detail))
        print('Dispositions {}'.format(dispositions))
        print('Animal preference {}'.format(animal_preference.animal_class))

        matching_animals = Animal.get_animals_by_type_and_disposition(animal_preference, dispositions)

        return jsonify(message='{}'.format(json.dumps(matching_animals))), 200
    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/get-animal-details-by-id', endpoint='get_animal_details_by_id', methods=['GET'])
def get_animal_details_by_id():
    """
    Route to get the details of the specified animal by id
    """
    animal_id = request.args.get('animalId')
    try:
        animal = Animal.object_as_dict(Animal.get_animal_by_id(animal_id))
        return jsonify(animal)
    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/create-animal-news-item', endpoint='create_animal_news_item', methods=['POST'])
@jwt_required(locations='cookies')
def create_animal_news_item():
    """
    Route for an authenticated shelter worker to add a new animal to their shelter
    :return:
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    try:
        username = User.get_username_by_id(current_user)
        animal_id = request.json.get('animalId', None)
        news_text = request.json.get('newsText', None)
        shelter_id = ShelterWorker.get_shelter_id_by_user_id(current_user)
    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 500

    try:
        user_detail = UserDetail.get_printable_user_detail(username)
        print(user_detail, flush=True)
    except Exception as e:
        print(e, flush=True)
        return jsonify(message="{}".format(e)), 501

    if user_detail['userType'] != 'shelter worker':
        return jsonify(message="User is not a shelter worker"), 401

    try:
        animal = Animal.get_animal_by_id(animal_id)
        if animal.shelter_id == shelter_id:
            new_animal_news = AnimalNews()
            result = new_animal_news.create_news_item_for_animal_id(news_text, animal_id)
        else:
            message = 'Animal does not belong to same shelter as shelter worker'
            print(message)
            return jsonify(message='{}'.format(message)), 502
    except Exception as e:
        print(e, flush=True)
        return jsonify(message="{}".format(e)), 503

    return jsonify(message='{}'.format(result)), 200


@app.route('/get-animal-news-by-id', endpoint='get_animal_news_by_id', methods=['GET'])
def get_animal_news_by_id():
    """
    Get all news items for an animal by animal id
    :return:
    """
    animal_id = request.args.get('animalId')
    try:
        animal_news = AnimalNews.get_printable_news_items_by_animal_id(animal_id)
        return jsonify(message=animal_news), 200
    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/get-recent-news-items', endpoint='get_recent_news_items', methods=['GET'])
def get_recent_news_items():
    """
    Get recent news items for all animal. Number of news items specified by newsItemCount
    parameter
    :return:
    """
    news_item_count = request.args.get('newsItemCount') or 3
    try:
        animal_news = AnimalNews.get_printable_news_items_all_animals(news_item_count)
        return jsonify(message=animal_news), 200
    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/update-adoption-status', endpoint='update_adoption_status', methods=['POST'])
@jwt_required(locations='cookies')
def update_adoption_status():
    """
    Route for a shelter worker to update the adoption status of an animal belonging to their shelter
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    animal_id = request.json.get('animalId', None)
    adoption_status = request.json.get('adoptionStatus')

    try:
        username = User.get_username_by_id(current_user)
        user_detail = UserDetail.get_printable_user_detail(username)
        shelter_id = ShelterWorker.get_shelter_id_by_user_id(current_user)

        if user_detail['userType'] == 'shelter worker':
            animal = Animal.get_animal_by_id(animal_id)
            if shelter_id == animal.shelter_id:
                result = Animal.update_adoption_status(animal_id, adoption_status)
                return jsonify(message='{}'.format(result)), 200
            else:
                message = 'Animal {} does not belong to shelter worker {} shelter'.format(animal_id, username)
                print(message)

    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/adopt-animal', endpoint='adopt_animal', methods=['POST'])
@jwt_required(locations='cookies')
def adopt_animal():
    """
    Route for an adopter to adopt an animal
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"')
        return jsonify(message="Missing user"), 400

    animal_id = request.json.get('animalId', None)

    try:
        username = User.get_username_by_id(current_user)
        user_detail = UserDetail.get_printable_user_detail(username)
        if user_detail['userType'] == 'adopter':
            adoption_status = Animal.get_adoption_status(animal_id)
            print(adoption_status)
            if adoption_status == 'Available':
                result = Animal.update_adoption_status(animal_id, 'Pending') \
                    and Animal.set_adopter(animal_id, current_user)
                return jsonify(message='{}'.format(result)), 200
            else:
                message = 'Animal is not available for adoption, adoption status: {}'.format(adoption_status)
                print(message)
                return jsonify(message='{}'.format(message)), 500
        else:
            message = 'User {} is not an adopter. Only adopters can adopt animals'.format(username)
            print(message)
            return jsonify(message='{}'.format(message)), 401

    except Exception as e:
        print(e)
        return jsonify(message='{}'.format(e)), 501


@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required(locations='cookies')
def delete_user(user_id):
    """
    Route for deleting a user by admin
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"', flush=True)
        return jsonify(message="Missing user"), 400

    if not Administrator.is_administrator(current_user):
        print('non-admin user error', flush=True)
        return jsonify(message="You are not allowed to delete other users"), 403

    if user_id == current_user:
        return jsonify(message="You are not allowed to delete yourself"), 403

    try:
        User.delete(user_id)
        return jsonify(message="Delete succeeded"), 200

    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 501

@app.route('/users', methods=['GET'])
@jwt_required(locations='cookies')
def get_users():
    """
    Route for deleting a user by admin
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"', flush=True)
        return jsonify(message="Missing user"), 400

    if not Administrator.is_administrator(current_user):
        print('non-admin user error', flush=True)
        return jsonify(message="Forbidden"), 403

    try:
        users = User.get_users()
        print(users, flush=True)
        return jsonify(message='{}'.format(json.dumps(users))), 200

    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 501

@app.route('/animals/<int:animal_id>', methods=['DELETE'])
@jwt_required(locations='cookies')
def delete_animal(animal_id):
    """
    Route for deleting an animal
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"', flush=True)
        return jsonify(message="Missing user"), 400

    # TODO: check the user is valid shelter worker

    try:
        Animal.delete(animal_id)
        return jsonify(message="Delete succeeded"), 200

    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 501

@app.route('/animals/<int:animal_id>', methods=['PUT'])
@jwt_required(locations='cookies')
def update_animal(animal_id):
    """
    Route for updating an animal profile
    """
    current_user = get_jwt_identity()

    if not current_user:
        print('uri=/login error="Missing user"', flush=True)
        return jsonify(message="Missing user"), 400

    try:
        animal = Animal.get_animal_by_id(animal_id)

        data = json.loads(request.form.get('data'))
        print(data, flush=True)

        image = ''
        if 'image' in request.files:
            image = request.files['image']
        if image and allowed_file(image.filename):
            filename = str(uuid.uuid4()) + secure_filename(image.filename)
            image_path = Path.joinpath(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            image_path = ''

        Animal.update_animal(
            animal_id,
            data['name'] or animal.name,
            data['age'] or animal.age,
            data['description'] or animal.description,
            image_path or animal.image_path,
            data['animalClass'],
            data['animalBreed'],
            data['adoptionStatus'],
            data['dispositions'],
        )

        return jsonify(message="Update succeeded"), 200

    except Exception as e:
        print(e, flush=True)
        return jsonify(message='{}'.format(e)), 501