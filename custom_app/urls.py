from custom_app.views import *

urls = {
    '/': CategoryList(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/edit-course/': EditCourse(),
    '/copy-course/': CopyCourse(),
    '/another_page/': another_page,
    '/contactus/': ContactUs(),
}
