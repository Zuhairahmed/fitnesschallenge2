from animal_adoption import (
    app, User, UserType, UserDetail,
    Disposition, Shelter, Adopter, ShelterWorker,
    Administrator, AnimalClass, AdoptionStatus,
    AnimalBreed, Animal, AnimalNews
)


def create_users():
    users = [
        {'username': 'johndoe@abc.com', 'password': 'test1'},
        {'username': 'jimdoe@abc.com', 'password': 'test2'},
        {'username': 'jeandoe@abc.com', 'password': 'test3'},
        {'username': 'admin@abc.com', 'password': 'test4'},
        {'username': 'test@abc.com', 'password': 'test5'},
    ]

    for user in users:
        new_user = User()
        new_user.create_user(user['username'], user['password'])


def create_user_types():
    user_types = [
        'adopter',
        'shelter worker',
        'administrator',
    ]

    for user_type in user_types:
        new_user_type = UserType()
        new_user_type.create_user_type(user_type)


def create_dispositions():
    dispositions = [
        'Good with other animals',
        'Good with children',
        'Animal must be leashed at all times'
    ]

    for disposition in dispositions:
        new_dispo = Disposition()
        new_dispo.create_disposition(disposition)


def create_shelters():
    shelters = [
        {
            'name': 'Critters and Creatures',
            'physical_address': '123 Bark Ave',
            'phone_number': '123-456-7890',
            'email_address': 'info@candc.com'
        },
        {
            'name': 'Creature Comforts',
            'physical_address': '555 Feline Way',
            'phone_number': '999-867-5309',
            'email_address': 'adopt@creaturecomforts.com'
        },
        {
            'name': 'Save a Pet',
            'physical_address': '789 Rover Pkwy',
            'phone_number': '111-222-3456',
            'email_address': 'rescue@saveapet.com'
        }
    ]

    for shelter in shelters:
        new_shelter = Shelter()
        result = new_shelter.create_new_shelter(
            shelter['name'],
            shelter['physical_address'],
            shelter['phone_number'],
            shelter['email_address']
        )
        print('Create new shelter {}: {}'.format(shelter['name'], result))


def create_animal_classes():
    animal_classes = [
        'dog',
        'cat',
        'other'
    ]

    for animal_class in animal_classes:
        new_animal_class = AnimalClass()
        new_animal_class.add_animal_class(animal_class)


def create_animal_breeds():
    breeds = [
        {
            'name': 'golden retriever',
            'class': 'dog'
        },
        {
            'name': 'border collie',
            'class': 'dog'
        },
        {
            'name': 'boxer',
            'class': 'dog'
        },
        {
            'name': 'tabby',
            'class': 'cat'
        },
        {
            'name': 'bengal',
            'class': 'cat'
        },
        {
            'name': 'other',
            'class': 'other'
        }
    ]

    for breed in breeds:
        new_breed = AnimalBreed()
        new_breed.add_animal_breed(breed['class'], breed['name'])

    print(AnimalBreed.get_all_animal_breeds())
    print(AnimalBreed.get_all_animal_breeds_by_class('dog'))


def create_adoption_status():
    adoption_statuses = [
        'Not Available',
        'Available',
        'Pending',
        'Adopted'
    ]

    for adoption_status in adoption_statuses:
        new_adoption_status = AdoptionStatus()
        new_adoption_status.create_adoption_status(adoption_status)


def create_user_details():
    user_details = [
        {
            'username': 'johndoe@abc.com',
            'first_name': 'john',
            'last_name': 'doe',
            'user_type': 'adopter'
        },
        {
            'username': 'janedoe@abc.com',
            'first_name': 'jane',
            'last_name': 'doe',
            'user_type': 'adopter'
        },
        {
            'username': 'jimdoe@abc.com',
            'first_name': 'jim',
            'last_name': 'doe',
            'user_type': 'invalid'
        },
        {
            'username': 'jimdoe@abc.com',
            'first_name': 'jim',
            'last_name': 'doe',
            'user_type': 'shelter worker'
        },
        {
            'username': 'jeandoe@abc.com',
            'first_name': 'jean',
            'last_name': 'doe',
            'user_type': 'administrator'
        },
        {
            'username': 'test@abc.com',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'shelter worker'
        }
    ]

    for user_detail in user_details:
        new_user_detail = UserDetail()
        new_user_detail.create_user_detail(
            user_detail['username'],
            user_detail['first_name'],
            user_detail['last_name'],
            user_detail['user_type']
        )


def update_user_details():
    user_updates = [
        {
            'username': 'johndoe@abc.com',
            'first_name': 'john',
            'last_name': 'doe',
            'dispositions': []
        },
        {
            'username': 'janedoe@a.com',
            'first_name': 'jane',
            'last_name': 'doe',
            'dispositions': []
        },
        {
            'username': 'jimdoe@abc.com',
            'first_name': 'jim',
            'last_name': 'doe',
            'dispositions': ['Good with other animals']
        },
        {
            'username': 'jeandoe@abc.com',
            'first_name': 'jean',
            'last_name': 'doe',
            'dispositions': []
        }
    ]

    try:
        for user_update in user_updates:
            UserDetail.update_user_detail(
                User.get_id_by_username(user_update['username']),
                user_update['username'],
                user_update['first_name'],
                user_update['last_name'],
                user_update['dispositions']
            )
            print(UserDetail.get_user_detail(user_update['username']))
            print(UserDetail.get_user_dispositions(user_update['username']))
    except Exception as e:
        print(e)


