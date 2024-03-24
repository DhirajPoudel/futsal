from django.shortcuts import render, redirect
from .models import Booking, Futsal
from django.db import models
from .forms import AddFutsalForm
from userAuth.models import User

def dashboard(request):
    total_users = get_total_users()
    total_bookings = get_total_bookings()
    total_futsals = get_total_futsals()

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_futsals': total_futsals,
    }

    return render(request, 'adminHome/dashboard.html', context)

def get_total_users():
    # return Booking.objects.values('user').annotate(user_count=models.Count('user')).count()
    return User.objects.count()

def get_total_bookings():
    return Booking.objects.count()

def get_total_futsals():
    return Futsal.objects.count()

def tablePage(request):
    futsals = Futsal.objects.all()
    bookings = Booking.objects.all()
    futsal_form = AddFutsalForm()
    context = {
        'futsals': futsals,
        'bookings': bookings,
        'futsal_form': futsal_form,
    }
    return render(request, 'adminHome/tables.html', context)

def addFutsal(request):
    if request.method == 'POST':
        form = AddFutsalForm(request.POST, request.FILES)
        print(request.user)
        if form.is_valid():
            form.addedBy = request.user
            form.save()
            return redirect('table')
        else:
            form = AddFutsalForm()
    return render(request, 'adminHome/table.html', {'form': form})

def approveBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Approved'
    booking.save()
    return redirect('table')

def rejectBooking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.status = 'Rejected'
    booking.save()
    return redirect('table')