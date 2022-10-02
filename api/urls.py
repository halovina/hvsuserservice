from django.urls import path
from api.users.views import LoginView
from api.product.views import ProductView, FilterProductView, DownloadFileCsvProduct

urlpatterns = [
    path('v1/users/login', LoginView.as_view(), name='api_users_login'),
    path('v1/product/', ProductView.as_view(), name='api_post_list_product'),
    path('v1/product/<int:key>/edit', ProductView.as_view(), name='api_edit_product'),
    path('v1/product/<int:key>/delete', ProductView.as_view(), name='api_delete_product'),
    path('v1/product/filter/bydate', FilterProductView.as_view(), name='api_filter_product_by_date'),
    path('v1/product/download-csv/<str:key>', DownloadFileCsvProduct.as_view(), name='api_product_downlaod_csv'),
]
