from datetime import datetime
from animal_adoption import db
from flask_sqlalchemy import inspect
from werkzeug.security import generate_password_hash, \
     check_password_hash


user_disposition_relationship = db.Table(
    'UserDispositionRelationshipTable',
    db.Column('user_detail_id', db.Integer, db.ForeignKey('UserDetailTable.id_user_detail')),
    db.Column('disposition_id', db.Integer, db.ForeignKey('DispositionTable.id_disposition'))
)

animal_disposition_relationship = db.Table(
    'AnimalDispositionRelationshipTable',
    db.Column('animal_id', db.Integer, db.ForeignKey('AnimalTable.id_animal')),
    db.Column('disposition_id', db.Integer, db.ForeignKey('DispositionTable.id_disposition'))
)


class User(db.Model):
    __tablename__ = 'UserTable'
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    def __init__(self):
        self.username = None
        self.password_hash = None

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def create_user(self, username, password):
        """
        Create a new user and hash the password
        :param username:
        :param password:
        :return:
        """
        if not User.get_id_by_username(username):
            self.username = username
            self.hash_password(password)
            db.session.add(self)
            db.session.commit()
            return True
        else:
            print('Username \'{}\' already exists'.format(username))
            return False

    @staticmethod
    def get_id_by_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user.id_user
        else:
            return None

    @staticmethod
    def get_username_by_id(user_id):
        user = User.query.filter_by(id_user=user_id).first()
        if user:
            return user.username
        else:
            return None

    def hash_password(self, password):
        """
        Hash password and store it in instance variable
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check that user provided password when hashed matches the saved password hash
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def authenticate_user(username, password):
        """
        Check if the user exists in the database and verify the hash of the
        supplied password matches the hash in the database
        :param username:
        :param password:
        :return:
        """
        if username is None or password is None:
            raise ValueError('Username and password may not be empty')

        user = User.query.filter_by(username=username).first()
        if user is None:
            raise ValueError('User %s does not exist' % username)

        if not user.check_password(password):
            return False

        return True

    @staticmethod
    def change_username(user_id, username):
        existing_user = User.query.filter_by(id_user=user_id).first()
        existing_user.username = username
        db.session.add(existing_user)
        db.session.commit()

    @staticmethod
    def delete(user_id):
        user = User.query.filter_by(id_user=user_id).first()
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_users():
        users = User.query.all()
        result = []
        for user in users:
            print(user, flush=True)
            obj = {
                column.key: getattr(user, column.key) for column in inspect(user).mapper.column_attrs if column.key != 'password_hash'
            }
            user_detail = UserDetail.get_printable_user_detail(user.username)
            obj.update(user_detail)
            result.append(obj)
        return result


class UserDetail(db.Model):
    __tablename__ = 'UserDetailTable'
    id_user_detail = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('UserTable.id_user'))
    user_type_id = db.Column(db.Integer, db.ForeignKey('UserTypeTable.id_user_type'))
    user_dispositions = db.relationship(
        'Disposition',
        secondary=user_disposition_relationship
    )

    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.user_id = None
        self.user_type_id = None
        self.user_dispositions = []

    def __repr__(self):
        return '<Name: {} {} id: {} type: {} dispositions: {}>'.format(
            self.first_name,
            self.last_name,
            self.user_id,
            self.user_type_id,
            self.user_dispositions
        )

    @staticmethod
    def object_as_dict(obj):
        try:
            return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def get_user_detail(username):
        try:
            user_detail = UserDetail.query.filter_by(user_id=User.get_id_by_username(username)).first()
            return user_detail
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def get_user_detail_by_user_id(user_id):
        try:
            user_detail = UserDetail.query.filter_by(user_id=user_id).first()
            return user_detail
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def get_printable_user_detail(username):
        try:
            user_detail = UserDetail.query.filter_by(user_id=User.get_id_by_username(username)).first()
            if not user_detail:
                return {}
            user_detail_dict = UserDetail.object_as_dict(user_detail)
            name = User.query.filter_by(id_user=user_detail_dict['user_id']).first().username
            user_type = UserType.query.filter_by(id_user_type=user_detail_dict['user_type_id']).first().user_type
            printable_user_details = {
                'username': name,
                'firstName': user_detail_dict['first_name'],
                'lastName': user_detail_dict['last_name'],
                'userType': user_type
            }
            return printable_user_details
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def get_user_dispositions(username):
        try:
            disposition_list = []
            user_detail = UserDetail.get_user_detail(username)
            if user_detail:
                for user_disposition in user_detail.user_dispositions:
                    if user_disposition:
                        disposition_list.append(user_disposition.disposition)
            else:
                raise ValueError('No user detail found for {}'.format(username))

            return {'dispositions': disposition_list}
        except Exception as e:
            raise ValueError('Get user dispositions for {} failed'.format(username))

    def create_user_detail(self, username, first_name, last_name, user_type, shelter=None):
        self.user_id = User.get_id_by_username(username)
        self.user_type_id = UserType.get_user_type_id_by_name(user_type)
        if not UserDetail.get_user_detail(username):
            if self.user_id:
                if self.user_type_id:
                    if not UserDetail.get_user_detail(username):
                        self.first_name = first_name
                        self.last_name = last_name
                        db.session.add(self)
                        db.session.commit()
                        return True
                    else:
                        print('User detail for \'{}\' already exists'.format(username))
                else:
                    print('User type \'{}\' does not exist'.format(user_type))
            else:
                print('Username \'{}\' not found'.format(username))
        else:
            print('Detail for username \'{}\' already exists'.format(username))

        return False

    @staticmethod
    def update_user_detail(user_id, username=None, first_name=None, last_name=None, dispositions=None, shelter=None):
        changed = False
        if not first_name and not last_name and not dispositions:
            print('No fields to update')
        user_detail = UserDetail.get_user_detail(User.get_username_by_id(user_id))
        if user_detail:
            if username:
                if User.get_username_by_id(user_id) != username:
                    changed = True
                    User.change_username(user_id, username)
            if first_name:
                if user_detail.first_name != first_name:
                    changed = True
                    user_detail.first_name = first_name
            if last_name:
                if user_detail.last_name != last_name:
                    changed = True
                    user_detail.last_name = last_name
            if dispositions:
                for disposition in dispositions:
                    changed = True
                    dispo = Disposition.get_disposition_by_name(disposition)
                    user_detail.user_dispositions.append(dispo)
            if changed:
                db.session.add(user_detail)
                db.session.commit()
                return True
            else:
                print('No changes made for \'{}\''.format(username))
                return True
        else:
            print('Username\'{}\' not found to update details'.format(username))

        return False

    @staticmethod
    def update_user_dispositions(username, dispositions):
        changed = False
        available_dispositions = Disposition.get_list_of_dispositions()
        user_detail = UserDetail.get_user_detail(username)
        existing_dispositions = UserDetail.get_user_dispositions(username)
        for existing_disposition in existing_dispositions['dispositions']:
            if existing_disposition not in dispositions:
                dispo = Disposition.get_disposition_by_name(existing_disposition)
                user_detail.user_dispositions.remove(dispo)
                changed = True
        for disposition in dispositions:
            if disposition not in available_dispositions:
                print('Disposition {} not found'.format(disposition))
                return False
            if disposition not in existing_dispositions['dispositions']:
                dispo = Disposition.get_disposition_by_name(disposition)
                user_detail.user_dispositions.append(dispo)
                changed = True

        if changed:
            db.session.add(user_detail)
            db.session.commit()
            return True
        else:
            return False


class UserType(db.Model):
    __tablename__ = 'UserTypeTable'
    id_user_type = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(32))

    def __init__(self):
        self.user_type = None

    def __repr__(self):
        return '<UserType {}>'.format(self.user_type)

    @staticmethod
    def get_user_type_id_by_name(user_type_name):
        user_type_record = UserType.query.filter_by(user_type=user_type_name).first()
        if user_type_record:
            return user_type_record.id_user_type
        else:
            return None

    @staticmethod
    def get_user_type_name_by_id(user_type_id):
        user_type_record = UserType.query.filter_by(id_user_type=user_type_id).first()
        if user_type_record:
            return user_type_record.user_type
        else:
            return None

    def create_user_type(self, name):
        user_type_record = UserType.get_user_type_id_by_name(name)
        if not user_type_record:
            self.user_type = name
            db.session.add(self)
            db.session.commit()
        else:
            print('User type \'{}\' already exists'.format(name))


class Adopter(db.Model):
    __tablename__ = 'AdopterTable'
    id_adopter = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserTable.id_user'))
    animal_preference_id = db.Column(db.Integer, db.ForeignKey('AnimalClassTable.id_animal_class'))

    def __init__(self):
        self.user_id = None
        self.animal_preference_id = None

    @staticmethod
    def get_adopter_by_name(username):
        adopter_user = Adopter.query.filter_by(user_id=User.get_id_by_username(username)).first()
        if adopter_user:
            return adopter_user
        else:
            raise ValueError('User {} not found in adopter table'.format(username))

    @staticmethod
    def assign_user_by_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            if Adopter.query.filter_by(user_id=user.id_user).first():
                raise ValueError('User {} already assigned as adopter'.format(username))
            else:
                new_adopter = Adopter()
                new_adopter.user_id = user.id_user
                db.session.add(new_adopter)
                db.session.commit()
                return True
        else:
            print('User {} not found'.format(username))
            raise ValueError('User {} not found'.format(username))

    @staticmethod
    def assign_user_by_id(user_id):
        user = User.query.filter_by(id_user=user_id).first()
        if user:
            if Adopter.query.filter_by(user_id=user.id_user).first():
                print('User {} already assigned as adopter'.format(user.username))
                return True
            else:
                new_adopter = Adopter()
                new_adopter.user_id = user.id_user
                db.session.add(new_adopter)
                db.session.commit()
                return True
        else:
            print('User id {} not found'.format(user_id))
            return False

    def assign_animal_preference_by_name(self, class_name):
        animal_class = AnimalClass.get_animal_class_by_name(class_name)
        if animal_class:
            self.animal_preference_id = animal_class.id_animal_class
            db.session.add(self)
            db.session.commit()
            return True
        else:
            raise ValueError('Animal class {} not found'.format(class_name))

    @staticmethod
    def get_animal_preference(username):
        try:
            adopter = Adopter.get_adopter_by_name(username)
            if adopter:
                animal_class = AnimalClass.get_animal_class_by_id(adopter.animal_preference_id)
                if animal_class:
                    return animal_class.animal_class
                else:
                    raise ValueError('Animal preference id {} not found for user {}'.format(
                        adopter.animal_preference_id,
                        username
                    ))
        except Exception as e:
            raise ValueError('No adopter row found for user {}'.format(username))


class ShelterWorker(db.Model):
    __tablename__ = 'ShelterWorkerTable'
    id_shelter_worker = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserTable.id_user'))
    shelter_id = db.Column(db.Integer, db.ForeignKey('ShelterTable.id_shelter'))

    def __init__(self):
        self.user_id = None
        self.shelter_id = None

    @staticmethod
    def get_shelter_id_by_user_id(user_id):
        return ShelterWorker.query.filter_by(user_id=user_id).first().shelter_id

    @staticmethod
    def get_shelter_by_username(username):
        try:
            user = User.query.filter_by(username=username).first()
            shelter_worker = ShelterWorker.query.filter_by(user_id=user.id_user).first()
            shelter_name = Shelter.query.filter_by(id_shelter=shelter_worker.shelter_id).first()
            return shelter_name.name
        except Exception as e:
            raise ValueError('{}'.format(e))

    @staticmethod
    def assign_user_by_username(username, shelter_name):
        user = User.query.filter_by(username=username).first()
        user_detail = UserDetail.get_user_detail(username)
        user_type = UserType.get_user_type_name_by_id(user_detail.user_type_id)
        if not user_type == 'shelter worker':
            print('User {} is not a shelter worker'.format(username))
            return False
        shelter = Shelter.query.filter_by(name=shelter_name).first()
        if user:
            if shelter:
                existing_shelter_worker = ShelterWorker.query.filter_by(user_id=user.id_user).first()
                if existing_shelter_worker:
                    if existing_shelter_worker.shelter_id == shelter.id_shelter:
                        print('User {} already assigned as shelter worker for {}'.format(username, shelter_name))
                    else:
                        print('Re-assigning {} from shelter {} to shelter {}'.format(
                            username,
                            Shelter.query.filter_by(id_shelter=existing_shelter_worker.shelter_id).first().name,
                            shelter_name
                        ))
                        existing_shelter_worker.shelter_id = shelter.id_shelter
                        db.session.add(existing_shelter_worker)
                        db.session.commit()
                        return True
                else:
                    new_shelter_worker = ShelterWorker()
                    new_shelter_worker.user_id = user.id_user
                    new_shelter_worker.shelter_id = shelter.id_shelter
                    db.session.add(new_shelter_worker)
                    db.session.commit()
                    return True
            else:
                print('Shelter {} not found'.format(shelter_name))
        else:
            print('User {} not found'.format(username))

        return False


class Administrator(db.Model):
    __tablename__ = 'AdministratorTable'
    id_administrator = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserTable.id_user'))

    def __init__(self):
        self.user_id = None

    @staticmethod
    def assign_user_by_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            existing_administrator = Administrator.query.filter_by(user_id=User.get_id_by_username(username)).first()
            if existing_administrator:
                print('User {} is already an administrator'.format(username))
            else:
                new_admin = Administrator()
                new_admin.user_id = User.get_id_by_username(username)
                db.session.add(new_admin)
                db.session.commit()
        else:
            print('User {} not found'.format(username))

    @staticmethod
    def is_administrator(user_id):
        user_detail = UserDetail.query.filter_by(user_id=user_id).first()
        if user_detail and user_detail.user_type_id == 3:
            return True
        else:
            return False


class Shelter(db.Model):
    __tablename__ = 'ShelterTable'
    id_shelter = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    physical_address = db.Column(db.String(32))
    phone_number = db.Column(db.String(32))
    email_address = db.Column(db.String(32))

    def __init__(self):
        self.name = None
        self.physical_address = None
        self.phone_number = None
        self.email_address = None

    @staticmethod
    def object_as_dict(obj):
        return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}

    @staticmethod
    def get_shelters():
        shelters = Shelter.query.all()
        shelter_list = []
        for shelter in shelters:
            shelter_list.append(Shelter.object_as_dict(shelter))
        return shelter_list

    @staticmethod
    def get_shelter_by_id(shelter_id):
        shelter = Shelter.query.filter_by(id_shelter=shelter_id).first()
        return Shelter.object_as_dict(shelter)

    @staticmethod
    def get_shelter_by_name(name):
        shelter = Shelter.query.filter_by(name=name).first()
        if shelter:
            return shelter
        else:
            print('Shelter {} not found'.format(name))

    def create_new_shelter(self, name, physical_address, phone_number, email_address):
        existing_shelter = Shelter.get_shelter_by_name(name)
        if not existing_shelter:
            self.name = name
            self.physical_address = physical_address
            self.phone_number = phone_number
            self.email_address = email_address
            db.session.add(self)
            db.session.commit()
            return True

        return False


class Animal(db.Model):
    __tablename__ = 'AnimalTable'
    id_animal = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.String(32))
    description = db.Column(db.TEXT)
    image_path = db.Column(db.TEXT)
    creation_date = db.Column(db.DATE)
    animal_class_id = db.Column(db.Integer, db.ForeignKey('AnimalClassTable.id_animal_class'))
    animal_breed_id = db.Column(db.Integer, db.ForeignKey('AnimalBreedTable.id_animal_breed'))
    adoption_status_id = db.Column(db.Integer, db.ForeignKey('AdoptionStatusTable.id_adoption_status'))
    shelter_id = db.Column(db.Integer, db.ForeignKey('ShelterTable.id_shelter'))
    adopter_id = db.Column(db.Integer, db.ForeignKey('AdopterTable.id_adopter'))
    animal_dispositions = db.relationship(
        'Disposition',
        secondary=animal_disposition_relationship
    )
    animal_class = db.relationship('AnimalClass')
    animal_breed = db.relationship('AnimalBreed')

    def __init__(self):
        self.name = None
        self.age = None
        self.description = None
        self.image_path = None
        self.creation_date = datetime.now()
        self.animal_class_id = None
        self.animal_breed_id = None
        self.adoption_status_id = None
        self.shelter_id = None
        self.adopter_id = None
        self.animal_dispositions = []

    def __repr__(self):
        return '<Name: {} age: {} description: {} imagePath: {} classId: {} breedId: {} statusId: {} shelterId: {}' \
               ' dispositions: {}>'.format(
                    self.name,
                    self.age,
                    self.description,
                    self.image_path,
                    self.animal_class_id,
                    self.animal_breed_id,
                    self.adoption_status_id,
                    self.shelter_id,
                    self.animal_dispositions
                )

    @staticmethod
    def object_as_dict(obj):
        try:
            result = {}
            for column in inspect(obj).mapper.column_attrs:
                if column.key == 'creation_date':
                    result[column.key] = (getattr(obj, column.key)).strftime('%Y-%m-%d')
                else:
                    result[column.key] = getattr(obj, column.key)

            # load dispositions
            result['dispositions'] = list(map(lambda x: x.disposition, obj.animal_dispositions))

            # Shelter info
            result['shelter'] = Shelter.get_shelter_by_id(result['shelter_id'])

            # Adopter info
            if obj.adopter_id:
                result['adopter'] = UserDetail.get_printable_user_detail(User.get_username_by_id(obj.adopter_id))

            return result
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def get_animals():
        result = []
        for animal in Animal.query:
            data = Animal.object_as_dict(animal)
            data['animal_class'] = animal.animal_class.animal_class
            data['animal_breed'] = animal.animal_breed.animal_breed
            data['dispositions'] = list(map(lambda x: x.disposition, animal.animal_dispositions))
            result.append(data)
        return result

    @staticmethod
    def get_animal_by_name_shelter_age(animal_name, animal_shelter, animal_age):
        animals_with_name = Animal.query.filter_by(name=animal_name)
        for animal in animals_with_name:
            if animal.shelter_id == Shelter.get_shelter_by_name(animal_shelter).id_shelter:
                if animal.age == animal_age:
                    return animal

        return None

    @staticmethod
    def get_animal_by_id(animal_id):
        animal = Animal.query.filter_by(id_animal=int(animal_id)).first()

        return animal

    @staticmethod
    def get_animals_by_shelter_id(shelter_id):
        animals = Animal.query.filter_by(shelter_id=shelter_id).all()
        return list(map(lambda x: Animal.object_as_dict(x), animals))

    @staticmethod
    def get_animals_by_type_and_disposition(animal_class, dispositions):
        matching_animals = []
        animals = Animal.query.filter_by(animal_class_id=animal_class.id_animal_class)
        for animal in animals:
            animal_dispositions = []
            for animal_disposition in animal.animal_dispositions:
                animal_dispositions.append(animal_disposition.disposition)

            matching_dispositions = [x for x in dispositions['dispositions'] if x in animal_dispositions]
            if matching_dispositions:
                matching_animals.append(Animal.object_as_dict(animal))

        return matching_animals

    @staticmethod
    def get_animal_dispositions_as_list(animal_obj):
        dispositions = []
        for disposition in animal_obj.animal_dispositions:
            dispositions.append(disposition)

    def create_animal(self, name, age, description, image_path, animal_class, animal_breed,
                      adoption_status, shelter, dispositions):
        """
        Method to create a new animal for a shelter #todo add duplicate checking
        """
        self.name = name
        self.age = age
        self.description = description
        self.image_path = image_path
        self.animal_class_id = AnimalClass.get_animal_class_by_name(animal_class).id_animal_class
        self.animal_breed_id = AnimalBreed.get_animal_breed_by_name(animal_breed).id_animal_breed
        self.adoption_status_id = AdoptionStatus.get_adoption_status_by_name(adoption_status).id_adoption_status
        self.shelter_id = Shelter.get_shelter_by_name(shelter).id_shelter
        for disposition in dispositions:
            self.animal_dispositions.append(Disposition.get_disposition_by_name(disposition))

        db.session.add(self)
        db.session.commit()

        return True

    @staticmethod
    def update_animal(animal_id, name, age, description, image_path, animal_class, animal_breed,
                      adoption_status, dispositions):
        """
        Method to update an animal profile
        """
        animal = Animal.get_animal_by_id(animal_id)
        animal.name = name
        animal.age = age
        animal.description = description
        animal.image_path = image_path
        animal.animal_class_id = AnimalClass.get_animal_class_by_name(animal_class).id_animal_class
        animal.animal_breed_id = AnimalBreed.get_animal_breed_by_name(animal_breed).id_animal_breed
        animal.adoption_status_id = AdoptionStatus.get_adoption_status_by_name(adoption_status).id_adoption_status

        # sync dispositions to new dispositions
        for disposition in dispositions:
            animal.animal_dispositions.append(Disposition.get_disposition_by_name(disposition))

        db.session.commit()

        return True

    @staticmethod
    def get_adoption_status(animal_id):
        animal = Animal.get_animal_by_id(animal_id)
        adoption_status = AdoptionStatus.get_adoption_status_by_id(animal.adoption_status_id)

        return adoption_status.adoption_status

    @staticmethod
    def update_adoption_status(animal_id, adoption_status):
        animal = Animal.get_animal_by_id(animal_id)
        animal.adoption_status_id = AdoptionStatus.get_adoption_status_by_name(adoption_status).id_adoption_status
        db.session.add(animal)
        db.session.commit()

        return True

    @staticmethod
    def set_adopter(animal_id, adopter_id):
        animal = Animal.get_animal_by_id(animal_id)
        animal.adopter_id = adopter_id
        db.session.add(animal)
        db.session.commit()

        return True
    
    @staticmethod
    def delete(animal_id):
        animal = Animal.query.filter_by(id_animal=animal_id).first()
        db.session.delete(animal)
        db.session.commit()


class AnimalNews(db.Model):
    __tablename__ = 'AnimalNewsTable'
    id_animal_news = db.Column(db.Integer, primary_key=True)
    news_item = db.Column(db.TEXT)
    creation_date = db.Column(db.TIMESTAMP)
    animal_id = db.Column(db.Integer, db.ForeignKey('AnimalTable.id_animal'))

    def __init__(self):
        self.news_item = None
        self.creation_date = datetime.now()

    def create_news_item_for_animal_id(self, news_text, animal_id):
        self.news_item = news_text
        self.animal_id = animal_id
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_news_items_by_animal_id(animal_id):
        news_items = AnimalNews.query.filter_by(animal_id=animal_id)
        return news_items

    @staticmethod
    def get_printable_news_items_by_animal_id(animal_id):
        printable_news = []
        news_items = AnimalNews.query.filter_by(animal_id=animal_id)

        for news in news_items:
            current_printable_item = {}
            current_printable_item['id'] = news.id_animal_news
            current_printable_item['text'] = news.news_item
            current_printable_item['date'] = news.creation_date.strftime("%d/%m/%Y %H:%M:%S")
            printable_news.append(current_printable_item)

        return printable_news

    @staticmethod
    def get_printable_news_items_all_animals(news_item_count):
        printable_news = []
        news_items = AnimalNews.query.order_by(AnimalNews.creation_date.desc()).limit(int(news_item_count))

        for news in news_items:
            current_printable_item = {
                'id': news.id_animal_news,
                'animal_id': news.animal_id,
                'text': news.news_item,
                'date': news.creation_date.strftime("%d/%m/%Y %H:%M")
            }
            printable_news.append(current_printable_item)

        return printable_news


class Disposition(db.Model):
    __tablename__ = 'DispositionTable'
    id_disposition = db.Column(db.Integer, primary_key=True)
    disposition = db.Column(db.String(256))

    def __init__(self):
        self.disposition = None

    def create_disposition(self, name):
        if not Disposition.get_disposition_by_name(name):
            self.disposition = name
            db.session.add(self)
            db.session.commit()
        else:
            print('Animal disposition \'{}\' already exists'.format(name))

    @staticmethod
    def get_list_of_dispositions():
        disposition_names = []

        dispositions = Disposition.query.all()
        for disposition in dispositions:
            disposition_names.append(disposition.disposition)

        return disposition_names

    @staticmethod
    def get_disposition_by_name(disposition_name):
        disposition_record = Disposition.query.filter_by(disposition=disposition_name).first()
        if disposition_record:
            return disposition_record
        else:
            return None

    @staticmethod
    def get_disposition_by_id(disposition_id):
        disposition_record = Disposition.query.filter_by(id_disposition=disposition_id).first()
        if disposition_record:
            return disposition_record
        else:
            return None


class AnimalClass(db.Model):
    __tablename__ = 'AnimalClassTable'
    id_animal_class = db.Column(db.Integer, primary_key=True)
    animal_class = db.Column(db.String(32))

    def __init__(self):
        self.animal_class = None

    def add_animal_class(self, name):
        if not AnimalClass.get_animal_class_by_name(name):
            self.animal_class = name
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def get_animal_class_by_name(name):
        animal_class = AnimalClass.query.filter_by(animal_class=name).first()
        if animal_class:
            return animal_class
        else:
            print('Animal class {} not found'.format(name))
            return None

    @staticmethod
    def get_animal_class_by_id(class_id):
        animal_class = AnimalClass.query.filter_by(id_animal_class=class_id).first()
        if animal_class:
            return animal_class
        else:
            print('Animal class {} not found'.format(class_id))
            return None


class AnimalBreed(db.Model):
    __tablename__ = 'AnimalBreedTable'
    id_animal_breed = db.Column(db.Integer, primary_key=True)
    animal_breed = db.Column(db.String(32))
    animal_class_id = db.Column(db.Integer, db.ForeignKey('AnimalClassTable.id_animal_class'))

    def __init__(self):
        self.animal_breed = None
        self.animal_class_id = None

    def add_animal_breed(self, class_name, breed_name):
        class_id = AnimalClass.get_animal_class_by_name(class_name)
        if class_id:
            self.animal_class_id = class_id.id_animal_class
            self.animal_breed = breed_name
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def get_animal_breed_by_name(breed_name):
        breed = AnimalBreed.query.filter_by(animal_breed=breed_name).first()
        if breed:
            return breed
        else:
            print('Breed name {} not found'.format(breed_name))
            return None

    @staticmethod
    def get_all_animal_breeds():
        breed_list = []
        breeds = AnimalBreed.query.all()
        if breeds:
            for breed in breeds:
                breed_list.append(breed.animal_breed)
            return breed_list

        return None

    @staticmethod
    def get_all_animal_breeds_by_class(class_name):
        breed_list = []
        breeds = AnimalBreed.query.filter_by(
            animal_class_id=AnimalClass.get_animal_class_by_name(class_name).id_animal_class
        )
        for breed in breeds:
            breed_list.append(breed.animal_breed)

        return breed_list


class AdoptionStatus(db.Model):
    __tablename__ = 'AdoptionStatusTable'
    id_adoption_status = db.Column(db.Integer, primary_key=True)
    adoption_status = db.Column(db.String(32))

    def __init__(self):
        self.adoption_status = None

    @staticmethod
    def get_adoption_status_by_name(name):
        adoption_status = AdoptionStatus.query.filter_by(adoption_status=name).first()
        if adoption_status:
            return adoption_status
        else:
            print('Adoption status {} not found'.format(name))

    @staticmethod
    def get_adoption_status_by_id(adoption_status_id):
        adoption_status = AdoptionStatus.query.filter_by(id_adoption_status=adoption_status_id).first()
        if adoption_status:
            return adoption_status
        else:
            print('Adoption status {} not found'.format(adoption_status_id))

    def create_adoption_status(self, adoption_status_name):
        if not AdoptionStatus.get_adoption_status_by_name(adoption_status_name):
            self.adoption_status = adoption_status_name
            db.session.add(self)
            db.session.commit()
