from django.shortcuts import render, redirect
from adminHome.models import Futsal
from django.contrib.auth import logout
from adminHome.models import Futsal, Booking
from datetime import datetime, timedelta
from django.contrib import messages
from .forms import FutsalSearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from adminHome.forms import AddFutsalForm

def homePage(request):
    futsals = Futsal.objects.all()
    total_futsals = Futsal.objects.count()
    form = FutsalSearchForm()
    futsal_types = Futsal.objects.values_list('futsal_type', flat=True).distinct()
    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
        user_booked_count = Booking.objects.filter(user=request.user).count()
    else:
        user_booked_futsals = None
    context = {
        'futsals': futsals,
        'total_futsals': total_futsals,
        'futsal_types': futsal_types,
        'user_booked_futsals': user_booked_futsals,
        'user_booked_count': user_booked_count,
        'form': form,
    }

    return render (request, 'userHome/home.html', context) 


# def futsalPage(request):
#     futsals = Futsal.objects.all()
#     form = FutsalSearchForm()

#     if request.user.is_authenticated:
#         user_booked_futsals = Booking.objects.filter(user=request.user)
#     else:
#         user_booked_futsals = None

#         for futsal in user_booked_futsals:
#             print(futsal.futsal)

#     context = {
#         'futsals': futsals,
#         'user_booked_futsals': user_booked_futsals,
#         'form': form, 
#     }
#     return render (request, 'userHome/futsal_list.html', context)


def bookFutsal(request, pk):
    futsal = Futsal.objects.get(id=pk)
    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
    else:
        user_booked_futsals = None

    time_slots = []
    book_time = 1
    print(futsal.open_time , futsal.close_time)
    while futsal.open_time <= futsal.close_time:
        time_slots.append(futsal.open_time.strftime("%I:%M %p"))
        futsal.open_time = futsal.open_time.replace(hour=futsal.open_time.hour + book_time)

    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        book_time = request.POST.get('book_time')
        print(booking_date, booking_time, book_time)
        try:
            booking = Booking.objects.create(
            user=request.user,
            futsal=Futsal.objects.get(id=pk),
            booking_date=booking_date,
            booking_time=booking_time,
            book_time=book_time
        )
            messages.success(request, f' {'Successfully Booked at ' + booking.futsal.name }')
            return redirect('/futsal_list/')
        except Exception as e:
            raise Exception("Booking Failed" + str(e))
            return redirect('futsal_list/')

    context = {
        'futsal': futsal,
        'time_slots': time_slots,
        'user_booked_futsals': user_booked_futsals,

    }
    return render(request, 'userHome/checkout.html', context)

def futsal_section(request):
    futsals = Futsal.objects.all()

def logoutUser(request):
    logout(request)
    return redirect('login')


def myBookings(request):
    bookings = Booking.objects.filter(user=request.user)
    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)


    print(bookings)
    context = {
        'bookings': bookings,
        'user_booked_futsals':  user_booked_futsals,
    }
    return render(request, 'userHome/my_bookings.html', context)


def searchFutsal(request):
    print("hello")
    form = FutsalSearchForm()
    if request.method == 'POST':
        form = FutsalSearchForm(request.POST)

    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        name = form.cleaned_data.get('name')
        location = form.cleaned_data.get('location')
        futsal_type = form.cleaned_data.get('futsal_type')
        price = form.cleaned_data.get('price')

        # Filter Futsal objects based on the search criteria
        futsals = Futsal.objects.filter(
            name__icontains=search_query,
            location__icontains=location,
            futsal_type__icontains=futsal_type,
            price__lte=price,
            # Add more filters as needed
        )

        # You can customize the search logic based on your requirements

        context = {'futsals': futsals, 'form': form}
        return render(request, 'userHome/search_response.html', context)

    context = {'form': form}
    return render(request, 'userHome/home.html', context)


def futsalPage(request):
    futsals = Futsal.objects.all()
    form = FutsalSearchForm()

    if request.user.is_authenticated:
        user_booked_futsals = Booking.objects.filter(user=request.user)
    else:
        user_booked_futsals = None

    context = {
        'futsals': futsals,
        'user_booked_futsals': user_booked_futsals,
        'form': form, 
    }

    return render(request, 'userHome/futsal_list.html', context)


def cancelBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    try:
        booking.delete()
        messages.success(request, f'Booking Cancelled')
    except Exception as e:
        raise Exception("Booking Cancellation Failed" + str(e))
    
    return redirect('my_bookings')

def manageFutsal(request):
    futsals = Futsal.objects.filter(addedBy=request.user)
    futsal_form = AddFutsalForm()

    if request.method == 'POST':
        print('Hello')
        futsal_form = AddFutsalForm(request.POST, request.FILES)
        if futsal_form.is_valid():
            futsal = futsal_form.save(commit=False)
            print(f"Before setting addedBy: {futsal.addedBy}")  # Debugging line
            futsal.addedBy = request.user
            print(f"After setting addedBy: {futsal.addedBy}")  # Debugging line
            futsal.save()
            return redirect('manage_futsal')

    context = {
        'futsals': futsals,
        'futsal_form': futsal_form,
    }
    return render(request, 'userHome/futsal_owner_table.html', context)

   