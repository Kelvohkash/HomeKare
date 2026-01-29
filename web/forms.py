from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Worker, Service, Review, UserProfile

class WorkerRegistrationForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select the services you are proficient in."
    )

    class Meta:
        model = Worker
        fields = [
            'full_name', 'email', 'phone_number', 'id_number', 
            'location', 'experience_level', 'skills', 'id_scan'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'id_number': forms.TextInput(attrs={'placeholder': 'ID/Passport Number'}),
            'location': forms.TextInput(attrs={'placeholder': 'Primary Area of Operation'}),
            'experience_level': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to all fields
        standard_classes = "w-full pl-12 pr-5 py-4 bg-white/50 border border-purple-100 focus:border-purple-500/50 rounded-2xl outline-none focus:ring-4 focus:ring-purple-500/10 transition-all placeholder:text-gray-400"
        for field in self.fields:
            if field != 'skills' and field != 'id_scan':
                self.fields[field].widget.attrs.update({'class': standard_classes})
            elif field == 'id_scan':
                self.fields[field].widget.attrs.update({'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'w-full px-5 py-3 bg-white/50 border border-purple-100 rounded-xl outline-none focus:border-purple-500/50 transition-all'}),
            'comment': forms.Textarea(attrs={'class': 'w-full px-5 py-3 bg-white/50 border border-purple-100 rounded-xl outline-none focus:border-purple-500/50 transition-all', 'rows': 3, 'placeholder': 'Tell us about your experience...'}),
        }

class CustomSignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100, 
        label='Full Name', 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )
    phone_number = forms.CharField(
        max_length=20, 
        label='Phone Number', 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    contact_preference = forms.ChoiceField(
        choices=UserProfile.CONTACT_PREFERENCE_CHOICES,
        label='How should we reach out to you?',
        widget=forms.Select(attrs={'class': 'w-full px-5 py-3 bg-white/50 border border-purple-100 rounded-xl outline-none'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        standard_classes = "w-full pl-12 pr-5 py-4 bg-white/50 border border-purple-100 focus:border-purple-500/50 rounded-2xl outline-none focus:ring-4 focus:ring-purple-500/10 transition-all placeholder:text-gray-400"
        
        # Style all fields
        for fieldname, field in self.fields.items():
            # Update class
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs.update({'class': f"{standard_classes} {existing_class}".strip()})
            
            # Ensure placeholders for default allauth fields
            if fieldname == 'email':
                field.widget.attrs.update({'placeholder': 'Enter your email address'})
            elif fieldname == 'password1':
                field.widget.attrs.update({'placeholder': 'Create a strong password'})
            elif fieldname == 'password2':
                field.widget.attrs.update({'placeholder': 'Repeat your password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
            # Profile is created by signal, so we update it
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.contact_preference = self.cleaned_data['contact_preference']
            profile.save()
        return user
