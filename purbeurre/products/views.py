from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, RedirectView

from sentry_sdk import capture_message, configure_scope

from authentication.models import User
from .models import Product, Substitute
# Create your views here.


class SearchView(ListView):
    """Return products from DB from query."""
    template_name = 'products/search.html'
    paginate_by = 9

    def get_queryset(self):
        with configure_scope() as scope:
            if '_auth_user_id' in self.request.session._session:
                scope.user = {
                    "email": User.objects.get(pk=self.request.session._session['_auth_user_id']).email
                }
            scope.level = 'info'
            capture_message('New search')

        return Product.objects.filter(
            product_name__icontains=self.request.GET['query']).\
                order_by('product_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET['query']
        context['target'] = 'products:result'
        context['query'] = self.request.GET['query']
        return context

class ResultView(ListView):
    """Return substitutes with same category and better/equal nutrigrade."""
    template_name = 'products/result.html'

    def get_queryset(self):
        self.product = Product.objects.get(pk=self.kwargs['product_id'])
        return Product.objects\
            .filter(category=self.product.category)\
            .filter(nutrition_grades__lte=self.product.nutrition_grades)\
            .exclude(id=self.kwargs['product_id'])\
            .order_by('nutrition_grades')[:9]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'allreadysaved' in self.request.GET:
            context['message'] = 'Déjà enregistré'
        context['query'] = self.product.product_name
        context['product'] = self.product
        context['title'] = self.product
        context['target'] = 'products:detail'
        return context


class DetailProductView(DetailView):
    """Show product details."""
    template_name = 'products/detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = kwargs['object'].product_name
        return context


class MyProductsView(LoginRequiredMixin, ListView):
    """Show saved products."""
    template_name = 'products/myproducts.html'
    paginate_by = 5

    def get_queryset(self):
        return Substitute.objects.filter(
            user_id=self.request.user.id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mes produits'
        context['target'] = 'products:result'
        return context


class DeleteSubstituteView(LoginRequiredMixin, DeleteView):
    """Ask for delete saved product."""
    model = Substitute
    success_url = reverse_lazy('products:myproducts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mes produits'
        return context


@login_required
def SaveView(request):
    """Save product/substitute."""
    if request.method == 'POST':
        # get data from POST
        product_id = request.POST['product_id']
        substitute_id = request.POST['substitute_id']
        next_url = request.POST['next']
        # get data from DB
        product_obj = Product.objects.get(pk=product_id)
        substitute_obj = Product.objects.get(pk=substitute_id)
        user_obj = User.objects.get(pk=request.user.id)
        # test if all obj are sets
        if product_obj and substitute_obj and user_obj:
            # create Substitute or return "allreadysaved"
            obj, created = Substitute.objects.get_or_create(
                user_id=user_obj,
                product_id=product_obj,
                substitute_id=substitute_obj
                )
            if created:
                return redirect('products:myproducts')
            else:
                return redirect(next_url+"?allreadysaved")
    return redirect('index')