def assign_animal_preferences():
    animal_preferences = [
        {
            'name': 'johndoe@abc.com',
            'preference': 'dog'
        },
        {
            'name': 'jimdoe@abc.com',
            'preference': 'cat'
        }
    ]

    for animal_preference in animal_preferences:
        adopter = Adopter.get_adopter_by_name(animal_preference['name'])
        adopter.assign_animal_preference_by_name(animal_preference['preference'])


def assign_adopters():
    Adopter.assign_user_by_username('johndoe@abc.com')
    Adopter.assign_user_by_id(User.get_id_by_username('jimdoe@abc.com'))


def assign_shelter_workers():
    ShelterWorker.assign_user_by_username('jeandoe@abc.com', 'Save a Pet')
    ShelterWorker.assign_user_by_username('jeandoe@abc.com', 'Creature Comforts')
    ShelterWorker.assign_user_by_username('test@abc.com', 'Creature Comforts')


def assign_administrators():
    Administrator.assign_user_by_username('admin@abc.com')


def create_animals():
    animals = [
        {
            'name': 'Fido',
            'age': '2',
            'description': 'Fido is a 2 year old Golden Retriever that loves children and '
                           'going on car rides.',
            'image': 'animal_adoption/front_end/public/img/sample/sample04.jpeg',
            'animal_class': 'dog',
            'animal_breed': 'golden retriever',
            'adoption_status': 'Available',
            'shelter': 'Creature Comforts',
            'dispositions': [
                'Good with other animals',
                'Good with children'
            ]
        },
        {
            'name': 'Boots',
            'age': '5',
            'description': 'Boots is a 5 year old Tabby that likes big families, but takes '
                           'time to warm up to other animals.',
            'image': 'animal_adoption/front_end/public/img/sample/sample05.jpeg',
            'animal_class': 'cat',
            'animal_breed': 'tabby',
            'adoption_status': 'Pending',
            'shelter': 'Critters and Creatures',
            'dispositions': [
                'Good with children'
            ]
        },
        {
            'name': 'Rex',
            'age': '3',
            'description': 'Rex is a 3 year old Boxer that likes to be left alone.',
            'image': 'animal_adoption/front_end/public/img/sample/sample06.jpeg',
            'animal_class': 'dog',
            'animal_breed': 'boxer',
            'adoption_status': 'Available',
            'shelter': 'Creature Comforts',
            'dispositions': [
                'Animal must be leashed at all times'
            ]
        },
        {
            'name': 'Michael',
            'age': '7',
            'description': 'Michael is a 7 year old Bengal that is happiest outside.',
            'image': 'animal_adoption/front_end/public/img/sample/sample07.jpeg',
            'animal_class': 'dog',
            'animal_breed': 'bengal',
            'adoption_status': 'Available',
            'shelter': 'Save a Pet',
            'dispositions': [
                'Good with other animals'
            ]
        },
        {
            'name': 'Snickers',
            'age': '2',
            'description': 'Snickers is a 2 year old Ferret that loves playing and sneaking '
                           'around the house.',
            'image': 'animal_adoption/front_end/public/img/sample/sample08.jpeg',
            'animal_class': 'other',
            'animal_breed': 'other',
            'adoption_status': 'Available',
            'shelter': 'Critters and Creatures',
            'dispositions': [
                'Good with children',
                'Good with other animals'
            ]
        },
        {
            'name': 'Ada',
            'age': '15',
            'description': 'Ada is a 15 year old Cockatiel that likes to sing and is happiest '
                           'when she is outside of her cage.',
            'image': 'animal_adoption/front_end/public/img/sample/sample09.jpeg',
            'animal_class': 'other',
            'animal_breed': 'other',
            'adoption_status': 'Available',
            'shelter': 'Save a Pet',
            'dispositions': [
                'Good with children'
            ]
        },
    ]

    for animal in animals:
        new_animal = Animal()
        new_animal.create_animal(
            animal['name'],
            animal['age'],
            animal['description'],
            animal['image'],
            animal['animal_class'],
            animal['animal_breed'],
            animal['adoption_status'],
            animal['shelter'],
            animal['dispositions']
        )


def create_news_items():
    news_items = [
        {
            'animal_id': '1',
            'text': 'news item 1 for animal 1'
        },
        {
            'animal_id': '1',
            'text': 'news item 2 for animal 1'
        },
        {
            'animal_id': '2',
            'text': 'news item 1 for animal 2'
        },
    ]

    for news_item in news_items:
        print(news_item)
        new_animal_news = AnimalNews()
        new_animal_news.create_news_item_for_animal_id(news_item['text'], news_item['animal_id'])

    animal_news = AnimalNews.get_news_items_by_animal_id(1)
    for i in animal_news:
        print(i.news_item)

    printable_animal_news = AnimalNews.get_printable_news_items_by_animal_id(1)
    for i in printable_animal_news:
        print(i)


def initialize_db():
    print('Creating users')
    create_users()
    print('Creating user types')
    create_user_types()
    print('Creating dispositions')
    create_dispositions()
    print('Creating shelters')
    create_shelters()
    print('Creating animal classes')
    create_animal_classes()
    print('Creating animal breeds')
    create_animal_breeds()
    print('Creating adoption statuses')
    create_adoption_status()
    print('Creating user details')
    create_user_details()
    print('Updating user details')
    update_user_details()
    print('Assigning users as adopters')
    assign_adopters()
    print('Assigning shelter workers')
    assign_shelter_workers()
    print('Assigning animal preferences to adopters')
    assign_animal_preferences()
    print('Creating animals')
    create_animals()
    print('Creating animal news items')
    create_news_items()


if __name__ == '__main__':
    with app.app_context():
        initialize_db()
