from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    """
    View for creating user accounts.
    """
    if request.method == 'POST':
        # Ininitializing form with data the post request
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # If a request is a post and the form submitted is valid
            # save the data in the form to the database
            form.save()
            # Give the user a message to tell them that account creation
            # was successful
            messages.success(
                request,
                'Your account has been created. You can now login'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
