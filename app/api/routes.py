from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}
#works! 
#Using Insomnia, add a GET request to make sure we're actually passing through the request
#http://127.0.0.1:5000/api/getdata

@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)
    #when we populate our data, we'll actually get a confirmation of the data we sent, when we look at Insomnia
    
# In this case, we're checking if the user is allowed to see the data, then querying the Contact data table and retrieving all the data, then saving it to contacts.
@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)


# SEE SPECIFIC CONTACT 

@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_contact_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        contact = Contact.query.get(id)
        response = contact_schema.dump(contact)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


#trying to use Insomnia to add to the contact list
# http://127.0.0.1:5000/contacts 404 Not Found
#It should have been a 401 
#but like we didnt send the token ig

#First, we'll have a Content-Type header with the value application/json. 
# The second header will be ' x-access-token ' with the value 'Bearer 456765676' 
# (Be aware that I just typed random numbers here. You will copy-paste YOUR token!!! NOT! MINE! in after Bearer)

# So if in HELPERS.PY...
#   if 'x-access-token' in request.headers:
            # token = request.headers['x-access-token'].split(' ')[1]
                        # find the Key (x access token) and the Bearer (value) 

# http://127.0.0.1:5000/api/contacts
# Bearer 62bd59e8c4317c0bc75515b064a9fdd5461275fc8c647e3f

# It works! POST 200 
# User fakeemail@code.com has been added to the database
# BIG TESTER: 62bd59e8c4317c0bc75515b064a9fdd5461275fc8c647e3f

# Now we try to GET contact, which is essentially the same steps
#  we get back a list


# UPDATE CONTACT !!!!!!!!

@api.route('/contacts/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)


# DELETE FROM CONTACT !!!!!!!!

@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# x-access-token
# Bearer OwsMvxer01PdR1Yp8-_8SZ9jsqAd_UQPrKS4euJx6IY
# http://127.0.0.1:5000/api/contacts/OwsMvxer01PdR1Yp8-_8SZ9jsqAd_UQPrKS4euJx6IY