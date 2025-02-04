from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication




import random
import string
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from .models import CustomUser

def generate_secure_password(length=8):
    """Generate a secure password with at least one uppercase letter, lowercase letter, number, and special character."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*(),.?\":{}|<>")

    # Generate the remaining characters randomly
    remaining = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>", k=length - 4))

    # Combine and shuffle the characters
    password = upper + lower + digit + special + remaining
    password = ''.join(random.sample(password, len(password)))
    return password

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    phone_number = request.data.get('phone')
    email = request.data.get('email')
    role = request.data.get('role')

    # Basic validations
    if not phone_number or not email or not role:
        return Response({"error": "Phone number, email and role are required."}, status=400)

    # Check if the phone number or email already exists
    if CustomUser.objects.filter(phone_number=phone_number).exists():
        return Response({"error": "A user with this phone number already exists."}, status=400)
    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "A user with this email already exists."}, status=400)

    try:
        # Generate a secure password
        password = generate_secure_password()



        # Hash the password
        hashed_password = make_password(password)

        # Create the user
        user = CustomUser.objects.create_user(
            phone_number=phone_number,
            email=email,
            role=role,
            password=hashed_password
        )

        user.save()

        # Send the password to the user's email
        send_mail(
            subject="Your Account Password",
            message=f"Hello, Your account has been created in Disaster-Guard-App. \nYour password is: {password}",
            from_email="no-reply@disasterGuard.com",
            recipient_list=[email],
        )

        return Response({"message": "User registered successfully."}, status=201)

    except IntegrityError:
        return Response({"error": "A user with this phone number or email already exists."}, status=400)






@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Basic validations
    if not email or not password:
        return Response({"error": "Email and password are required."}, status=400)
    
    print(f"\n Submitted data: \n Email: {email} \n Password: {password} \n")

    try:
        # First check if user exists
        user_exists = CustomUser.objects.filter(email=email).exists()
        if not user_exists:
            return Response({"error": "No user found with this email."}, status=401)

        # Then try to authenticate
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return Response({"error": "Invalid password."}, status=401)

        if not user.is_active:
            return Response({"error": "This account is inactive."}, status=401)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            "id": user.id,
            "phone_number": user.phone_number,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "message": "Login successful."
        }, status=200)

    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response({"error": "An error occurred during login."}, status=500)













import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import CustomUser

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    phone_number = request.data.get('email')
    new_password = request.data.get('new_password')

    # Basic validation
    if not phone_number:
        return Response({"error": "Email is required."}, status=400)

    if not new_password:
        return Response({"error": "New password is required."}, status=400)
    
    
    print("\n Submitted data\n ")
    print("=" * 20)
    print(f" Email: {phone_number}\n Password: {new_password}\n")

    # Validate password strength
    if len(new_password) < 6:
        return Response({"error": "Password must be at least 6 characters long."}, status=400)
    if not re.search(r"[A-Z]", new_password):
        return Response({"error": "Password must contain at least one uppercase letter."}, status=400)
    if not re.search(r"[a-z]", new_password):
        return Response({"error": "Password must contain at least one lowercase letter."}, status=400)
    if not re.search(r"[0-9]", new_password):
        return Response({"error": "Password must contain at least one number."}, status=400)
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
        return Response({"error": "Password must contain at least one special character."}, status=400)

    try:
        # Find the user
        user = CustomUser.objects.get(email=phone_number)
        
    
        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Send the new password to the user's email
        send_mail(
            subject="Your New Password",
            message=f"Your password has been reset. Your new password is: {new_password}",
            from_email="no-reply@disasterGuard.com",
            recipient_list=[user.email],
        )
        
        print('Password Changed successfully and can now login')

        return Response({"message": "Password reset successfully. A confirmation has been sent to your email."}, status=200)

    except CustomUser.DoesNotExist:
        return Response({"error": "User with this phone number does not exist."}, status=404)






from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication




# Delete a user by ID (admin only)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_by_id(request, user_id):
    
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=200)
    except ObjectDoesNotExist:
        return Response({"error": "User with the given ID does not exist."}, status=404)





from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser  # Adjust this import as per your project structure

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    phone_number = request.data.get('phone_number')
    email = request.data.get('email')
    role = request.data.get('role')

    # Validate required fields
    if not phone_number or not email or not role:
        return Response({"message": "Phone number, email, and role are required for updating a user."}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)

        # Check if the phone number or email already exists, excluding the current user
        if CustomUser.objects.filter(phone_number=phone_number).exclude(id=user_id).exists():
            print("A user with this phone number already exists.")
            return Response({"message": "A user with this phone number already exists."}, status=400)

        if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            print("A user with this email already exists.")
            return Response({"message": "A user with this email already exists."}, status=400)

        # Update user fields
        user.phone_number = phone_number
        user.email = email
        user.role = role
        user.save()

        return Response({"message": "User updated successfully."}, status=200)

    except ObjectDoesNotExist:
        return Response({"message": "User with the given ID does not exist."}, status=404)

    except Exception as e:
        # Catch-all for unexpected errors
        return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=500)

    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_users(request):
    # if request.user.role != 'admin':
    #     return Response({"error": "You are not authorized to view this resource."}, status=403)
    
    users = CustomUser.objects.all().values(
        'id', 'phone_number', 'email', 'role', 'created_at',
    )
    return Response({"users": list(users)}, status=200)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        
        # if request.user.role != 'admin' and request.user.id != user.id or request.user.role != 'manager' and request.user.id != user.id:
        #     return Response({"error": "You are not authorized to access this user."}, status=403)
        
       
        return Response({
            "id": user.id,
            "phone_number": user.phone_number,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }, status=200)
    except ObjectDoesNotExist:
        return Response({"error": "User with the given ID does not exist."}, status=404)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_email(request):
    email = request.query_params.get('email')

    if not email:
        return Response({"error": "Email is required to search for a user."}, status=400)

    try:
        user = CustomUser.objects.select_related('created_by').get(email=email)
        
        if request.user.role != 'admin' and request.user.email != email:
            return Response({"error": "You are not authorized to access this user."}, status=403)

        created_by_user = user.created_by
        return Response({
            "id": user.id,
            "phone_number": user.phone_number,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),

        }, status=200)
    except ObjectDoesNotExist:
        return Response({"error": "User with the given email does not exist."}, status=404)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_phone(request):
    phone_number = request.query_params.get('phone_number')

    if not phone_number:
        return Response({"error": "Phone number is required to search for a user."}, status=400)

    try:
        user = CustomUser.objects.select_related('created_by').get(phone_number=phone_number)
        
        if request.user.role != 'admin' and request.user.phone_number != phone_number:
            return Response({"error": "You are not authorized to access this user."}, status=403)

        created_by_user = user.created_by
        return Response({
            "id": user.id,
            "phone_number": user.phone_number,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),

        }, status=200)
    except ObjectDoesNotExist:
        return Response({"error": "User with the given phone number does not exist."}, status=404)




import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactUsSerializer
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status

# Configure logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def contact_us(request):
    logger.info("Received contact request with data: %s", request.data)
    
    serializer = ContactUsSerializer(data=request.data)
    
    if serializer.is_valid():
        names = serializer.validated_data['names']
        email = serializer.validated_data['email']
        subject = serializer.validated_data['subject']
        description = serializer.validated_data['description']
        
        # Check for empty fields
        if not names.strip():
            logger.error("Name field is empty.")
            return Response({"error": "Name field cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        if not subject.strip():
            logger.error("Subject field is empty.")
            return Response({"error": "Subject field cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        if not description.strip():
            logger.error("Description field is empty.")
            return Response({"error": "Description field cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            logger.error("Invalid email format: %s", email)
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        # Sending email
        try:
            send_mail(
                subject=f"Contact Us: {subject}",
                message=f"Name: {names}\nEmail: {email}\n\nDescription:\n{description}",
                from_email=email,
                recipient_list=['harerimanaclementkella@gmail.com'],
                fail_silently=False,
            )
            logger.info("Email sent successfully to %s", email)
            return Response({"message": "Email sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("An error occurred while sending email: %s", e)
            return Response({"error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    logger.error("Invalid serializer data: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)