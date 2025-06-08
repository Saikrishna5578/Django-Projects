from django.contrib import messages
from django.shortcuts import redirect
from app.models import account  # Adjust the import as per your app name

def check_pin(view_func):
    def wrapper(request, *args, **kwargs):
        # Get the user name
        name = request.user
        
        try:
            # Fetch the account object
            pn = account.objects.get(name=name)
            if pn.pin == "000000":
                messages.error(request, "Please SET YOUR PIN first")
                return redirect('pin')  # Redirect to the profile page to set the pin
        except account.DoesNotExist:
            messages.error(request, "Account not found")
            return redirect('login')  # Redirect to login if account not found
        
        return view_func(request, *args, **kwargs)
    return wrapper
