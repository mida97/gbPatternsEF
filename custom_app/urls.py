from custom_app.views import *

urls = {
    '/': index_view,
    '/another_page/': another_page,
    '/contactus/': ContactUs(),
}
