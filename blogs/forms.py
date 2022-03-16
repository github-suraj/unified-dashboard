from django import forms
from .models import Category, Blog, BlogComment

def get_category_list():
    category = Category.objects.all().values_list('name', 'name')
    return [item for item in category]

class BlogCreateForm(forms.ModelForm):
    private = forms.BooleanField(help_text='Keep your blog private', required=False)

    def __init__(self, *args, **kwargs):
        super(BlogCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Blog
        fields = ['category', 'title', 'content', 'private', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 1}),
        }
