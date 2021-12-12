from custom_app.views import *

urls = {
    '/': index_view,
    '/admin/': AdminView(),
    '/books/': Books(),
    '/contactus/': ContactUs(),
}
