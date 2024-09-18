from django.shortcuts import redirect
from .request_manager import Action
from frontend.settings import MAIN_URL
from django.http import HttpRequest

def login_required (function) : 

    def wrapper (self, request, **kwargs) : 

        user = request.COOKIES.get('user',None)

        if user is None :
            kwargs['headers'] = None
        
        else:
            action = Action(
                url = MAIN_URL + '/user/profile/',
                headers = {'Authorization':f"Bearer {user}"}
            )

            action.get()

            if not action.is_valid : 
                kwargs['headers'] = None
            else:
                kwargs['headers'] = {'Authorization':f"Bearer {user}"}
                kwargs['user'] = action.json_data()
        
        if kwargs['headers'] is None :
            return redirect('login')
        
        func = function(self,request,**kwargs)
        return func
    
    return wrapper


